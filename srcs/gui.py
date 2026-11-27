import pygame as py
from srcs.screens.menuScreen import MenuScreen
from srcs.screens.screen import Screens, Font
from srcs.screens.gameoverScreen import GameOverScreen
from srcs.screens.gameScreen import GameScreen
from srcs.screens.leaderboardScreen import LeaderboardScreen
from srcs.screens.wonscreen import WonScreen
from typing import Tuple, List


class GUI:
    def __init__(self) -> None:
        py.init()

        displays: List[Tuple[int, int]] = py.display.get_desktop_sizes()
        screen_width, screen_height = displays[0]
        width: int = 1000 if screen_width <= 1600 else 1300
        height: int = 750 if screen_height <= 900 else 900
        self.screen: py.Surface = py.display.set_mode((width, height))

        self.icon: py.Surface = py.image.load("assets/icon.png")
        self.running: bool = True
        current_screen: (
            MenuScreen | GameOverScreen | LeaderboardScreen
            | GameScreen | WonScreen) = MenuScreen()
        clock: py.time.Clock = py.time.Clock()
        py.display.set_icon(self.icon)
        quit_message: py.Surface = Font.CUSTOM(size=15).render(
            "[Q]: quit",
            True,
            'yellow'
        )
        quit_message_rect: py.Rect = quit_message.get_rect(
            center=(width - 100, height - 20))
        self.quit: bool = False

        while self.running:
            events: List[py.event.EventType] = py.event.get()
            dt: float = min(clock.tick(60) / 1000.0, 0.05)

            for event in events:
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_q:
                        self.quit = True
            current_screen.event_handler(events)
            current_screen.update(dt, self.screen)
            current_screen.draw(self.screen)

            if current_screen.next_screen is not Screens.NONE:
                if current_screen.next_screen == Screens.MENUSCREEN:
                    current_screen = MenuScreen()
                elif current_screen.next_screen == Screens.GAMESCREEN:
                    current_screen = GameScreen()
                elif current_screen.next_screen == Screens.LEADERBOARDSCREEN:
                    current_screen = LeaderboardScreen()
                elif current_screen.next_screen == Screens.GAMEOVERSCREEN:
                    current_screen = GameOverScreen()
                elif current_screen.next_screen == Screens.WONSCREEN:
                    current_screen = WonScreen()
                current_screen.next_screen = Screens.NONE

            self.screen.blit(quit_message, quit_message_rect)
            if (current_screen.quit or self.quit):
                break

            py.display.update()

        py.quit()
