from pydantic import BaseModel

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
    state: str
    score: int = 0
