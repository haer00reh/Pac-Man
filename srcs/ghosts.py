from objects import Ghost, Pacman

class Clyde(Ghost):
    def chase(self, pacman: Pacman):
        pass


class Blinky(Ghost):
    def chase(self, pacman: Pacman):
        self.x, self.y = self.move(pacman.x, pacman.y)


class Inky(Ghost):
    def chase(self, pacman: Pacman):
        pass


class Pinky(Ghost):
    def chase(self, pacman: Pacman):
        directions = {
            "north": (0, -4),
            "east": (4, 0),
            "south": (0, 4),
            "west": (-4, 0)
        }

        dx, dy = directions[pacman.direction]
        self.x, self.y = self.move(pacman.x + dx, pacman.y + dy)

    