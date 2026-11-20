import sys
import random
from typing import Any
from game import Game


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <config.json>", file=sys.stderr)
        sys.exit(1)

    game = Game()
    game.config.file_path = sys.argv[1]
    game.config.extract()
    random.seed(game.config.seed)

    game.load_level(1)
    game.collect_valid_positions()
    game.init_positions()

    test_game(game)


if __name__ == "__main__":
    main()