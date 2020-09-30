#!/usr/bin/python
# -*- coding: utf-8 -*-


import unittest
from TwentyFortyEight.engine import Game
import numpy as np


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game([[0, 2, 0, 0],
                          [4, 2, 0, 0],
                          [0, 0, 2, 2],
                          [0, 0, 2, 0]])

    def test_swipe_up(self):
        self.game.swpie_up()
        self.assertTrue((self.game.board == np.array([[4, 4, 4, 2],
                                                      [0, 0, 0, 0],
                                                      [0, 0, 0, 0],
                                                      [0, 0, 0, 0]])).all())
        self.assertEqual(self.game.score, 8)

    def test_swipe_down(self):
        self.game.swipe_down()
        self.assertTrue((self.game.board == np.array([[0, 0, 0, 0],
                                                      [0, 0, 0, 0],
                                                      [0, 0, 0, 0],
                                                      [4, 4, 4, 2]])).all())
        self.assertEqual(self.game.score, 8)

    def test_swipe_left(self):
        self.game.swpie_left()
        self.assertTrue((self.game.board == np.array([[2, 0, 0, 0],
                                                      [4, 2, 0, 0],
                                                      [4, 0, 0, 0],
                                                      [2, 0, 0, 0]])).all())
        self.assertEqual(self.game.score, 4)

    def test_swipe_right(self):
        self.game.swpie_right()
        self.assertTrue((self.game.board == np.array([[0, 0, 0, 2],
                                                      [0, 0, 4, 2],
                                                      [0, 0, 0, 4],
                                                      [0, 0, 0, 2]])).all())
        self.assertEqual(self.game.score, 4)

    def test_add_tiles(self):
        self.assertTrue(([4, 4] == self.game.add_tiles([2, 2, 4])))

    def test_avlbl_spaces(self):
        self.assertTrue(([(0, 0), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0), (2, 1), (3, 0),
                          (3, 1), (3, 3)] == self.game.avlbl_spaces()))


def main():
    tests = TestGame()
    tests.test_swipe_down()
    tests.test_swipe_up()
    tests.test_swipe_right()
    tests.test_swipe_left()
    tests.test_add_tiles()
    tests.test_avlbl_spaces()


if __name__ == "__main__":
    unittest.main()
