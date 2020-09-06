#!/usr/bin/python
# -*- coding: utf-8 -*-


from resources import DEFAULT_BET, DEFAULT_CARDS, DEFAULT_SCORE, DEFAULT_BUDGET, \
    BET_MIN, DEFAULT_FLAGS, NUM_DECKS, NUM_PLAYERS, DEFAULT_DECK
from random import shuffle, choice
from typing import NewType
from typing import List, Tuple
from copy import deepcopy, copy
import time
import colours as col
from os import system, name


# UWAGA poniższy kod korzysta z pewnych założeń, których spełnienie jest konieczne do poprawnego działania programu;
#   1. Gracze mają różne imiona.
#   2. Nie można użyć split wiecej niż raz na 'rundę' (rozdzielonych kart nie można ponownie rozdzielić)
#   3. Od razu mam rozwiązanie dla wielu graczy,w game tworzona jest lista obiektów player
#   4. Zakładam, że defaultowe wartości gry wynoszą odpowiednio:
#       score = 0,  player.cards = [[]],   bet = 10,    dealer.cards = [[]],    imie = "player{numer gracza}"
#       budget = 200,   liczba graczy = 1,  liczba talii = 1
#
#   5. Jest problem z draw - potrzeba instancji klasy game żeby istniała talia na której draw wykonuje operacje

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def restart():
    import sys
    import os
    os.execv(sys.executable, ['python'] + sys.argv)


def create_lindexes():
    return [index+1 for index in range(NUM_PLAYERS)]


def create_player_names(lindexes):
    return [f"player {index}" for index in lindexes]


def create_deck():
    deck = NUM_DECKS * DEFAULT_DECK
    shuffle(deck)
    return deck


def create_players(llcards, llflags, llbets, llscores, llindexes, lnames, lbudgets):
    return [Player(deepcopy(lcards), deepcopy(lflags), deepcopy(lbets), deepcopy(lscores), deepcopy(lindexes), name2, budget) for
            lcards, lflags, lbets, lscores, lindexes, name2, budget in zip(llcards, llflags, llbets, llscores, llindexes, lnames, lbudgets)]


Card = NewType("Card", Tuple[str, int, str])
Cards = NewType("Cards", List[Card])


def game_loop():
    game = Game()
    game.first_round()
    game.first_turn()
    game.process_player_choices()
    while game.run_next_turn():
        game.next_turn()
        game.process_player_choices()
    game.final_turn()
    while game.run_next_round():
        game.next_round()
        game.first_turn()
        game.process_player_choices()
        while game.run_next_turn():
            game.next_turn()
            game.process_player_choices()
        game.final_turn()
    game.final_round()


