from srcs.objects import Ghost


class Blinky(Ghost):
    def get_target(self, blinky: Ghost | None = None) -> tuple[int, int]:
        return self.pacman.x, self.pacman.y


class Pinky(Ghost):
    def get_target(self, blinky: Ghost | None = None) -> tuple[int, int]:
        return self.get_ahead_position(4)


class Inky(Ghost):
    def get_target(self, blinky: Ghost | None = None) -> tuple[int, int]:
        ax, ay = self.get_ahead_position(2)
        if blinky is None:
            return self.pacman.x, self.pacman.y
        return 2 * ax - blinky.x, 2 * ay - blinky.y


class Clyde(Ghost):
    def get_target(self, blinky: Ghost | None = None) -> tuple[int, int]:
        distance = ((self.pacman.x - self.x) ** 2
                    + (self.pacman.y - self.y) ** 2) ** 0.5
        if distance < 8:
            return self.start_x, self.start_y
        return self.pacman.x, self.pacman.y
