import sys
import random
from typing import Any
from game import Game


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <config.json>", file=sys.stderr)
        sys.exit(1)

    game = Game()
    game.setup(sys.argv[1])


if __name__ == "__main__":
    main()