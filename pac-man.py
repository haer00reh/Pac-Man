import sys
from srcs.game import Game
from srcs.gui import GUI

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <config.json>", file=sys.stderr)
        sys.exit(1)
    display = GUI()



if __name__ == "__main__":
    main()