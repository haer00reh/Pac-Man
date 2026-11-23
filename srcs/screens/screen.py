from abc import ABC, abstractmethod
from enum import Enum
import pygame as py


class Colors(Enum):
    WHITE = (255, 255, 255)
    GREY = py.Color("#818181")
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)


class Screens(Enum):
    MENUSCREEN = 'MENUSCREEN'
    GAMESCREEN = 'GAMESCREEN'
    LEADERBOARDSCREEN = 'LEADERBOARDSCREEN'
    GAMEOVERSCREEN = 'GAMEOVERSCREEN'
    NONE = None


class Displays(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


py.init()


class Font(Enum):
    S1 = py.font.SysFont(None, 50)
    S2 = py.font.SysFont(None, 40)
    H1 = py.font.SysFont(None, 30)
    H2 = py.font.SysFont(None, 27)
    H3 = py.font.SysFont(None, 25)
    H4 = py.font.SysFont(None, 22)
    P = py.font.SysFont("arial", 16)


class Screen(ABC):

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def event_handler(self, events):
        pass