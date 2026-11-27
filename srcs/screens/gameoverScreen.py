from srcs.screens.screen import Screen, Screens, Font
import pygame as py
from srcs.config import GameResults
from typing import Tuple


class GameOverScreen(Screen):
    def __init__(self) -> None:
        self.next_screen: Screens = Screens.NONE
        self.width: int
        self.height: int
        self.width, self.height = py.display.get_window_size()
        self.caption_text: str = "Game Screen"
        game_over_img: py.Surface = py.image.load(
            "assets/game_over_bg.jpeg").convert()
        self.background: py.Surface = py.transform.scale(
            game_over_img, (self.width, self.height))
        self.results: GameResults = GameResults._getinstance()
        self.quit: bool = False
        py.display.set_caption(self.caption_text)

    def draw(self, screen: py.Surface) -> None:
        screen.blit(self.background, (0, 0))
        screen.blit(*self.get_height_score())
        screen.blit(*self.get_final_score())
        screen.blit(*self.get_final_level())
        screen.blit(*self.get_try_message())
        screen.blit(*self.get_quit_message())

    def update(self, dt: float, surface: py.Surface) -> None:
        pass

    def event_handler(self, events) -> None:
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.next_screen = Screens.GAMESCREEN
                if event.key == py.K_ESCAPE:
                    self.quit = True

    def get_height_score(self) -> Tuple[py.Surface, py.Rect]:
        high_score: int = 1400  # get high score from json file

        text: py.Surface = Font.CUSTOM(size=40).render(
            f"final high_score: {high_score}".upper(),
            True,
            'white'
        )
        text_rect: py.Rect = text.get_rect()
        text_rect.center = (self.width // 2, (self.height // 2) + 100)
        return text, text_rect

    def get_final_score(self) -> Tuple[py.Surface, py.Rect]:
        score: int = self.results.score

        text: py.Surface = Font.CUSTOM(size=40).render(
            f"final score: {score}".upper(),
            True,
            'white'
        )
        text_rect: py.Rect = text.get_rect()
        text_rect.center = (self.width // 2, (self.height // 2) + 150)
        return text, text_rect

    def get_final_level(self) -> Tuple[py.Surface, py.Rect]:
        level: int = self.results.level

        text: py.Surface = Font.CUSTOM(size=40).render(
            f"level: {level}".upper(),
            True,
            'white'
        )
        text_rect: py.Rect = text.get_rect()
        text_rect.center = (self.width // 2, (self.height // 2) + 200)
        return text, text_rect

    def get_try_message(self) -> Tuple[py.Surface, py.Rect]:
        text: py.Surface = Font.CUSTOM(size=30).render(
            "press space to try again".upper(),
            True,
            'yellow'
        )
        text_rect: py.Rect = text.get_rect()
        text_rect.center = (self.width // 2, (self.height) - 150)
        return text, text_rect

    def get_quit_message(self) -> Tuple[py.Surface, py.Rect]:
        text: py.Surface = Font.CUSTOM(size=30).render(
            "press esc to quit".upper(),
            True,
            'yellow'
        )
        text_rect: py.Rect = text.get_rect()
        text_rect.center = (self.width // 2, (self.height) - 100)
        return text, text_rect
