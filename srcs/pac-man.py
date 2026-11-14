from mazegenerator import MazeGenerator
from config import Config, GameState, Game

if __name__ == "__main__":
    configs = Config(file_path="config.json")
    configs.extract()
    state = GameState()
    m = MazeGenerator(seed=42)
    g = Game(config=configs, state=state)
    print(m.maze)
    print("\n\n\n")
    g.validate_positions(m.maze)
    print(g.valid_positions)
