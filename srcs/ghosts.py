from objects import Ghost, Pacman

class Clyde(Ghost):

    def get_clyde_target(self):
        distance = ((self.pacman.x - self.x) ** 2 + (self.pacman.y - self.y) ** 2) ** 0.5
        if distance < 8:
            return self.start_x, self.start_y
        return self.pacman.x, self.pacman.y

    def chase(self):
        target_x, target_y = self.get_clyde_target()
        self.x, self.y = self.move(target_x, target_y)



class Blinky(Ghost):
    def chase(self, pacman: Pacman):
        self.x, self.y = self.move(pacman.x, pacman.y)


class Inky(Ghost):
    def get_inky_target(self, blinky: Ghost):
        target = self.get_ahead_position(self.pacman, 2)
        target_x = 2 * target[0] - blinky.x
        target_y = 2 * target[1] - blinky.y
        return target_x, target_y

    def chase(self, blinky: Ghost):
        target_x, target_y = self.get_inky_target(blinky)
        self.x, self.y = self.move(target_x, target_y)


class Pinky(Ghost):
    def chase(self):
        target = self.get_ahead_position(self.pacman, 4)
        self.x, self.y = self.move(target[0], target[1])