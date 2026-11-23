from srcs.screens.screen import Screen, Screens, Font
from srcs.drawer import Drawer
import pygame as py
from srcs.game import Game
import sys
from srcs.game import Directions

class GameScreen(Screen):
    def __init__(self, display):
        self.next_screen = Screens.NONE
        self.quit = False
        self.game = Game()
        self.game.setup(sys.argv[1] if len(sys.argv) > 1 else "config.json")
        self.w, self.h = py.display.get_window_size()
        self.caption_text = "Game Screen"
        pac_icon = py.image.load('assets/pacman_icon.png')
        sx = 40
        sy = 40
        if 20 > self.game.size[0] >= 15:
            sx = 30
        elif self.game.size[0] >= 20:
            sx = 20
        if 20 > self.game.size[1] >= 15:
            sy = 30
        elif self.game.size[1] >= 20:
            sy = 20
        self.pacman_icon = py.transform.scale(pac_icon, (sx, sy))
        self.drawer = Drawer(self.game, self.pacman_icon)

    def get_score(self):
        return (Font.H2.value.render(
            f"SCORE :  {self.game.state.score}",
            True,
            'yellow'
          ))

    def get_timer(self):
         return (Font.H2.value.render(
              f"TIMER :  {self.game.config.time_limit}",
              True,
              'yellow'
         ))

    def get_level(self):
         return (Font.H2.value.render(
              f"LEVEL  :  {self.game.level_index + 1}",
              True,
              'yellow'
         ))

    def get_lives(self):
         return (Font.H2.value.render(
              f"LIVES  :  {self.game.state.lives}",
              True,
              'yellow'
         ))
    
    def draw(self, screen):
        py.display.set_caption(self.caption_text)
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

    def update(self, dt):
         self.game.update(dt)

    def event_handler(self, events):
          for e in events:
               if e.type == py.KEYDOWN:
                    if e.key == py.K_LEFT:
                         self.game.set_direction(Directions.WEST)
                    elif e.key == py.K_RIGHT:
                         self.game.set_direction(Directions.EAST)
                    elif e.key == py.K_UP:
                         self.game.set_direction(Directions.NORTH)
                    elif e.key == py.K_DOWN:
                         self.game.set_direction(Directions.SOUTH)
