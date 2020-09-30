#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import random, shuffle
import numpy as np
import tkinter as tk

BOARD_SIZE = 4


class Game:
    def __init__(self, board=None, score=0):
        if board:
            self.board = np.array(board)
        else:
            self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype='int32')
            self.add_new_tile()
            self.add_new_tile()
        self.score = score

    def __str__(self):
        raise NotImplementedError

    def add_new_tile(self):
        t_val = 2 if random() < 0.9 else 4
        pick_from = self.avlbl_spaces()
        if pick_from:
            shuffle(pick_from)
            insert_rand = pick_from[0]
            self.board[insert_rand] = t_val
        else:
            print("Game over.")
            return 0

    def avlbl_spaces(self):
        tup_irow_index = []
        for r_index, row in enumerate(self.board):
            for e_index, elem in enumerate(row):
                if not elem:
                    tup_irow_index.append((r_index, e_index))
        return tup_irow_index

    def swipe_left(self):
        old_board = self.board.copy()
        for i in range(BOARD_SIZE):
            n_row = [elem for elem in self.board[i, :] if elem]
            n_row = self.add_tiles(n_row)
            self.board[i, :] = n_row + (BOARD_SIZE - len(n_row)) * [0]
        if (old_board != self.board).any():
            self.add_new_tile()

    def swipe_right(self):
        old_board = self.board.copy()
        for i in range(BOARD_SIZE):
            n_row = [elem for elem in self.board[i, :] if elem]
            n_row = self.add_tiles(n_row)
            self.board[i, :] = (BOARD_SIZE - len(n_row)) * [0] + n_row
        if (old_board != self.board).any():
            self.add_new_tile()

    def swipe_up(self):
        old_board = self.board.copy()
        for i in range(BOARD_SIZE):
            n_col = [elem for elem in self.board[:, i] if elem]
            n_col = self.add_tiles(n_col)
            self.board[:, i] = n_col + (BOARD_SIZE - len(n_col)) * [0]
        if (old_board != self.board).any():
            self.add_new_tile()

    def swipe_down(self):
        old_board = self.board.copy()
        for i in range(BOARD_SIZE):
            n_col = [elem for elem in self.board[:, i] if elem]
            n_col = self.add_tiles(n_col)
            self.board[:, i] = (BOARD_SIZE - len(n_col)) * [0] + n_col
        if (old_board != self.board).any():
            self.add_new_tile()

    #
    #   To add_tiles pass row or column at the time, not the whole board!
    #   It's not pretty. I know. "It just works".
    #

    def add_tiles(self, cl: list):
        for index, elem in enumerate(cl):
            if index < len(cl) - 1 and cl[index] == cl[index + 1]:
                cl[index] = elem * 2
                self.score += elem * 2
                cl.pop(index + 1)
            else:
                cl[index] = elem
        return cl


