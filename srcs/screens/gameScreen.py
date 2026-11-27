from srcs.screens.screen import Screen, Screens, Font
from srcs.drawer import Drawer
import pygame as py
from srcs.game import Game
import sys
from srcs.game import Direction
from srcs.config import GameResults


class GameScreen(Screen):

    def __init__(self) -> None:
        self.next_screen: Screens = Screens.NONE
        self.quit: bool = False
        self.game: Game = Game()
        self.game.setup(sys.argv[1] if len(sys.argv) > 1 else None)
        self.w: int
        self.h: int
        self.w, self.h = py.display.get_window_size()
        self.caption_text: str = "Game Screen"
        self.drawer: Drawer = Drawer(self.game)
        py.display.set_caption(self.caption_text)

    def get_score(self) -> py.Surface:
        return (Font.H2.value.render(
            f"SCORE :  {self.game.state.score}",
            True,
            'yellow'
        ))

    def get_timer(self) -> py.Surface:
        return (Font.H2.value.render(
            f"TIMER :  {int(self.game.time_left)}",
            True,
            'yellow'
        ))

    def get_level(self) -> py.Surface:
        return (Font.H2.value.render(
            f"LEVEL  :  {self.game.level_index + 1}",
            True,
            'yellow'
        ))

    def get_lives(self) -> py.Surface:
        return (Font.H2.value.render(
            f"LIVES  :  {self.game.state.lives}",
            True,
            'yellow'
        ))

    def draw(self, screen: py.Surface) -> None:
        screen.fill((0, 0, 0))
        self.drawer.draw_maze(screen)
        score = self.get_score()
        timer = self.get_timer()
        level = self.get_level()
        lives = self.get_lives()
        screen.blit(timer, (50, self.h // 4))
        screen.blit(score, (50, (self.h // 4) + 100))
        screen.blit(level, (50, (self.h // 4) + 200))
        screen.blit(lives, (50, (self.h // 4) + 300))

    def update(self, dt: float, surface: py.Surface) -> None:
        self.game.update(dt)
        if self.game.level_completed is True:
            self.drawer.update(self.game, surface)
            self.game.level_completed = False
        if (self.game.status == "game_over"):
            self.next_screen = Screens.GAMEOVERSCREEN
        if (self.game.status == "won"):
            self.next_screen = Screens.WONSCREEN
        if self.next_screen is not Screens.NONE.value:
            GameResults(
                self.game.state.score,
                self.game.level_index + 1,
                self.game.config.highscore_file
                )

    def event_handler(self, events) -> None:
        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_LEFT:
                    self.game.set_direction(Direction.WEST)
                elif e.key == py.K_RIGHT:
                    self.game.set_direction(Direction.EAST)
                elif e.key == py.K_UP:
                    self.game.set_direction(Direction.NORTH)
                elif e.key == py.K_DOWN:
                    self.game.set_direction(Direction.SOUTH)