class Game:

    def __init__(self, llcards=None, llflags=None, llscores=None, llbets=None, llindexes=None, lnames=None, lbudgets=None,
                 dealer_cards=None):
        self.__llscores = llscores if llscores is not None else deepcopy(NUM_PLAYERS * [DEFAULT_SCORE])
        self.__llbets = llbets if llbets is not None else deepcopy(NUM_PLAYERS * [DEFAULT_BET])
        self.__llcards = llcards if llcards is not None else deepcopy(NUM_PLAYERS * [DEFAULT_CARDS])
        self.__llflags = llflags if llflags is not None else deepcopy(NUM_PLAYERS * [DEFAULT_FLAGS])
        self.__llindexes = llindexes if llindexes is not None else deepcopy(NUM_PLAYERS * [create_lindexes()])
        self.__lnames = lnames if lnames is not None else deepcopy(create_player_names(self.__llindexes[0]))
        self.__lbudgets = lbudgets if lbudgets is not None else deepcopy(NUM_PLAYERS * [DEFAULT_BUDGET])
        self.deck = deepcopy(create_deck())
        self.cut_reached = False
        self.plbrkn = []
        self.pllst = create_players(self.__llcards, self.__llflags, self.__llbets,
                                    self.__llscores, self.__llindexes, self.__lnames, self.__lbudgets)
        self.dealer = Dealer(dealer_cards) if dealer_cards is not None else Dealer()

    def __str__(self) -> str:
        report = 'Game.__str__() called\n'
        report += f'Liczba graczy w grze : {len(self.pllst)}\nLiczba graczy bez pieniędzy : {len(self.plbrkn)}\n'
        for player in self.pllst:
            report += str(player)
        return report

    def insert_cut(self):
        lenght = len(self.deck)
        begin = int(lenght * 0.25)
        end = int(lenght * 0.8)
        index = choice(range(begin, end))
        replacement = self.deck[begin:end]
        replacement.insert(index, "CUT")
        self.deck = self.deck[:begin] + replacement + self.deck[end:]

    def first_turn(self) -> None:         # Ta funckja powinna konczyć się wyborem ruchu dla każdej ręki każdego gracza
        clear()
        self.draw_hand(self.dealer.hand)
        for player in self.pllst:
            for hand in player.hands_nt:
                self.draw_hand(hand)
            player.calculate_scores()
            self.show_dealers_card()
            player.choice(self.dealer, self.draw)
            player.choice_processing_functions()
            input("Press 'enter' to select next player.")

    def next_turn(self) -> None:
        clear()
        for player in self.pllst:
            if player.hands_nt:
                self.show_dealers_card()
                player.choice(self.dealer, self.draw)
                player.choice_processing_functions()
                input("Press 'enter' to select next player.")

    def run_next_turn(self) -> bool:
        run = 0
        for player in self.pllst:
            run += len(player.hands_nt)
        return bool(run)

    def final_turn(self) -> None:
        print("All players either lost or chose to stand! - Final turn begins")
        for player in self.pllst:
            for hand in player.hands_stand:
                hand.choose_best_ace_value()
                hand.check_for_blackjack()
        self.dealer.draw_until_17_or_higher(self.draw)
        self.determine_round_outcome()
        self.CENR()
        choose = input("Press 'enter' to continue.\nType :\n'reset' to restart the game.\n'quit' to quit the game.\n")
        if choose == "reset":
            restart()
        if choose == "quit":
            exit()

    def first_round(self) -> None:
        self.subtract_bets_from_budgets()
        self.insert_cut()

    def next_round(self) -> None:
        if self.cut_reached:
            print("Cut has been reached - deck is being shuffled")
            self.deck = create_deck()
            self.insert_cut()
        for player in self.pllst:
            player.reset_player()
        self.dealer.reset_dealer()
        self.subtract_bets_from_budgets()

    def run_next_round(self) -> bool:
        return bool(len(self.pllst))

    def final_round(self):
        outcome = "Game over!\nAll players are out of money:"
        scores = [(player.name, player.budget) for player in self.pllst + self.plbrkn]

        def sort(elem):
            return elem[1]

        scores.sort(key=sort)
        for index, score in enumerate(scores):
            name1, wynik = scores
            outcome += f'{index + 1}. {name1} finished the game with {wynik}$\n'
        print(outcome)

    def process_player_choices(self):
        for player in self.pllst:
            player.choice_processing_functions()

    def draw(self, hand):
        card = self.deck.pop(0)
        if card[0] == "Ace":
            if hasattr(hand, "aces"):
                hand.aces.append(card)
        if type(card) == str:
            self.cut_reached = True
            self.draw(hand)
        else:
            hand.cards.append(card)

    def draw_hand(self, hand):
        self.draw(hand)
        self.draw(hand)

    def show_dealers_card(self):
        print(f"Dealer's card : {self.dealer.hand.cards[0]}") if self.run_next_turn() else print(
            f"Dealer's cards : {self.dealer.hand.cards}")

    def determine_round_outcome(self):
        print()
        d_score = self.dealer.hand.score
        if d_score > 21:
            print("Dealer busted! All those who didn't bust win!")
            for player in self.pllst:
                def difference(dealer_score, hand_score):
                    return abs(dealer_score - 21) - abs(hand_score - 21)

                hands_blckjck = [hand for hand in player.hands_stand if hand.flags["blackJack"] and difference(d_score, hand.score) != 0]
                hands_win = [hand for hand in player.hands_stand if difference(d_score, hand.score) > 0 and not hand.flags["blackJack"]]
                print(col.red(f"{player.name}") + " :")
                for hand in hands_blckjck:
                    pot = hand.win()
                    player.budget += pot
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score}" + col.green(" > ") + f"{d_score} - "
                    outcome += col.cyan(f"Black Jack! pot {pot}$ = {hand.bet}$ * 2,5")
                    print(outcome)

                for hand in hands_win:
                    pot = hand.win()
                    player.budget += pot
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score}" + col.green(" > ") + f"{d_score} - "
                    outcome += col.green(f'wins {pot}$')
                    print(outcome)

                for hand in player.hands_busted:
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score}" + col.red(" >> ") + "21 - "
                    outcome += col.red("busted")
                    print(outcome)
                print(f"    Current budget : {player.budget}$\n")
        else:
            for player in self.pllst:
                print(col.red(f"{player.name}") + " :")

                def difference(dealer_score, hand_score):
                    return abs(dealer_score - 21) - abs(hand_score - 21)

                hands_blckjck = [hand for hand in player.hands_stand if hand.flags["blackJack"] and difference(d_score, hand.score) != 0]
                hands_win = [hand for hand in player.hands_stand if difference(d_score, hand.score) > 0 and not hand.flags["blackJack"]]
                hands_draw = [hand for hand in player.hands_stand if not difference(d_score, hand.score)]
                hands_loss = [hand for hand in player.hands_stand if difference(d_score, hand.score) < 0]
                hands_busted = [hand for hand in player.hands_busted]

                for hand in hands_blckjck:
                    pot = hand.win()
                    player.budget += pot
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score}" + col.green(" > ") + f"{d_score} - "
                    outcome += col.cyan(f"Black Jack! pot {pot}$ = {hand.bet}$ * 2,5")
                    print(outcome)

                for hand in hands_win:
                    pot = hand.win()
                    player.budget += pot
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score}" + col.green(" > ") + f"{d_score} - "
                    outcome += col.green(f'wins {pot}$')
                    print(outcome)

                for hand in hands_draw:
                    pot = hand.draw()
                    player.budget += pot
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score} = {d_score} - " \
                                                                      f"draws bet returned ({hand.bet}$)"
                    print(outcome)

                for hand in hands_loss:
                    pot = hand.loss(self.dealer)
                    player.budget += pot
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score}" + col.red(" < ") + f"{d_score} - "
                    if pot == 0:
                        outcome += col.red(f"loses")
                    else:
                        outcome += col.yellow("loses with valid insurance")
                    print(outcome)

                for hand in hands_busted:
                    outcome = col.magenta(f"    hand {hand.index}") + f" : {hand.score}" + col.red(" >> ") + "21 - "
                    outcome += col.red("busted")
                    print(outcome)
                print(f"    Current budget : {player.budget}$\n")

    def CENR(self):
        npllst = []
        for player in self.pllst:
            if player.can_afford_new_round():
                npllst.append(player)
            else:
                self.plbrkn.append(player)
        self.pllst = npllst

    def subtract_bets_from_budgets(self) -> None:  # OBLICZA BUDŻET PO ODJĘCIU ZAKŁĄDU (PRZY WEJŚCIU DO NOWEJ RUNDY)
        for player in self.pllst:
            for hand in player.hands_nt:
                player.budget -= hand.bet
        print("Bets has been subtracted form budgets.")



