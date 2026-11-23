import pygame as py
from srcs.screens.menuScreen import MenuScreen
from srcs.screens.screen import Screens, Displays
from srcs.screens.gameoverScreen import GameOverScreen
from srcs.screens.gameScreen import GameScreen
from srcs.screens.leaderboardScreen import LeaderboardScreen

class GUI:
    def __init__(self):
        py.init()

        displays = py.display.get_desktop_sizes()
        screen_width, screen_height = displays[0]
        width = 1000 if screen_width <= 1600 else 1300
        height = 750 if screen_height <= 900 else 900
        self.screen = py.display.set_mode((width, height))

        self.display = Displays.SMALL 

        
        self.icon = py.image.load("assets/icon.png")
        self.running = True
        current_screen = MenuScreen(self.display)
        clock = py.time.Clock()
        

        while self.running:
            events = py.event.get()
            py.display.set_icon(self.icon)
            dt = clock.tick(60) / 1000.0

            for event in events:
                if event.type == py.QUIT:
                    self.running = False
            current_screen.event_handler(events)
            current_screen.update(dt)

            current_screen.draw(self.screen)
            if current_screen.next_screen is not Screens.NONE:
                if current_screen.next_screen == Screens.MENUSCREEN:
                    current_screen = MenuScreen(self.display)
                elif current_screen.next_screen == Screens.GAMESCREEN:
                    current_screen = GameScreen(self.display)
                elif current_screen.next_screen == Screens.LEADERBOARDSCREEN:
                    current_screen = LeaderboardScreen(self.display)
                elif current_screen.next_screen == Screens.GAMEOVERSCREEN:
                    current_screen = GameOverScreen(self.display)
                current_screen.next_screen = None
            if (current_screen.quit):
                break

            py.display.update()

        py.quit()

    def quite(self, e):
        return e.type == py.QUIT
