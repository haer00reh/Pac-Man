
from srcs.screens.screen import Screen, Screens, Displays
import pygame as py
from srcs.button import Button


class MenuScreen(Screen):
    def __init__(self, display: Displays = Displays.LARGE):
        self.next_screen: Screens = Screens.NONE
        self.caption_text = "Menu"
        self.width, self.height = py.display.get_surface().get_size()
        self.image = py.image.load("assets/pacman_heading.png")
        self.heading = py.transform.scale(self.image, (self.width - 100, (self.height // 2)))
        self.heading_rect = self.heading.get_rect(center=(self.width // 2, 200))
        self.quit = False
        self.start_btn = Button(
            (self.width // 2, (self.height // 2)),
            "start".upper()
        )
        self.leaderboard_btn = Button(
            (self.width // 2, (self.height // 2) + 80),
            "leaderboard".upper()
        )
        self.exit_btn = Button(
            (self.width // 2, (self.height // 2) + 160),
            "exit".upper()
        )
        # bg_image = py.image.load("assets/bg_home.jpg")
        # self.bg_image = py.transform.scale(bg_image, (self.width, self.height))

    def draw(self, screen):
        py.display.set_caption(self.caption_text)
        screen.blit(self.heading, self.heading_rect)
        self.start_btn.draw(screen)
        self.exit_btn.draw(screen)
        self.leaderboard_btn.draw(screen)

        self.exit_btn.hover(py.mouse.get_pos())
        self.start_btn.hover(py.mouse.get_pos())
        self.leaderboard_btn.hover(py.mouse.get_pos())


    def update(self, dt):
        pass

    def event_handler(self, events):
        for event in events:
            if self.exit_btn.clicked(event):
                self.quit = True
            if self.start_btn.clicked(event):
                self.next_screen = Screens.GAMESCREEN
            if self.leaderboard_btn.clicked(event):
                self.next_screen = Screens.LEADERBOARDSCREEN