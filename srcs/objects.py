import random
from collections import deque

from pydantic import BaseModel

FULL_WALL = 15

DIRECTIONS = [
    (0, -1, 1, 4),   # North
    (1, 0, 2, 8),    # East
    (0, 1, 4, 1),    # South
    (-1, 0, 8, 2),   # West
]


def open_neighbors(x: int, y: int, maze: list[list[int]]) -> list[tuple[int, int]]:
    """Tiles you can step to from (x, y) without crossing a wall."""
    result = []
    for dx, dy, wall, opposite_wall in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if not (0 <= ny < len(maze) and 0 <= nx < len(maze[0])):
            continue
        if maze[y][x] & wall:
            continue
        if maze[ny][nx] & opposite_wall:
            continue
        result.append((nx, ny))
    return result


class Pacman(BaseModel):
    x: int
    y: int
    state: str
    direction: tuple[int, int] = (0, 0)


class PacGum(BaseModel):
    x: int
    y: int
    score: int = 0
    eaten: bool


class SuperPacGum(PacGum):
    pass


class Ghost(BaseModel):
    x: int
    y: int
    start_x: int
    start_y: int
    pacman: Pacman
    state: str
    edible: bool = False
    score: int = 0

    def respawn(self) -> None:
        self.x = self.start_x
        self.y = self.start_y
        self.state = "alive"
        self.edible = False

    def get_ahead_position(self, distance: int) -> tuple[int, int]:
        dx, dy = self.pacman.direction
        return (self.pacman.x + dx * distance, self.pacman.y + dy * distance)

    def get_target(self, blinky: "Ghost | None" = None) -> tuple[int, int]:
        """Blinky's behaviour by default: go straight for pacman."""
        return self.pacman.x, self.pacman.y

    def snap_to_valid(self, target: tuple[int, int],
                      maze: list[list[int]]) -> tuple[int, int]:
        """Pinky/Inky targets can land in a wall or outside the maze."""
        tx, ty = target
        if 0 <= ty < len(maze) and 0 <= tx < len(maze[0]) and maze[ty][tx] != FULL_WALL:
            return target
        return min(
            ((x, y) for y, row in enumerate(maze)
             for x, cell in enumerate(row) if cell != FULL_WALL),
            key=lambda p: (p[0] - tx) ** 2 + (p[1] - ty) ** 2,
        )

    def move(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        maze: list[list[int]],
    ) -> tuple[int, int] | None:
        """BFS: returns the next tile on the shortest path to goal."""
        if start == goal:
            return start
        queue = deque([start])
        parents: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                current = goal
                while parents[current] != start:
                    current = parents[current]
                return current
            for neighbor in open_neighbors(x, y, maze):
                if neighbor in parents:
                    continue
                parents[neighbor] = (x, y)
                queue.append(neighbor)
        return None

    def chase(self, maze: list[list[int]], blinky: "Ghost | None" = None) -> None:
        target = self.snap_to_valid(self.get_target(blinky), maze)
        step = self.move((self.x, self.y), target, maze)
        if step is not None:
            self.x, self.y = step

    def wander(self, maze: list[list[int]], rng: random.Random) -> None:
        """Used while the ghost is edible."""
        options = open_neighbors(self.x, self.y, maze)
        if options:
            self.x, self.y = rng.choice(options)