#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import random


class Game:
    def __init__(self, board=None, score=0):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]] if board is not None else board
        self.score = score

    def __str__(self):
        raise NotImplementedError

    def add_new_tile(self):
        t_val = 2 if random() < 0.9 else 4

    def avlbl_spaces(self):
        row_index = []
        for r_index, row in enumerate(self.board):
            for e_index, elem in enumerate(row):
                if not elem:
                    row_index.append((row_index, e_index))
        return 
