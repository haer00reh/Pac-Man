from pydantic import BaseModel
from collections import deque

class Pacman(BaseModel):
    x: int
    y: int
    state: str

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
    state: str
    edible: bool = False
    score: int = 0

    def respawn(self):
        self.x = self.start_x
        self.y = self.start_y
        self.state = "alive"

    def move(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        maze: list[list[int]]
    ) -> tuple[int, int] | None:

        directions = [
            (0, -1, 1, 4),  # North
            (1, 0, 2, 8),   # East
            (0, 1, 4, 1),  # South
            (-1, 0, 8, 2)  # West
        ]

        queue = deque([start])
        parents = {start: None}
        if start == goal:
            return start
        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                current = goal

                while parents[current] != start:
                    current = parents[current]

                return current

            for dx, dy, wall, opposite_wall in directions:
                nx = x + dx
                ny = y + dy
                neighbor = (nx, ny)

                if not (0 <= ny < len(maze) and 0 <= nx < len(maze[0])):
                    continue

                if maze[y][x] & wall:
                    continue

                if maze[ny][nx] & opposite_wall:
                    continue

                if neighbor in parents:
                    continue

                parents[neighbor] = (x, y)
                queue.append(neighbor)

        return None