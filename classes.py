#!/usr/bin/python
# -*- coding: utf-8 -*-


from GameLogic.resources import DEFAULT_DECK_NA, DEFAULT_BET, DEFAULT_CARDS, DEFAULT_SCORE, DEFAULT_BUDGET, NUM_PLAYERS, NUM_DECKS, \
    DEFAULT_DECK_LEN, BET_MIN, NA_DECK_LEN, DEFAULT_FLAGS
from random import sample
from typing import NewType
from typing import List, Tuple, Dict
from copy import deepcopy, copy
import colours as col
import time


# UWAGA poniższy kod korzysta z pewnych założeń, których spełnienie jest konieczne do poprawnego działania programu;
#   1. Gracze mają różne imiona.
#   2. Nie można użyć split wiecej niż raz na 'rundę' (rozdzielonych kart nie można ponownie rozdzielić)
#   3. Od razu mam rozwiązanie dla wielu graczy,w game tworzona jest lista obiektów player
#   4. Zakładam, że defaultowe wartości gry wynoszą odpowiednio:
#       score = 0,  player.cards = [[]],   bet = 10,    dealer.cards = [[]],    imie = "player{numer gracza}"
#       budget = 200,   liczba graczy = 1,  liczba talii = 1
#
#   5. Jest problem z draw - potrzeba instancji klasy game żeby istniała talia na której draw wykonuje operacje

def create_player_names():
    return [f"player {i + 1}" for i in range(NUM_PLAYERS)]


def initialize_game():
    return Game()


def create_deck():
    return sample(NUM_DECKS * DEFAULT_DECK_NA, NUM_DECKS * NA_DECK_LEN)


DECK = deepcopy(create_deck())


def create_players(llscores, llcards, llbets, llflags, lnames, lbudgets):
    return [Player(lcards, lflags, lbets, lscores, name, budgets) for lcards, lflags, lbets, lscores, name, budgets in
            zip(llcards, llflags, llbets, llscores, lnames, lbudgets)]


def draw(cards):
    cards.append(DECK.pop(0))


class Game:

    def __init__(self, llcards=None, llflags=None, llscores=None, llbets=None, lnames=None, lbudgets=None, ldealer_cards=None):
        self.__llscores = llscores if llscores is not None else copy([NUM_PLAYERS * DEFAULT_SCORE])
        self.__llbets = llbets if llbets is not None else copy([NUM_PLAYERS * DEFAULT_BET])
        self.__llcards = llcards if llcards is not None else copy([NUM_PLAYERS * DEFAULT_CARDS])
        self.__llflags = llflags if llflags is not None else deepcopy([NUM_PLAYERS * DEFAULT_FLAGS])
        self.__lnames = lnames if lnames is not None else create_player_names()
        self.__lbudgets = lbudgets if lbudgets is not None else copy([NUM_PLAYERS * DEFAULT_BUDGET])

        self.pllst = create_players(self.__llcards, self.__llflags, self.__llbets,
                                    self.__llscores, self.__lnames, self.__lbudgets)

        self.dealer = Dealer(ldealer_cards) if ldealer_cards[0] is not None else Dealer()


    def __str__(self) -> str:
        report = 'Game.__str__() called\n'
        report += f'Liczba graczy {len(self.pllst)}\n'


    def run_round_loop(self) -> None:
        return len(self.plbsd + self.pl_stood) != NUM_PLAYERS

    def final_round(self) -> None:
        print("All players either lost or chose to stand!\n")
        time.sleep(3)
        self.calculate_and_verify_scores()
        self.dealer.draw_until_17_or_higher()
        self.calculate_round_outcome()
        self.check_if_can_aff_new_round()

    def next_round(self) -> None:
        self.calculate_and_verify_scores()
        # TUTAJ GRACZ PODEJMUJE DECYZJE MIĘDZY hit(), double_down(), split(), insure(), stand()

    def first_round(self) -> None:
        self.subtract_bets_from_budgets()

    def first_turn(self):
        for player in self.pllst:
            player.hands_nt = player.hands
            for hand in player.hands_nt:
                hand.draw_hand()
            player.calculate_scores()

    def next_turn(self):
        for player in self.pllst:
            for hand in self.hand_new_turn[player]:
                #
                #   TUTAJ PETLA AKCJI
                #

    def final_turn(self):
        raise NotImplementedError

    def run_next_turn(self):
        return


    def calculate_round_outcome(self) -> None:
        for player in self.pl_stood:
            difference = abs(self.dealer.score - 21) - abs(player.score - 21)
            if difference > 0:
                player.win(False if player not in self.black_jack else True)
                print(f"{player.name} won this round.\n")
            elif difference == 0:
                player.loss()
                print(f"{player.name} lost this round.\n")
            else:
                player.budget += player.bet
                print(f"{player.name} had the same score as dealer.\n")

    def run_game_loop(self):
        return len(self.pl_broken) != NUM_PLAYERS

    def check_if_can_aff_new_round(self):
        raise NotImplementedError

    def subtract_bets_from_budgets(self) -> None:  # OBLICZA BUDŻET PO ODJĘCIU ZAKŁĄDU (PRZY WEJŚCIU DO NOWEJ RUNDY)
        for player in self.pllst:
            for hand in player.hands:
                player.budget -= hand.bet


