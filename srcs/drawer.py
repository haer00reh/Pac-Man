import pygame as py
from srcs.game import Game, Direction
from typing import Tuple, List
from srcs.objects import Ghost
from srcs.ghosts import Blinky, Inky, Clyde, Pinky


TOP = 1
RIGHT = 2
BOTTOM = 4
LEFT = 8
FORTY_TWO_TEMPLATE = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


class Drawer:
    def __init__(self, game: Game):
        self.game = game
        self.maze = game.maze
        self.maze_width = game.size[0]
        self.maze_height = game.size[1]
        self.blinky_img = py.image.load("assets/blinky.png")
        self.pinky_img = py.image.load("assets/pinky.png")
        self.inky_img = py.image.load("assets/inky.png")
        self.clyde_img = py.image.load("assets/clyde.png")
        self.pacman_img = py.image.load('assets/pacman_icon.png')
        self.pacman = self.get_pacman_image(self.pacman_img)

    def update(self, game: Game, surface: py.Surface):
        self.game = game
        self.maze = game.maze
        self.maze_width = game.size[0]
        self.maze_height = game.size[1]
        self.draw_maze(surface)

    def is_42_cell(self, x: int, y: int) -> bool:
        """Return True if cell (x, y) belongs to the centered '42' pattern."""
        grid = self.maze
        width = self.maze_width
        height = self.maze_height

        if not (0 <= y < height and 0 <= x < width):
            return False

        tmpl_h = len(FORTY_TWO_TEMPLATE)
        tmpl_w = len(FORTY_TWO_TEMPLATE[0])
        if height < tmpl_h * 2 or width < tmpl_w * 2:
            return False

        posx = (width - tmpl_w) // 2
        posy = (height - tmpl_h) // 2

        tx = x - posx
        ty = y - posy
        if 0 <= ty < tmpl_h and 0 <= tx < tmpl_w:
            return FORTY_TWO_TEMPLATE[ty][tx] == 1 and grid[y][x] == 15

        return False

    def _draw_wall_rect(
        self,
        surface: py.Surface,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str,
        thickness: int,
    ) -> None:
        """
            Draw a thick wall
            centered cleanly along the segment (x1, y1) -> (x2, y2).
        """
        half = thickness // 2
        if y1 == y2:
            # Horizontal wall
            left = min(x1, x2) - half
            top = y1 - half
            width = abs(x2 - x1) + thickness
            py.draw.rect(surface, color, py.Rect(left, top, width, thickness))
        elif x1 == x2:
            # Vertical wall
            left = x1 - half
            top = min(y1, y2) - half
            height = abs(y2 - y1) + thickness
            py.draw.rect(surface, color, py.Rect(left, top, thickness, height))

    def draw_42_cell(
        self,
        surface: py.Surface,
        x: int,
        y: int,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str = "gold",
        thickness: int = 8,
    ) -> None:
        """Draw a single '42' cell filled and walled in one unified color."""
        cell = self.maze[y][x]

        # Fill the interior of the '42' cell using the same color as its walls
        cell_rect = py.Rect(x1, y1, x2 - x1, y2 - y1)
        py.draw.rect(surface, color, cell_rect)

        if cell & TOP:
            self._draw_wall_rect(surface, x1, y1, x2, y1, color, thickness)
        if cell & RIGHT:
            self._draw_wall_rect(surface, x2, y1, x2, y2, color, thickness)
        if cell & BOTTOM:
            self._draw_wall_rect(surface, x1, y2, x2, y2, color, thickness)
        if cell & LEFT:
            self._draw_wall_rect(surface, x1, y1, x1, y2, color, thickness)

    def get_pacgums_pos(self, ll: list):
        return [(gum.x, gum.y) for gum in ll if gum.eaten is False]

    def draw_maze(
        self,
        surface: py.Surface,
        cell_size: int | None = None,
        min_cell_size: int = 32,
        max_cell_size: int = 72,
        top_margin: int = 60,
        bottom_margin: int = 30,
        side_margin: int = 40,
        wall_color: str = "royalblue",
        forty_two_color: str = "gold",
        thickness: int = 8,
    ) -> None:
        grid = self.maze
        width = self.maze_width
        height = self.maze_height
        if width <= 0 or height <= 0:
            return

        surf_w, surf_h = surface.get_size()
        avail_w = max(1, surf_w - 2 * side_margin)
        avail_h = max(1, surf_h - top_margin - bottom_margin)

        if cell_size is None:
            fit_size = min(avail_w // width, avail_h // height)
            cell_size = max(min_cell_size, min(max_cell_size, fit_size))

        maze_w = width * cell_size
        maze_h = height * cell_size

        offset_x = (surf_w - maze_w) // 2
        offset_y = top_margin + (avail_h - maze_h) // 2

        forty_two_cells: list[tuple[int, int, int, int, int, int]] = []

        # Pass 1: Draw all non-42 walls
        for y in range(height):
            for x in range(width):
                x1 = offset_x + x * cell_size
                y1 = offset_y + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if self.is_42_cell(x, y):
                    forty_two_cells.append((x, y, x1, y1, x2, y2))
                    continue

                cell = grid[y][x]
                if (cell & TOP) and not self.is_42_cell(x, y - 1):
                    self._draw_wall_rect(surface, x1, y1, x2, y1, wall_color,
                                         thickness)
                if (cell & RIGHT) and not self.is_42_cell(x + 1, y):
                    self._draw_wall_rect(surface, x2, y1, x2, y2, wall_color,
                                         thickness)
                if (cell & BOTTOM) and not self.is_42_cell(x, y + 1):
                    self._draw_wall_rect(surface, x1, y2, x2, y2, wall_color,
                                         thickness)
                if (cell & LEFT) and not self.is_42_cell(x - 1, y):
                    self._draw_wall_rect(surface, x1, y1, x1, y2, wall_color,
                                         thickness)

        for x, y, x1, y1, x2, y2 in forty_two_cells:
            self.draw_42_cell(
                surface,
                x,
                y,
                x1,
                y1,
                x2,
                y2,
                color=forty_two_color,
                thickness=thickness,
            )

        pacgums = self.get_pacgums_pos(self.game.state.pacgums)
        for x, y in pacgums:
            gumx = offset_x + x * cell_size + cell_size // 2
            gumy = offset_y + y * cell_size + cell_size // 2
            py.draw.circle(surface, 'white', (gumx, gumy), 3)
        superpacgums = self.get_pacgums_pos(self.game.state.super_pacgums)
        for x, y in superpacgums:
            gumx = offset_x + x * cell_size + cell_size // 2
            gumy = offset_y + y * cell_size + cell_size // 2
            py.draw.circle(surface, 'white', (gumx, gumy), 6)
            superpacgums = self.get_pacgums_pos(self.game.state.super_pacgums)
        # Draw Pacman and ghosts
        ghosts: List[Tuple[Ghost, py.Surface]] = self.get_ghosts_image()
        for gh in ghosts:
            rect = gh[1].get_rect()
            gh_x: float = (offset_x + gh[0].visual_x
                           * cell_size + cell_size // 2)
            gh_y: float = (offset_y + gh[0].visual_y
                           * cell_size + cell_size // 2)
            rect.center = (int(gh_x), int(gh_y))
            surface.blit(gh[1], rect)

        # Draw the pacgums
        pac_x, pac_y = ((self.game.state.pacman.visual_x,
                         self.game.state.pacman.visual_y)
                        if self.game.state.pacman
                        else (0, 0))
        cx = offset_x + pac_x * cell_size + cell_size // 2
        cy = offset_y + pac_y * cell_size + cell_size // 2
        icon, rect = self.update_direction()
        rect.center = (cx, cy)
        surface.blit(icon, rect)

    def get_pacman_image(self, img):
        sx = 40
        sy = 40
        if 20 > self.game.size[0] > 15:
            sx = 30
        elif self.game.size[0] >= 20:
            sx = 20
        if 20 > self.game.size[1] > 15:
            sy = 30
        elif self.game.size[1] >= 20:
            sy = 20
        return py.transform.scale(img, (sx, sy))

    def get_ghosts_image(self):
        ghosts = self.game.state.ghosts
        res = []
        img = None
        sx = 40
        sy = 40
        if 20 > self.game.size[0] > 15:
            sx = 30
        elif self.game.size[0] >= 20:
            sx = 20
        if 20 > self.game.size[1] > 15:
            sy = 30
        elif self.game.size[1] >= 20:
            sy = 20
        for gh in ghosts:
            if gh.state == 'dead':
                continue
            if isinstance(gh, Blinky):
                img = py.transform.scale(self.blinky_img, (sx, sy))
            if isinstance(gh, Clyde):
                img = py.transform.scale(self.clyde_img, (sx, sy))
            if isinstance(gh, Inky):
                img = py.transform.scale(self.inky_img, (sx, sy))
            if isinstance(gh, Pinky):
                img = py.transform.scale(self.pinky_img, (sx, sy))
            res.append((gh, img))
            img = None
        return res

    def update_direction(self):
        angle = 0
        if (self.game.next_direction is Direction.NORTH):
            angle = 90
        if (self.game.next_direction is Direction.SOUTH):
            angle = -90
        if (self.game.next_direction is Direction.EAST):
            angle = 0
        if (self.game.next_direction is Direction.WEST):
            angle = 180
        self.pacman = self.pacman = self.get_pacman_image(self.pacman_img)
        rotated_img = py.transform.rotate(self.pacman, angle=angle)
        new_rect = rotated_img.get_rect()
        return rotated_img, new_rect
