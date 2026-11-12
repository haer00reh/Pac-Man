from mazegenerator import MazeGenerator
from config import Config

if __name__ == "__main__":
    configs = Config(file_path="config.json")
    configs.extract()
    configs.init()
