import sys
import random
from typing import Any
from config import Game

# def fmt(obj: Any) -> str:
#     """One-line 'key=value' dump of any pydantic model (or plain object)."""
#     data = obj.model_dump() if hasattr(obj, "model_dump") else vars(obj)
#     return ", ".join(f"{k}={v!r}" for k, v in data.items())


# def test_game(game: Game) -> None:
#     line = "=" * 50
#     print(line)
#     print(" GAME STATE TEST")
#     print(line)

#     # config
#     cfg = game.config
#     print("\n[CONFIG]")
#     for name in ("time_limit", "seed", "point_per_gum",
#                  "point_per_sgum", "point_per_ghost"):
#         print(f"  {name:<16}: {getattr(cfg, name)}")

#     # maze
#     print("\n[MAZE]")
#     print(f"  size            : {len(game.maze[0])} x {len(game.maze)}")
#     print(f"  valid positions : {len(game.valid_positions)}")

#     # pacman
#     print("\n[PACMAN]")
#     pac = game.state.pacman
#     if pac:
#         print(f"  pos : ({pac.x}, {pac.y})")
#         print(f"  all : {fmt(pac)}")
#     else:
#         print("  not initialized")

#     # ghosts
#     print(f"\n[GHOSTS] ({len(game.state.ghosts)})")
#     for g in game.state.ghosts:
#         print(f"  {type(g).__name__:<7} pos=({g.x}, {g.y})  |  {fmt(g)}")

#     # pacgums
#     gums = game.state.pacgums
#     print(f"\n[PACGUMS] ({len(gums)})")
#     for i, p in enumerate(gums):
#         print(f"  #{i:<3} pos=({p.x}, {p.y})  |  {fmt(p)}")

#     # sanity checks
#     print("\n[CHECKS]")
#     all_pos = [(o.x, o.y) for o in game.state.ghosts + gums]
#     if pac:
#         all_pos.append((pac.x, pac.y))
#     print(f"  all on valid cells : {all(p in game.valid_positions for p in all_pos)}")
#     gum_pos = [(p.x, p.y) for p in gums]
#     print(f"  no duplicate gums  : {len(gum_pos) == len(set(gum_pos))}")
#     print(line)


# def main() -> None:
#     if len(sys.argv) != 2:
#         print("Usage: python main.py <config.json>", file=sys.stderr)
#         sys.exit(1)

#     game = Game()
#     game.config.file_path = sys.argv[1]
#     game.config.extract()
#     random.seed(game.config.seed)

#     game.load_level(1)
#     game.validate_positions()
#     game.init_positions()

#     test_game(game)


if __name__ == "__main__":
    main()