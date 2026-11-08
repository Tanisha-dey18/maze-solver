"""Generate a random maze with depth-first search, then solve it with breadth-first search.

Usage:
    python maze.py                      # 12 x 24 maze, solved
    python maze.py --rows 8 --cols 16 --seed 42
    python maze.py --no-solve
"""

import argparse
import random
from collections import deque

Cell = tuple[int, int]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right


def neighbours(cell: Cell, rows: int, cols: int) -> list[Cell]:
    r, c = cell
    return [(r + dr, c + dc) for dr, dc in DIRECTIONS if 0 <= r + dr < rows and 0 <= c + dc < cols]


def generate(rows: int, cols: int, rng: random.Random) -> dict[Cell, set[Cell]]:
    """Returns the maze as a graph: each cell maps to the cells it has an open passage to.

    Uses randomized depth-first search with an explicit stack: walk to a random unvisited
    neighbour, knocking down the wall between; when stuck, back up. Every cell gets visited
    exactly once, so the result is a "perfect" maze: exactly one path between any two cells.
    """
    passages: dict[Cell, set[Cell]] = {(r, c): set() for r in range(rows) for c in range(cols)}
    start = (0, 0)
    visited = {start}
    stack = [start]
    while stack:
        cell = stack[-1]
        unvisited = [n for n in neighbours(cell, rows, cols) if n not in visited]
        if not unvisited:
            stack.pop()  # dead end: backtrack
            continue
        nxt = rng.choice(unvisited)
        passages[cell].add(nxt)
        passages[nxt].add(cell)
        visited.add(nxt)
        stack.append(nxt)
    return passages


def solve(passages: dict[Cell, set[Cell]], start: Cell, goal: Cell) -> list[Cell] | None:
    """Breadth-first search. Returns the shortest path from start to goal, or None."""
    came_from: dict[Cell, Cell | None] = {start: None}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell == goal:
            path = []
            while cell is not None:  # walk the breadcrumbs back to the start
                path.append(cell)
                cell = came_from[cell]
            return path[::-1]
        for nxt in passages[cell]:
            if nxt not in came_from:
                came_from[nxt] = cell
                queue.append(nxt)
    return None


def render(passages: dict[Cell, set[Cell]], rows: int, cols: int, path: list[Cell] | None = None) -> str:
    """Draws the maze with ASCII characters; the path, if given, is shown with asterisks."""
    on_path = set(path or [])
    lines = ["+" + "---+" * cols]
    for r in range(rows):
        row = "|"
        floor = "+"
        for c in range(cols):
            row += " * " if (r, c) in on_path else "   "
            row += " " if (r, c + 1) in passages[(r, c)] else "|"
            floor += "   +" if (r + 1, c) in passages[(r, c)] else "---+"
        lines.append(row)
        lines.append(floor)
    # Openings: entrance at the top-left, exit at the bottom-right
    lines[0] = "+   " + lines[0][4:]
    lines[-1] = lines[-1][:-4] + "   +"
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and solve a random maze.")
    parser.add_argument("--rows", type=int, default=12)
    parser.add_argument("--cols", type=int, default=24)
    parser.add_argument("--seed", type=int, help="same seed = same maze")
    parser.add_argument("--no-solve", action="store_true", help="print the maze without the solution")
    args = parser.parse_args()
    if not (2 <= args.rows <= 100 and 2 <= args.cols <= 100):
        parser.error("rows and cols must be between 2 and 100")

    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    passages = generate(args.rows, args.cols, random.Random(seed))
    goal = (args.rows - 1, args.cols - 1)
    path = None if args.no_solve else solve(passages, (0, 0), goal)

    print(render(passages, args.rows, args.cols, path))
    summary = f"Seed {seed}"
    if path:
        summary += f" | shortest path: {len(path)} cells"
    print(summary)


if __name__ == "__main__":
    main()
