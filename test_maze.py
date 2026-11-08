"""Run with: python -m unittest -v"""

import random
import unittest

from maze import generate, render, solve


class TestMaze(unittest.TestCase):
    def setUp(self):
        self.rows, self.cols = 10, 15
        self.passages = generate(self.rows, self.cols, random.Random(7))

    def test_passages_are_two_way(self):
        for cell, links in self.passages.items():
            for other in links:
                self.assertIn(cell, self.passages[other])

    def test_passages_only_join_adjacent_cells(self):
        for (r, c), links in self.passages.items():
            for (r2, c2) in links:
                self.assertEqual(abs(r - r2) + abs(c - c2), 1)

    def test_maze_is_perfect(self):
        # A perfect maze is a spanning tree: every cell reachable and exactly cells - 1 passages
        edges = sum(len(links) for links in self.passages.values()) // 2
        self.assertEqual(edges, self.rows * self.cols - 1)
        for cell in self.passages:
            self.assertIsNotNone(solve(self.passages, (0, 0), cell))

    def test_path_is_connected_and_ends_correctly(self):
        goal = (self.rows - 1, self.cols - 1)
        path = solve(self.passages, (0, 0), goal)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], goal)
        for a, b in zip(path, path[1:]):
            self.assertIn(b, self.passages[a])

    def test_unreachable_goal_returns_none(self):
        walled = {(0, 0): set(), (0, 1): set()}
        self.assertIsNone(solve(walled, (0, 0), (0, 1)))

    def test_same_seed_gives_same_maze(self):
        again = generate(self.rows, self.cols, random.Random(7))
        self.assertEqual(again, self.passages)

    def test_render_size(self):
        lines = render(self.passages, self.rows, self.cols).splitlines()
        self.assertEqual(len(lines), 2 * self.rows + 1)
        self.assertTrue(all(len(line) == 4 * self.cols + 1 for line in lines))


if __name__ == "__main__":
    unittest.main()
