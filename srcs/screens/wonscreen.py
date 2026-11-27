from srcs.screens.screen import Screen, Screens, Font
from srcs.config import GameResults
import pygame as py
from pathlib import Path
import json
from json import JSONDecodeError
from typing import List, Dict
import sys
from typing import Tuple
from srcs.error import Error


class WonScreen(Screen):
    def __init__(self) -> None:
        self.next_screen: Screens = Screens.NONE
        self.caption_text: str = "Winner Screen"
        self.width: int
        self.height: int
        self.width, self.height = py.display.get_window_size()
        game_over_img = py.image.load("assets/won_bg.jpeg").convert()
        self.background: py.Surface = py.transform.scale(
            game_over_img, (self.width, self.height))
        box_width = 500
        box_height = 60
        self.text_box_rect: py.Rect = py.Rect(
            (self.width // 2) - (box_width // 2),
            (self.height // 2) - (box_height // 2) - 100,
            box_width, box_height
        )
        self.box_color: py.Color = py.Color("#373A3DFF")
        self.input_text: str = ''
        self.results: GameResults = GameResults._getinstance()
        self.quit: bool = False

    def draw(self, screen: py.Surface) -> None:
        py.display.set_caption(self.caption_text)
        screen.blit(self.background, (0, 0))
        py.draw.rect(
            screen, self.box_color, self.text_box_rect, border_radius=6)

        text_surface: py.Surface = Font.CUSTOM(None, size=60).render(
            self.input_text, True, 'white')
        text_rect: py.Rect = text_surface.get_rect()
        text_rect.center = self.text_box_rect.center
        screen.blit(text_surface, text_rect)
        screen.blit(*self.get_message())
        screen.blit(*self.get_info())

    def update(self, dt: float, surface: py.Surface) -> None:
        pass

    def event_handler(self, events) -> None:
        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_RETURN:
                    if len(self.input_text) != 0:
                        self.save_record()
                        self.next_screen = Screens.LEADERBOARDSCREEN
                if e.key == py.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif len(self.input_text) >= 10:
                    continue
                else:
                    self.input_text += (e.unicode
                                        if self.valid_name(e.unicode)
                                        else '')

    def valid_name(self, s: str):
        if s in ' ':
            return True
        if not s.isalnum():
            return False
        return True

    def get_message(self) -> Tuple[py.Surface, py.Rect]:
        text: py.Surface = Font.CUSTOM(size=20).render(
            "enter your name and press enter to save score".upper(),
            True,
            'white'
        )
        text_rect: py.Rect = text.get_rect(
            center=(self.width // 2,
                    (self.height // 2) - 150
                    ))
        return text, text_rect

    def get_info(self) -> Tuple[py.Surface, py.Rect]:
        text: py.Surface = Font.CUSTOM(size=20).render(
            (f"score: {self.results.score}    "
             f"level: {self.results.level}").upper(),
            True,
            'white'
        )
        text_rect: py.Rect = text.get_rect(
            center=(self.width // 2,
                    (self.height) - 100
                    ))
        return text, text_rect

    def save_record(self) -> None:
        file: Path = Path(self.results.file)
        self.input_text = self.input_text.strip()
        if not file.exists():
            self.write(file)
        else:
            self.append(file)

    def write(self, f: Path) -> None:
        try:
            with open(f.__str__(), 'w', encoding='utf-8') as fd:
                data = []
                data.append({
                    "name": self.input_text,
                    "score": self.results.score,
                    'level': self.results.level
                })
                json.dump(data[:10], fd, indent=4)
        except Exception as e:
            raise Error(e)

    def append(self, f: Path) -> None:
        try:
            with open(f.__str__(), 'r', encoding='utf-8') as fd:
                data: List[Dict[str, str | int]] = json.load(fd)
            data.sort(key=lambda e: e['score'], reverse=True)
            data = data[:9]
            with open(f.__str__(), 'w', encoding='utf-8') as fd:
                data.append({
                    "name": self.input_text,
                    "score": self.results.score,
                    "level": self.results.level
                })
                data.sort(key=lambda e: e['score'], reverse=True)
                json.dump(data, fd, indent=4)

        except JSONDecodeError:
            self.write(f)
        except Exception as e:
            print(e)
            sys.exit(1)
