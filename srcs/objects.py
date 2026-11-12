from pydantic import BaseModel
from mazegenerator import MazeGenerator
from config import Config

class Pacman(BaseModel):
    x: int
    y: int
    state: str

class PacGum(BaseModel):
    x: int
    y: int
    eaten: bool


class Ghost(BaseModel):
    x: int
    y: int
    state: str


class GameState(BaseModel):
    pacman: Pacman
    ghosts: list[Ghost]
    pacgums: list[PacGum]
    mazes: list[MazeGenerator]

    def initialize(self, configs: Config):
        self.mazes = [MazeGenerator(size=configs.data.get("maze_size", 10))]