class Interface:
    def __init__(self):
        self.game = Game()
        self.root = tk.Tk()

    def v_col(self, value):
        value_to_colour = {0: "#ffffff",
                           2: "#eee4da",
                           4: "#ede0c8",
                           8: "#f2b179",
                           16: "#f67c5f",
                           32: "#f65e3b",
                           64: "#f65e3b",
                           128: "#edcf72",
                           256: "#edcc61",
                           512: "#edc850",
                           1024: "#edc53f",
                           2048: "#edc22e",
                           }
        return value_to_colour[value] if value in value_to_colour.keys() else "#FE7F9C"

    def create_grid(self):
        self.root.title("2048 v1.0 by MikiSpoko200")

        # Def Lables

        b = self.game.board
        r = self.root
        size = 3
        pink = "#FE7F9C"
        score = tk.Label(r, text=f"Score {self.game.score}", padx=size, pady=size, fg="#000000", bg=pink, borderwidth=4,
                         relief="groove",
                         font=("Helvetica", 18), width=20, height=2)
        L1 = tk.Label(r, text=f"{b[0, 0]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[0, 0]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L2 = tk.Label(r, text=f"{b[0, 1]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[0, 1]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L3 = tk.Label(r, text=f"{b[0, 2]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[0, 2]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L4 = tk.Label(r, text=f"{b[0, 3]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[0, 3]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L5 = tk.Label(r, text=f"{b[1, 0]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[1, 0]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L6 = tk.Label(r, text=f"{b[1, 1]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[1, 1]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L7 = tk.Label(r, text=f"{b[1, 2]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[1, 2]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L8 = tk.Label(r, text=f"{b[1, 3]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[1, 3]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L9 = tk.Label(r, text=f"{b[2, 0]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[2, 0]), borderwidth=4,
                      relief="groove",
                      font=("Helvetica", 18), width=4, height=2)
        L10 = tk.Label(r, text=f"{b[2, 1]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[2, 1]), borderwidth=4,
                       relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L11 = tk.Label(r, text=f"{b[2, 2]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[2, 2]), borderwidth=4,
                       relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L12 = tk.Label(r, text=f"{b[2, 3]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[2, 3]), borderwidth=4,
                       relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L13 = tk.Label(r, text=f"{b[3, 0]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[3, 0]), borderwidth=4,
                       relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L14 = tk.Label(r, text=f"{b[3, 1]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[3, 1]), borderwidth=4,
                       relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L15 = tk.Label(r, text=f"{b[3, 2]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[3, 2]), borderwidth=4,
                       relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L16 = tk.Label(r, text=f"{b[3, 3]}", padx=size, pady=size, fg="#000000", bg=self.v_col(b[3, 3]), borderwidth=4,
                       relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L17 = tk.Label(r, text=f" ", padx=size, pady=size, fg="#000000", bg="#ffffff", borderwidth=4, relief="groove",
                       font=("Helvetica", 18), width=4, height=2)
        L18 = tk.Label(r, text=f" ", padx=size, pady=size, fg="#000000", bg="#ffffff", borderwidth=4, relief="groove",
                       font=("Helvetica", 18), width=4, height=2)

        # Put Lables on the screen

        score.grid(row=0, column=0, columnspan=4)

        L1.grid(row=1, column=0)
        L2.grid(row=1, column=1)
        L3.grid(row=1, column=2)
        L4.grid(row=1, column=3)

        L5.grid(row=2, column=0)
        L6.grid(row=2, column=1)
        L7.grid(row=2, column=2)
        L8.grid(row=2, column=3)

        L9.grid(row=3, column=0)
        L10.grid(row=3, column=1)
        L11.grid(row=3, column=2)
        L12.grid(row=3, column=3)

        L13.grid(row=4, column=0)
        L14.grid(row=4, column=1)
        L15.grid(row=4, column=2)
        L16.grid(row=4, column=3)

        L17.grid(row=5, column=0)
        L18.grid(row=5, column=2)

        self.labels = ([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13, L14, L15, L16], score)

        # Create buttons

        B1 = tk.Button(self.root, text="Up", command=lambda: [self.game.swipe_up(), self.update_labels()], padx=size, pady=size, fg="#000000",
                       bg="#ffffff", borderwidth=4, relief="groove", font=("Helvetica", 18), width=4, height=2)
        B2 = tk.Button(self.root, text="Left", command=lambda: [self.game.swipe_left(), self.update_labels()], padx=size, pady=size, fg="#000000",
                       bg="#ffffff", borderwidth=4, relief="groove", font=("Helvetica", 18), width=4, height=2)
        B4 = tk.Button(self.root, text="Right", command=lambda: [self.game.swipe_right(), self.update_labels()], padx=size, pady=size, fg="#000000",
                       bg="#ffffff", borderwidth=4, relief="groove", font=("Helvetica", 18), width=4, height=2)
        B3 = tk.Button(self.root, text="Down", command=lambda: [self.game.swipe_down(), self.update_labels()], padx=size, pady=size, fg="#000000",
                       bg="#ffffff", borderwidth=4, relief="groove", font=("Helvetica", 18), width=4, height=2)

        B1.grid(row=5, column=1)
        B2.grid(row=6, column=0)
        B3.grid(row=6, column=1)
        B4.grid(row=6, column=2)

        self.root.mainloop()


    def update_labels(self):
        labels, score = self.labels
        if str(self.game.score) != score["text"]:
            score["text"] = f"score : {self.game.score}"
        brd_to_list = []
        for row in self.game.board:
            for elem in row:
                brd_to_list.append(elem)
        for f_val, label in zip(brd_to_list, labels):
            if str(f_val) != label["text"]:
                label.config(text=f"{f_val}", bg=self.v_col(f_val))


def main():
    inter = Interface()
    inter.create_grid()

if __name__ == "__main__":
    main()
