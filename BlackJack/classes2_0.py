#!/usr/bin/python
# -*- coding: utf-8 -*-

from GameLogic.resources import DEFAULT_FLAGS, DEFAULT_BET, DEFAULT_CARDS, DEFAULT_DECK_NA, DEFAULT_BET, DEFAULT_CARDS,\
    DEFAULT_SCORE, DEFAULT_BUDGET, NUM_PLAYERS, NUM_DECKS, DEFAULT_DECK_LEN, BET_MIN, NA_DECK_LEN
from random import sample
from copy import deepcopy, copy
import GameLogic.colours as col
import time

def draw(deck):
    deck.append(DECK.pop(0))


class Entity(object):  # KLASA MACIERZYSTA DLA KLAS PLAYER I DEALER

    def __init__(self, lcards=None, lflags=None, lbets=None, score=0):
        self.decks = [Deck(cards, flags, bet) for cards, flags, bet in zip(lcards, lflags, lbets)]
        self.score = score


class Deck:
    def __init__(self, cards=None, flags=None, bet=None):
        self.cards = cards if cards is not None else DEFAULT_CARDS
        self.flags = flags if flags is not None else DEFAULT_FLAGS
        self.bet = bet if bet is not None else DEFAULT_BET
        self.insurance = 0 if not flags["insurance"] else self.bet * 0.5

    def __str__(self):
        report = "Deck.__str__() called\n"
        report += f"Cards : {self.cards}\n"
        report += f"Flags : {self.flags}\n"
        report += f"Bet : {self.bet}\n"
        return report

    def can_hit(self):
        return not self.flags["DD"]

    def can_stand(self):
        return not self.flags["stand"]

    def can_DD(self):
        return not self.flags["hit"]

    def can_split(self):
        if len(self.cards == 2):
            _, card1, _ = self.cards[0]
            _, card2, _ = self.cards[1]
            return card1 == card2

        else:
            return False



class Player(Entity):

    def __init__(self, lcards, lflags, lbets, score, name, budget):
        super().__init__(lcards=lcards, lflags=lflags, lbets=lbets, score=score)
        self.name = name
        self.budget = budget

    def get_flags(self):
        return [deck.flags for deck in self.decks]

    def reset_flags(self):
        for deck in self.decks:
            deck.flags = DEFAULT_FLAGS

    def __str__(self):
        report = ""
        for deck in self.decks:
            report += "\t"
            report += str(deck)
            report += "\n"
        report += f"Score : {self.score}"
        report += f"Budget : {self.budget}"
        report += f"Name : {self.name}"
        return report

    # USTAWIA WARTOŚĆ ZAKŁADU    /    PATRZĄC Z PERSPEKTYWY CZASU TA FUNKCJA JEST DO WYWALENIA DO POLA BĘDZIE SIĘ
    #                            /    ODWOŁYWAĆ BEZPOŚREDNIO PRZEZ PLAYER.BET = NOWA_WARTOŚĆ

    def add_points(self):
        self.score, aces_to_assign_value, self.cards = score_without_aces(self.cards)
        if len(aces_to_assign_value) != 0:
            print(f"{self.name} have {len(aces_to_assign_value)} aces.\n")
            print("\t1) 1 point\n")
            print("\t2) 11 points\n")
            run = True
            value = 11
            cards_to_insert = {}
            for loop, index_ace in enumerate(aces_to_assign_value.items()):
                index, ace = index_ace
                _, _, colour = ace
                while run:
                    print("Your current score is " + col.GREEN + f"{self.score}\n" + col.WHITE)
                    print(f"Choose the value of the {loop + 1} ace\n")
                    choice = input("I choose: ")
                    if choice == "1":
                        value = 1
                        run = False
                    if choice == "2":
                        value = 11
                        run = False
                    else:
                        print("Invalid input number! Please try again.")
                self.score += value
                cards_to_insert[index] = ("Ace", value, colour)
            print(f"Your final score is {self.score}")
            for index, card in cards_to_insert.items():
                self.cards.insert(index, card)

    def set_bet(self, new_bet=None):
        if new_bet is None:
            new_bet = input(col.GREEN + "Input new bet value: \n")

        if self.budget >= new_bet >= BET_MIN:
            self.bet = new_bet
        else:
            print(col.RED + "You cannot set your bet to that value\n")

    def win(self, black_jack=False):
        self.budget += 2 * self.bet if not black_jack else 2.5 * self.bet
        self.cards = []
        self.insurance = 0
        self.do_split: bool = False
        self.had_hit: bool = False
        self.had_split: bool = False
        self.had_stood: bool = False
        self.had_doubled: bool = False
        self.can_enter_new_round = True

    def loss(self):
        if self.insurance:
            self.budget += 2 * self.insurance
        self.cards = []
        self.insurance = 0
        self.do_split: bool = False
        self.had_hit: bool = False
        self.had_split: bool = False
        self.had_stood: bool = False
        self.had_doubled: bool = False
        self.can_enter_new_round = True

    def r_draw(self):
        self.budget += self.bet
        self.cards = []
        self.insurance = 0
        self.do_split: bool = False
        self.had_hit: bool = False
        self.had_split: bool = False
        self.had_stood: bool = False
        self.had_doubled: bool = False
        self.can_enter_new_round = True

    # METODY SPRAWDZAJĄCE:

    def can_hit(self):
        if not self.had_doubled and not self.had_stood:
            return True
        else:
            return False

    def can_split(self):
        if len(self.cards) >= 2:
            _, card1, _ = self.cards[0]
            _, card2, _ = self.cards[1]

            if card1 == card2 and not self.had_hit and not self.had_split and not self.had_stood:
                return True
        else:
            return False

    def can_double_down(self):
        return not self.had_hit and not self.had_stood and not self.had_doubled



def foo(pllst):
    for player in pllst:
        for deck in player.hands:
