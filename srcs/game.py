import random
import sys

from pydantic import BaseModel, ConfigDict, Field
from config import GameState, Config
from mazegenerator import MazeGenerator
from objects import Ghost, PacGum, Pacman, SuperPacGum
from ghosts import Blinky, Clyde, Inky, Pinky
from enum import Enum

FULL_WALL = 15
PACMAN_STEP = 0.15
GHOST_STEP = 0.20
FRIGHTENED_TIME = 8.0


class Directions(Enum):
    NORTH = (0, -1, 1, 4)
    EAST = (1, 0, 2, 8)
    SOUTH = (0, 1, 4, 1)
    WEST = (-1, 0, 8, 2)

class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    state: GameState = Field(default_factory=GameState)
    config: Config = Field(default_factory=Config)
    valid_positions: list[tuple[int, int]] = Field(default_factory=list)
    valid_set: set[tuple[int, int]] = Field(default_factory=set)
    maze: list[list[int]] = Field(default_factory=list)
    rng: random.Random = Field(default_factory=random.Random)
    
    level_index: int = 0
    status: str = "running"  #     running    or    game_over      ot         won
    time_left: float = 0.0
    direction: Directions | None = None
    next_direction: Directions | None = None
    pacman_spawn: tuple[int, int] = (0, 0)
    pacman_acc: float = 0.0
    ghost_acc: float = 0.0

    def setup(self, file_path: str) -> None:
        self.config.file_path = file_path
        self.config.extract()
        self.state = GameState(lives=self.config.lives)
        self.status = "running"
        self.load_level(0)

    def load_level(self, level_index: int) -> None:
        levels = self.config.data.get("level")
        if not isinstance(levels, list) or not 0 <= level_index < len(levels):
            print(f"Level not found: {level_index}", file=sys.stderr)
            sys.exit(1)
        try:
            dat = levels[level_index]
            size = (dat["width"], dat["height"])
        except (KeyError, TypeError):
            print(f"Invalid level definition: {level_index}", file=sys.stderr)
            sys.exit(1)

        self.maze = MazeGenerator(seed=self.config.seed, size=size).maze
        if not self.maze:
            print(f"Level not found: {level_index}", file=sys.stderr)
            sys.exit(1)

        self.level_index = level_index
        self.rng = random.Random(self.config.seed + level_index)
        self.time_left = float(self.config.time_limit)
        self.collect_valid_positions()
        self.init_positions()

    def collect_valid_positions(self) -> None:
        self.valid_positions = [
            (x, y)
            for y, row in enumerate(self.maze)
            for x, cell in enumerate(row)
            if cell != FULL_WALL
        ]
        self.valid_set = set(self.valid_positions)

    def closest_euclidean_valid(self) -> tuple[int, int]:
        width = len(self.maze[0])
        height = len(self.maze)
        center = (width // 2, height // 2)
        return min(
            self.valid_positions,
            key=lambda pos: (pos[0] - center[0]) ** 2 + (pos[1] - center[1]) ** 2,
        )

    def init_positions(self) -> None:
        if not self.valid_positions:
            print("Maze has no valid positions", file=sys.stderr)
            sys.exit(1)

        self.state.ghosts = []
        self.state.pacgums = []
        self.state.super_pacgums = []
        self.state.frightened_timer = 0.0
        self.direction = None
        self.next_direction = None
        self.pacman_acc = 0.0
        self.ghost_acc = 0.0

        width = len(self.maze[0])
        height = len(self.maze)
        center = (width // 2, height // 2)
        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]

        if center in self.valid_set:
            spawn = center
        else:
            spawn = self.closest_euclidean_valid()
        self.pacman_spawn = spawn
        self.state.pacman = Pacman(x=spawn[0], y=spawn[1], state="alive")

        if not all(corner in self.valid_set for corner in corners):
            print("Invalid corner positions", file=sys.stderr)
            sys.exit(1)

        for ghost_cls, (cx, cy) in zip((Blinky, Clyde, Inky, Pinky), corners):
            self.state.ghosts.append(ghost_cls(
                x=cx, start_x=cx, y=cy, start_y=cy, state="alive",
                score=self.config.point_per_ghost, pacman=self.state.pacman,
            ))
            self.state.super_pacgums.append(SuperPacGum(
                x=cx, y=cy, eaten=False, score=self.config.point_per_sgum,
            ))

        excluded = set(corners)
        excluded.add(spawn)
        available = [pos for pos in self.valid_positions if pos not in excluded]
        count = min(self.config.data.get("pacgum", 0), len(available))
        for x, y in self.rng.sample(available, count):
            self.state.pacgums.append(
                PacGum(x=x, y=y, eaten=False, score=self.config.point_per_gum)
            )


    def set_direction(self, direction: Directions) -> None:
        """Call this from your input handler."""
        if isinstance(direction, Directions):
            self.next_direction = direction

    def can_move(self, x: int, y: int, direction: Directions) -> bool:
        if not isinstance(direction, Directions):
            return False
        dx, dy, wall, opposite_wall = direction.value
        nx, ny = x + dx, y + dy

        if not (0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0])):
            return False
        if self.maze[y][x] & wall:
            return False
        if self.maze[ny][nx] & opposite_wall:
            return False
        return True

    def update_pacman(self) -> None:
        pacman = self.state.pacman
        if pacman is None:
            return
        for direction in (self.next_direction, self.direction):
            if direction and self.can_move(pacman.x, pacman.y, direction):
                self.direction = direction
                dx, dy = direction.value[:2]
                pacman.x += dx
                pacman.y += dy
                pacman.direction = (dx, dy)
                return


    def update_ghosts(self) -> None:
        blinky = next((g for g in self.state.ghosts if isinstance(g, Blinky)), None)
        for ghost in self.state.ghosts:
            if ghost.edible:
                ghost.wander(self.maze, self.rng)
            else:
                ghost.chase(self.maze, blinky)


    def eat_ghost(self, ghost: Ghost) -> None:
        self.state.score += ghost.score
        ghost.respawn()

    def reset_positions(self) -> None:
        pacman = self.state.pacman
        if pacman is not None:
            pacman.x, pacman.y = self.pacman_spawn
        if pacman is not None:
            pacman.direction = (0, 0)
        self.direction = None
        self.next_direction = None
        self.state.frightened_timer = 0.0
        for ghost in self.state.ghosts:
            ghost.respawn()

    def lose_life(self) -> None:
        self.state.lives -= 1
        if self.state.lives <= 0:
            self.status = "game_over"
        else:
            self.reset_positions()

    def check_ghost_collisions(self) -> None:
        pacman = self.state.pacman
        if not pacman:
            return
        for ghost in self.state.ghosts:
            if (ghost.x, ghost.y) != (pacman.x, pacman.y):
                continue
            if ghost.edible:
                self.eat_ghost(ghost)
            else:
                self.lose_life()
                return

    def frighten_ghosts(self) -> None:
        self.state.frightened_timer = FRIGHTENED_TIME
        for ghost in self.state.ghosts:
            ghost.edible = True
            ghost.state = "vulnerable"

    def check_gums_collisions(self) -> None:
        pacman = self.state.pacman
        if not pacman:
            return
        pos = (pacman.x, pacman.y)
        for pacgum in self.state.pacgums:
            if not pacgum.eaten and (pacgum.x, pacgum.y) == pos:
                pacgum.eaten = True
                self.state.score += pacgum.score
        for super_pacgum in self.state.super_pacgums:
            if not super_pacgum.eaten and (super_pacgum.x, super_pacgum.y) == pos:
                super_pacgum.eaten = True
                self.state.score += super_pacgum.score
                self.frighten_ghosts()
        self.state.pacgums = [g for g in self.state.pacgums if not g.eaten]
        self.state.super_pacgums = [g for g in self.state.super_pacgums if not g.eaten]


    def update_frightened(self, delta_time: float) -> None:
        if self.state.frightened_timer <= 0:
            return
        self.state.frightened_timer -= delta_time
        if self.state.frightened_timer <= 0:
            self.state.frightened_timer = 0.0
            for ghost in self.state.ghosts:
                if ghost.edible:
                    ghost.edible = False
                    ghost.state = "alive"

    def check_game_over(self) -> bool:
        return self.state.lives <= 0 or self.time_left <= 0

    def check_level_completion(self) -> bool:
        return (all(g.eaten for g in self.state.pacgums)
                and all(g.eaten for g in self.state.super_pacgums))

    def advance_level(self) -> None:
        next_index = self.level_index + 1
        if next_index >= len(self.config.data.get("level", [])):
            self.status = "won"
        else:
            self.load_level(next_index)

    def update(self, delta_time: float) -> None:
        """delta_time in seconds."""
        if self.status != "running":
            return

        self.time_left -= delta_time
        self.update_frightened(delta_time)

        self.pacman_acc += delta_time
        while self.pacman_acc >= PACMAN_STEP and self.status == "running":
            self.pacman_acc -= PACMAN_STEP
            self.update_pacman()
            self.check_gums_collisions()
            self.check_ghost_collisions()

        self.ghost_acc += delta_time
        while self.ghost_acc >= GHOST_STEP and self.status == "running":
            self.ghost_acc -= GHOST_STEP
            self.update_ghosts()
            self.check_ghost_collisions()

        if self.status != "running":
            return
        if self.check_game_over():
            self.status = "game_over"
        elif self.check_level_completion():
            self.advance_level()
