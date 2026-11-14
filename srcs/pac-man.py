from mazegenerator import MazeGenerator
from config import Config, GameState, Game

if __name__ == "__main__":
    configs = Config(file_path="config.json")
    configs.extract()
    m = MazeGenerator(seed=42)
    print(m.maze)