class HandDealer:
    def __init__(self, cards: List[Card] = None, score: int = None):
        self.score = score if score is not None else deepcopy(DEFAULT_SCORE[0])
        self.cards = cards if cards is not None else deepcopy(DEFAULT_CARDS[0])

    def __str__(self):
        report = f"HandDealer.__str__() called\n"
        report += f"Cards : {self.cards}\n"
        report += f"Score : {self.score}\n"
        return report


class Hand(HandDealer):
    def __init__(self, cards=None, flags=None, bet=None, score=None, index=0):
        super().__init__(cards, score)
        self.flags = flags if flags is not None else deepcopy(DEFAULT_FLAGS[0])
        self.bet = bet if bet is not None else deepcopy(DEFAULT_BET[0])
        self.index = index
        self.aces = []

    def __str__(self):
        report = f"Hand.__str__() called for id : {id(self)}\n"
        report += f"Cards : {self.cards}\n"
        report += f"Flags : {self.flags}\n"
        report += f"Bet : {self.bet}\n"
        report += f"Score : {self.score}\n"
        report += f"Index : {self.index}"
        return report

    def __eq__(self, other):
        if type(other) == tuple:
            return False
        return id(self) == id(other)

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
        return dealer.hand.cards[0][0] == "Ace"

    def win(self):
        return 2 * self.bet if not self.flags["blackJack"] else 2.5 * self.bet

    def loss(self, dealer):
        return 0 if not (self.flags["insurance"] and dealer.hand.score == 21) else self.bet

    def draw(self):
        return self.bet

    def check_for_blackjack(self):
        if len(self.cards) == 2 and self.score == 21:
            self.flags["blackJack"] = True

    def change_and_replace(self, best_value, score):
        self.score = score
        self.aces[:best_value] = [("Ace", 1, colour) for _, _, colour in self.aces[:best_value]]
        self.aces[best_value:] = [("Ace", 11, colour) for _, _, colour in self.aces[best_value:]]
        self.cards = [card if card[0] != "Ace" else self.aces.pop() for card in self.cards]
        print(f"Hand {self.index}: Best ace values has been chosen.")
        print(f"{self.score} : {self.cards}")

    def choose_best_ace_value(self):
        if self.aces:
            for it in range(len(self.aces) + 1):
                score = self.score
                ones = len(self.aces) - it
                score += ones + it * 11
                if score > 21:
                    self.change_and_replace(ones + 1, score-10)
                    break
                if it == len(self.aces):
                    self.change_and_replace(ones, score)


