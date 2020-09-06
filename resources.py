#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU ZAPISANE SĄ WSZYSTKIE PODSTAWOWE WARTOŚCI
#

DEFAULT_DECK_NA = [('2', 2, 'Diamond'), ('3', 3, 'Diamond'), ('4', 4, 'Diamond'),
                         ('5', 5, 'Diamond'), ('6', 6, 'Diamond'), ('7', 7, 'Diamond'), ('8', 8, 'Diamond'),
                         ('9', 9, 'Diamond'), ('10', 10, 'Diamond'), ('Jack', 10, 'Diamond'),
                         ('Queen', 10, 'Diamond'), ('King', 10, 'Diamond'),
                         ('2', 2, 'Spade'), ('3', 3, 'Spade'), ('4', 4, 'Spade'), ('5', 5, 'Spade'),
                         ('6', 6, 'Spade'), ('7', 7, 'Spade'), ('8', 8, 'Spade'), ('9', 9, 'Spade'),
                         ('10', 10, 'Spade'), ('Jack', 10, 'Spade'), ('Queen', 10, 'Spade'), ('King', 10, 'Spade'),
                         ('2', 2, 'Club'), ('3', 3, 'Club'), ('4', 4, 'Club'),
                         ('5', 5, 'Club'), ('6', 6, 'Club'), ('7', 7, 'Club'), ('8', 8, 'Club'),
                         ('9', 9, 'Club'), ('10', 10, 'Club'), ('Jack', 10, 'Club'), ('Queen', 10, 'Club'),
                         ('King', 10, 'Club'), ('2', 2, 'Heart'), ('3', 3, 'Heart'),
                         ('4', 4, 'Heart'), ('5', 5, 'Heart'), ('6', 6, 'Heart'), ('7', 7, 'Heart'),
                         ('8', 8, 'Heart'), ('9', 9, 'Heart'), ('10', 10, 'Heart'), ('Jack', 10, 'Heart'),
                         ('Queen', 10, 'Heart'), ("King", 10, 'Heart')]


DEFAULT_TESTS = [('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'),
                 ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'),
                 ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'),
                 ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond'), ('Ace', 0, 'Diamond')]


DEFAULT_DECK = [('Ace', 0, 'Diamond'), ('2', 2, 'Diamond'), ('3', 3, 'Diamond'), ('4', 4, 'Diamond'),
                   ('5', 5, 'Diamond'), ('6', 6, 'Diamond'), ('7', 7, 'Diamond'), ('8', 8, 'Diamond'),
                   ('9', 9, 'Diamond'), ('10', 10, 'Diamond'), ('Jack', 10, 'Diamond'),
                   ('Queen', 10, 'Diamond'), ('King', 10, 'Diamond'), ('Ace', 0, 'Spade'),
                   ('2', 2, 'Spade'), ('3', 3, 'Spade'), ('4', 4, 'Spade'), ('5', 5, 'Spade'),
                   ('6', 6, 'Spade'), ('7', 7, 'Spade'), ('8', 8, 'Spade'), ('9', 9, 'Spade'),
                   ('10', 10, 'Spade'), ('Jack', 10, 'Spade'), ('Queen', 10, 'Spade'), ('King', 10, 'Spade'),
                   ('Ace', 0, 'Club'), ('2', 2, 'Club'), ('3', 3, 'Club'), ('4', 4, 'Club'),
                   ('5', 5, 'Club'), ('6', 6, 'Club'), ('7', 7, 'Club'), ('8', 8, 'Club'),
                   ('9', 9, 'Club'), ('10', 10, 'Club'), ('Jack', 10, 'Club'), ('Queen', 10, 'Club'),
                   ('King', 10, 'Club'), ('Ace', 0, 'Heart'), ('2', 2, 'Heart'), ('3', 3, 'Heart'),
                   ('4', 4, 'Heart'), ('5', 5, 'Heart'), ('6', 6, 'Heart'), ('7', 7, 'Heart'),
                   ('8', 8, 'Heart'), ('9', 9, 'Heart'), ('10', 10, 'Heart'), ('Jack', 10, 'Heart'),
                   ('Queen', 10, 'Heart'), ("King", 10, 'Heart')]

DEFAULT_FLAGS = [{

    "hit": False,
    "DD": False,
    "split": False,
    "insurance": False,
    "stand": False,
    "blackJack": False

}]
DEFAULT_BET = [10]
DEFAULT_SCORE = [0]
DEFAULT_CARDS = [[]]
DEFAULT_BUDGET = 200

NUM_PLAYERS = 2  # musi być mniejszy niż 8 bo tak
NUM_DECKS = 3

BET_MIN = 5
