from srcs.screens.screen import Screen, Screens, Font
import pygame as py
from typing import List, Dict
from srcs.game import Game
import sys
import json
from srcs.error import Error


class LeaderboardScreen(Screen):

    def __init__(self) -> None:
        self.next_screen: Screens = Screens.NONE
        self.width: int
        self.height: int
        self.width, self.height = py.display.get_window_size()
        self.caption_text: str = "Leaderboard Screen"
        img: py.Surface = py.image.load('assets/leaderboard_bg.jpeg')
        self.bg = py.transform.scale(img, (self.width, self.height))
        self.quit = False
        self.leaderboard: List[Dict[str, str | int]] = []
        self.file_not_found: bool = True
        self.message_event = Font.CUSTOM(size=15).render(
            f"Press {"enter".upper()} To Start",
            True,
            "yellow"
        )
        self.message_rect = self.message_event.get_rect(
            center=(self.width // 2, 200))
        self.upload()

    def upload(self) -> None:
        config: str = Game._getconfig(sys.argv[1] if len(sys.argv) >= 2
                                      else None)
        data: list = []
        try:
            with open(config, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except Exception as e:
            raise Error(e)
        else:
            self.file_not_found = False
        data = data[:10]
        data.sort(key=lambda e: e.get('score'), reverse=True)
        self.leaderboard = data

    def draw(self, screen):
        py.display.set_caption(self.caption_text)
        screen.blit(self.bg, (0, 0))
        if not self.file_not_found:
            for i, ele in enumerate(self.leaderboard):
                screen.blit(*self.format_record(ele, i))
        else:
            text: py.Surface = Font.CUSTOM(size=20).render(
                    "- empty -".upper(), True, 'white'
                )
            rect = text.get_rect(center=(self.width//2, self.height // 2))
            screen.blit(
                text, rect
            )
        screen.blit(self.message_event, self.message_rect)

    def format_record(self, ele: Dict[str, str | int], i: int):
        text = Font.CUSTOM(size=20).render(
            f"{i + 1}.{str(ele.get('name', None))} - {ele.get('score')} pts",
            False,
            'white'
        )
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2,
                            ((self.height // 2) - 100) + i * 50)
        return text, text_rect

    def update(self, dt: float, surface: py.Surface):
        pass

    def event_handler(self, events):
        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_RETURN:
                    self.next_screen = Screens.GAMESCREEN
