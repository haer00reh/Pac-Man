from srcs.screens.screen import Screen, Screens, Font
import pygame as py

class LeaderboardScreen(Screen):
    def __init__(self, display):
        self.next_screen: Screens = Screens.NONE
        self.caption_text = "Leaderboard Screen"
        self.heading = Font.S1.value.render("Leaderboard Screen", True, (255, 255, 255))
        self.quit = False
    
    def draw(self, screen):
        py.display.set_caption(self.caption_text)
        screen.fill((0, 0, 0))
        screen.blit(self.heading, (50, 50))

    def update(self, dt):
        pass

    def event_handler(self, events):
        pass

