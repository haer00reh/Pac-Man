from srcs.screens.screen import Screen, Screens
import pygame as py

class GameOverScreen(Screen):
    def __init__(self, font):
        self.next_screen: Screens = None
        self.font = font
        self.caption_text = "Game Over"
        self.static_text = "Press 1: Start Game | Press 2: Leaderboard"
    
    def draw(self, screen):
        py.display.set_caption(self.caption_text)
        screen.fill((0, 0, 0))
        self.font.render_to(screen, (50, 50), self.caption_text, (255, 255, 255))


    def update(self, dt):
        pass

    def event_handler(self, events):
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_1:
                    self.next_screen = Screens.GAMESCREEN
                elif event.key == py.K_2:
                    self.next_screen = Screens.LEADERBOARDSCREEN
                elif event.key == py.K_3:
                    self.next_screen = Screens.GAMEOVERSCREEN
                elif event.key == py.K_RETURN:
                    self.next_screen = Screens.MENUSCREEN