class Player:
    def __init__(self, lcards, lflags, lbets, lscores, lindexes, name3, budget):
        self.hands_nt = [Hand(deepcopy(cards), deepcopy(flags), copy(bet), copy(score), copy(index)) for cards, flags, bet, score, index in
                         zip(lcards, lflags, lbets, lscores, lindexes)] if \
            (lcards, lflags, lbets, lscores) != (None, None, None, None, None) else [Hand()]
        self.name = name3
        self.aces = []
        self.budget = budget
        self.hands_stand = []
        self.hands_busted = []

    def __str__(self):
        report = f"\tPlayer.__str__() called\n"
        report += "\u001b[31m"
        report += f"Name : {self.name}\n"
        report += "\u001b[37m"
        report += f"Budget : {self.budget}$\n"
        report += f"{self.name}.hands_nt : {self.hands_nt}\n"
        report += f"{self.name}.hands_stand : {self.hands_stand}\n"
        report += f"{self.name}.hands_busted : {self.hands_busted}\n"
        return report

    def hit(self, hand, draw):
        draw(hand)
        hand.flags["hit"] = True

    def stand(self, hand):
        hand.flags["stand"] = True
        self.hands_stand.append(hand)

    def DD(self, hand, draw):
        if self.can_afford_new_bet(hand):
            self.budget -= hand.bet
            draw(hand)
            self.calculate_scores()
            hand.bet *= 2
            hand.flags["DD"] = True
            if hand.score <= 21:
                self.hands_stand.append(hand)
        else:
            print(f"{self.name} : Hand {hand.index} cannot afford to Double Down.")

    def split(self, hand):
        if self.can_afford_new_bet(hand):
            index = self.hands_nt.index(hand)
            hand.flags["split"] = True
            self.hands_nt = [elem for elem in self.hands_nt if elem != hand]
            self.budget -= hand.bet
            hand1, hand2 = Hand(deepcopy([hand.cards[0]]), deepcopy(hand.flags), copy(hand.bet)),\
                           Hand(deepcopy([hand.cards[1]]), deepcopy(hand.flags), copy(hand.bet))
            hand1.index = hand.index
            for h in (hand1, hand2):
                for card in h.cards:
                    if card[0] == "Ace":
                        h.aces.append(card)
            self.hands_nt.insert(index, (hand1, hand2))
        else:
            print(f"{self.name} : Hand {hand.index} cannot afford to split.")

    def insure(self, hand):
        if self.can_afford_insurance(hand):
            self.budget -= hand.bet * 0.5
            hand.flags["insurance"] = True
        else:
            print(f"{self.name} : Hand {hand.index} cannot afford an insurance.")

    def can_afford_insurance(self, hand):
        return hand.bet * 0.5 <= self.budget

    def can_afford_new_bet(self, hand):
        return hand.bet <= self.budget

    def can_afford_new_round(self):
        return self.budget >= BET_MIN

    def choice(self, dealer, draw):
        for hand in self.hands_nt:
            run = True
            print(col.red(f"{self.name}") + " : ")
            print(f"    budget : {self.budget}$")
            mess = col.magenta(f"    hand {hand.index} ") + f":\n       score : {hand.score}"
            mess += f"{len(self.aces)}x Ace" if self.aces else ""
            print(mess)
            print(f"       bet : {hand.bet}$")
            print(f"       cards : {hand.cards}")
            while run:
                choice = input()
                if choice == "hit":
                    if hand.can_hit():
                        self.hit(hand, draw)
                        run = False
                    else:
                        print(f"This hand can't hit.")
                elif choice == "stand":
                    if hand.can_stand():
                        self.stand(hand)
                        run = False
                    else:
                        print(f"This hand can't stand.")
                elif choice == "split":
                    if hand.can_split():
                        self.split(hand)
                        run = False
                    else:
                        print(f"This hand can't split.")
                elif choice == "double down":
                    if hand.can_DD():
                        self.DD(hand, draw)
                        run = False
                    else:
                        print(f"This hand can't DD.")
                elif choice == "insurance" or choice == "insure":
                    if hand.can_insure(dealer):
                        self.insure(hand)
                        run = False
                    else:
                        print(f"This hand can't use insurance.")
                else:
                    print("Invalid input please try again.")

    def choice_processing_functions(self):
        self.check_for_split()
        self.calculate_scores()
        self.check_for_bust()
        self.lists_override()

    def check_for_bust(self):
        for hand in self.hands_nt:
            if hand.score - len(hand.aces) > 21:
                self.hands_busted.append(hand)

    def check_for_split(self):
        nowa_lista = []
        i = 1
        for elem in self.hands_nt:
            if type(elem) == tuple:
                elem[1].index = len(self.hands_nt + self.hands_busted + self.hands_stand) + i
                i += 1
                nowa_lista.append(elem[0])
                nowa_lista.append(elem[1])
            else:
                nowa_lista.append(elem)
        nowa_lista.sort(key=lambda elem: elem.index)
        self.hands_nt = nowa_lista

    def lists_override(self):
        self.hands_nt = [hand for hand in self.hands_nt if hand not in self.hands_stand + self.hands_busted]

    def get_flags(self):
        return [hand.flags for hand in self.hands_nt]

    def reset_flags(self):
        for hand in self.hands_nt:
            hand.flags = deepcopy(DEFAULT_FLAGS)

    def calculate_scores(self):
        for hand in self.hands_nt:
            nscore = 0
            for card in hand.cards:
                nscore += card[1]
            hand.score = nscore

    def reset_player(self):
        for index in create_lindexes():
            self.hands_nt = [Hand(index=copy(index))]
        self.hands_stand = []
        self.hands_busted = []


