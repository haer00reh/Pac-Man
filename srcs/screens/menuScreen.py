
from srcs.screens.screen import Screen, Screens
import pygame as py
from srcs.button import Button


class MenuScreen(Screen):
    def __init__(self) -> None:
        self.next_screen: Screens = Screens.NONE
        self.caption_text: str = "Menu"
        self.width: int = 0
        self.height: int = 0
        self.width, self.height = py.display.get_window_size()
        self.image: py.Surface = py.image.load("assets/pacman_heading.png")
        self.heading: py.Surface = py.transform.scale(
            self.image, (self.width - 100, (self.height // 2)))
        self.heading_rect: py.Rect = self.heading.get_rect(
            center=(self.width // 2, 200))
        self.quit: bool = False
        self.start_btn: Button = Button(
            (self.width // 2, (self.height // 2)),
            "start".upper()
        )
        self.leaderboard_btn: Button = Button(
            (self.width // 2, (self.height // 2) + 80),
            "leaderboard".upper()
        )
        self.exit_btn: Button = Button(
            (self.width // 2, (self.height // 2) + 160),
            "exit".upper()
        )
        py.display.set_caption(self.caption_text)

    def draw(self, screen: py.Surface) -> None:
        screen.fill("black")
        screen.blit(self.heading, self.heading_rect)
        self.start_btn.draw(screen)
        self.exit_btn.draw(screen)
        self.leaderboard_btn.draw(screen)

        self.exit_btn.hover(py.mouse.get_pos())
        self.start_btn.hover(py.mouse.get_pos())
        self.leaderboard_btn.hover(py.mouse.get_pos())

    def update(self, dt: float, surface: py.Surface) -> None:
        pass

    def event_handler(self, events) -> None:
        for event in events:
            if self.exit_btn.clicked(event):
                self.quit = True
            if self.start_btn.clicked(event):
                self.next_screen = Screens.GAMESCREEN
            if self.leaderboard_btn.clicked(event):
                self.next_screen = Screens.LEADERBOARDSCREEN