class Entity:

    def __init__(self, lcards=None, lflags=None, lbets=None, lscores=None):
        self.hands = [Hand(cards, flags, bet, score) for cards, flags, bet, score in zip(lcards, lflags, lbets, lscores)] if \
            (lcards, lflags, lbets, lscores) != (None, None, None, None) else [Hand()]


class HandDealer:
    def  __init__(self, cards=DEFAULT_CARDS, score=DEFAULT_SCORE):
        self.score = score
        self.cards = cards

    def __str__(self):
        report = f"HandDealer.__str__() called\n"
        report += f"Cards : {self.cards}\n"
        report += f"Score : {self.score}\n"
        return report


class Hand(HandDealer):
    def __init__(self, cards=DEFAULT_CARDS, flags=DEFAULT_FLAGS, bet=DEFAULT_BET, score=DEFAULT_SCORE):
        super().__init__(cards, score)
        self.flags = flags
        self.bet = bet

    def __str__(self):
        report = "Hand.__str__() called\n"
        report += f"Cards : {self.cards}\n"
        report += f"Flags : {self.flags}\n"
        report += f"Bet : {self.bet}\n"
        report += f"Score : {self.score}\n"
        return report

    def can_hit(self):
        return not self.flags["DD"]

    def can_stand(self):
        return not self.flags["stand"]

    def can_DD(self):
        return not self.flags["hit"]

    def can_split(self):
        if len(self.cards) == 2:
            _, card1, _ = self.cards[0]
            _, card2, _ = self.cards[1]
            return card1 == card2

        else:
            return False

    def can_insure(self, dealer):
        return dealer.hands[0][0][0] == "Ace"

    def draw_hand(self):
        draw(self.cards)
        draw(self.cards)

    def hit(self):
        draw(self.cards)
        self.flags["hit"] = True

    def stand(self):
        self.flags["stand"] = True

    def DD(self):
        draw(self.cards)
        draw(self.cards)
        self.flags["DD"] = True

    def split(self):
        self.cards = [[card] for card in self.cards]
        self.flags["split"] = True

    def insure(self):
        self.flags["insurance"] = True


class Player(Entity):

    def __init__(self, lcards, lflags, lbets, lscores, name, budget):
        super().__init__(lcards=lcards, lflags=lflags, lbets=lbets, lscores=lscores)
        self.name = name
        self.budget = budget

        self.hands_nt = []
        self.hands_stand = []
        self.hands_busted = []

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

    def get_flags(self):
        return [deck.flags for deck in self.decks]

    def reset_flags(self):
        for deck in self.decks:
            deck.flags = DEFAULT_FLAGS

    def calculate_scores(self):
        n_hands_nt = []
        for hand in self.hands_nt:
            nscore = 0
            for card in hand.cards:
                nscore += card[1]
            hand.score = nscore
            if hand.score > 21:
                self.hands_busted.append(hand)
            else:
                n_hands_nt.append(hand)
        self.hands_nt = n_hands_nt

    def reset_cards(self):
        self.decks = [Hand(bet=deck.bet) for deck in self.decks]

    def win(self, black_jack=False):
        self.budget += 2 * self.bet if not black_jack else 2.5 * self.bet
        self.reset_cards()

    def loss(self):
        if self.decinsurance:
            self.budget += 2 * self.insurance
        self.reset_cards()

    def r_draw(self):
        self.budget += self.bet
        self.reset_cards()


class Dealer(Entity):

    def __init__(self, lcards=None, lscore=None):
        super().__init__(lcards=lcards, lscores=lscore)

    def add_points(self):
        self.score, aces_with_indexes, self.cards = score_without_aces(self.cards)
        for index, card in aces_with_indexes.items():
            _, point, colour = card
            if self.score <= 10:
                point = 11
            else:
                point = 1
            new_card = "Ace", point, colour
            self.score += point
            self.cards.insert(index, new_card)

    def draw_until_17_or_higher(self):
        self.add_points()
        print(f"Dealer's score is {self.score}\n")
        if self.score < 17:
            print("dealer draws!\n")
            time.sleep(3)
            draw(self.hands[0].cards)
            self.add_points()
            self.draw_until_17_or_higher()
        else:
            print(f"Dealer's final score is {self.score}\n")
