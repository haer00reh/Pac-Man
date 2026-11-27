from abc import ABC, abstractmethod
from enum import Enum
import pygame as py
from typing import List


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
    WONSCREEN = 'WONSCREEN'
    NONE = None


py.init()


def customFontSize(font: str = "assets/font/pixel.ttf", size: int = 30):
    return py.font.Font(font, size)


class Font(Enum):
    CUSTOM = customFontSize
    S1 = py.font.SysFont(None, 50)
    S2 = py.font.SysFont(None, 40)
    H1 = py.font.SysFont(None, 30)
    H2 = py.font.SysFont(None, 27)
    H3 = py.font.SysFont(None, 25)
    H4 = py.font.SysFont(None, 22)
    P = py.font.SysFont("arial", 16)

    def __call__(self, *values, **key):
        return customFontSize(*values, **key)


class Screen(ABC):

    @abstractmethod
    def draw(self, surface: py.Surface):
        pass

    @abstractmethod
    def update(self, dt: float, surface: py.Surface):
        pass

    @abstractmethod
    def event_handler(self, events: List[py.event.EventType]):
        pass
