# 🧩 Maze Generator & Solver

A small command-line tool in plain Python that **generates** a random maze with depth-first search and **solves** it with breadth-first search. No dependencies.

```
+   +---+---+---+---+---+---+---+---+---+
| * |     *   *   *   *   * |     *   * |
+   +   +   +---+---+---+   +---+   +   +
| * |   | *   *   *   * | *   *   * | * |
+   +---+---+   +---+   +---+---+---+   +
| *   *   * |   | *   * |           | * |
+---+---+   +---+   +---+   +   +---+   +
|       | *   *   * |       |   | *   * |
+   +---+---+---+---+   +---+---+   +---+
|                                 *   * |
+---+---+---+---+---+---+---+---+---+   +
Seed 3 | shortest path: 30 cells
```

## Usage

Requires Python 3.10+.

```bash
python maze.py                                # 12 x 24 maze with its solution
python maze.py --rows 8 --cols 16 --seed 42   # same seed = same maze
python maze.py --no-solve                     # just the maze
```

Rows and columns can be 2–100.

## How it works

The maze is stored as a **graph**: each cell maps to the set of neighbouring cells it has an open passage to.

**Generating: randomized depth-first search**

1. Start at the top-left cell and push it on a stack.
2. Look at the cell on top of the stack. If it has unvisited neighbours, pick one at random, knock down the wall between them, and push it.
3. If it has none, pop it (backtrack).
4. Repeat until the stack is empty.

Every cell is visited exactly once, so the result is a **perfect maze**: a spanning tree with exactly one path between any two cells. DFS makes long, winding corridors.

**Solving: breadth-first search**

BFS explores cells in order of distance from the start, using a queue. The first time it reaches the exit, it has found the **shortest** path. It remembers how it reached each cell (`came_from`) and walks those breadcrumbs back to rebuild the path.

## Project structure

| File           | Purpose                                 |
|----------------|-----------------------------------------|
| `maze.py`      | Generator, solver, ASCII renderer, CLI  |
| `test_maze.py` | Unit tests                              |

## Run the tests

```bash
python -m unittest -v
```

The tests check that passages are two-way and only join adjacent cells, that the maze is a perfect spanning tree (every cell reachable, exactly `cells - 1` passages), that the solved path is connected from entrance to exit, and that the same seed gives the same maze.

## License

[MIT](LICENSE)
