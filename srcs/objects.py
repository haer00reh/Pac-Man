from pydantic import BaseModel

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