class Dealer:

    def __init__(self, cards: List[Cards] = None, score=None):
        self.hand = HandDealer(cards=cards, score=score) if (cards, score) != (None, None) else HandDealer()

    def reset_dealer(self):
        self.hand = HandDealer()

    def calculate_score(self):
        aces = []
        nscore = 0
        for card in self.hand.cards:
            if card[0] != "Ace":
                nscore += card[1]
            else:
                aces.append(card)
        self.hand.score = nscore
        naces = []
        for ace in aces:
            _, point, colour = ace
            if self.hand.score <= 10:
                point = 11
            else:
                point = 1
            naces.append(("Ace", point, colour))
            self.hand.score += point
        self.hand.cards = [card if card[0] != "Ace" else naces.pop() for card in self.hand.cards]

    def draw_until_17_or_higher(self, draw):
        self.calculate_score()
        message = f"Dealer's cards and score : {self.hand.cards} : {self.hand.score}"
        message += " < 17" if self.hand.score < 17 else ""
        print(message)
        while self.hand.score < 17:
            draw(self.hand)
            print(f"Dealer draws {self.hand.cards[-1]}")
            self.calculate_score()
            time.sleep(2)
        else:
            print(f"Dealer's final cards and score : {self.hand.cards} : {self.hand.score}")


def main():
    game_loop()


main()
