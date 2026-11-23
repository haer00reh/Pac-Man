from typing import Tuple
import pygame as py
from srcs.screens.screen import Font


class Button:
    def __init__(
        self,
        coordinate: Tuple[int, int],
        text: str,
        w: int = 300,
        h: int = 70
    ):
        self.text = text
        self.w = w
        self.h = h

        self.rect = py.Rect(0, 0, w, h)
        self.rect.center = coordinate

        self.border_color = py.Color("#52649B")
        self.hover_border = py.Color("#38DDF8")

        self.text_color = py.Color("#C8CAD1")
        self.hover_text = py.Color("#FADB2E")

        self.fill_color = (15, 30, 85, 35)
        self.hover_fill = (20, 100, 180, 100)

        self.current_color = self.border_color
        self.current_text = self.text_color

        self.progress = 0.0
        self.is_hovered = False

        self.font = Font.H1.value
        self.label = self.font.render(
            self.text, True, self.current_text
        )

    def hover(self, mouse_pos):
        if not (self.rect.collidepoint(mouse_pos) or self.is_hovered):
            return self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.update(1)
        else:
            self.update(1)
        return self.is_hovered

    def update(self, dt):
        target = 1.0 if self.is_hovered else 0.0

        factor = 1 - pow(0.001, dt)

        self.progress += (
            target - self.progress
        ) * factor

        self.current_color = self.border_color.lerp(
            self.hover_border,
            self.progress
        )

        self.current_text = self.text_color.lerp(
            self.hover_text,
            self.progress
        )
        self.label = self.font.render(
            self.text, True, self.current_text

        )

    def draw(self, screen):
        t = self.progress

        glass = py.Surface(
            self.rect.size,
            py.SRCALPHA
        )

        fill = tuple(
            int(a + (b - a) * t)
            for a, b in zip(self.fill_color, self.hover_fill)
        )

        py.draw.rect(
            glass,
            fill,
            glass.get_rect(),
            border_radius=12
        )

        screen.blit(glass, self.rect.topleft)

        py.draw.rect(
            screen,
            self.current_color,
            self.rect,
            width=2,
            border_radius=12
        )

        label_rect = self.label.get_rect(
            center=self.rect.center
        )

        shadow = self.font.render(
            self.text, True, (0, 0, 25)
        )

        screen.blit(
            shadow,
            (label_rect.x + 1, label_rect.y + 2)
        )

        screen.blit(self.label, label_rect)

    def clicked(self, e):
        return (
            e.type == py.MOUSEBUTTONDOWN
            and e.button == 1
            and self.rect.collidepoint(e.pos)
        )
