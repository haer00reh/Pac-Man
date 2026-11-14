from mazegenerator import MazeGenerator
from config import Config, GameState

if __name__ == "__main__":
    configs = Config(file_path="config.json")
    configs.extract()
    state = GameState()
    state.init(configs)
