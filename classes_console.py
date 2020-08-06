#!/usr/bin/python
# -*- coding: utf-8 -*-


from resources import DEFAULT_DECK, DEFAULT_BET, DEFAULT_CARDS, DEFAULT_SCORE, DEFAULT_BUDGET, NUM_PLAYERS, NUM_DECKS, \
    DEFAULT_DECK_LEN, BET_MIN
from random import sample
from typing import NewType
from typing import List, Tuple
from copy import deepcopy, copy
from utility import add_cards, add_cards_dealer
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
    names = []
    for i in range(NUM_PLAYERS):
        names.append(f"player {i + 1}")
    return names


# TWORZY TALIĘ DO GRY

def create_deck():
    return sample(NUM_DECKS * DEFAULT_DECK, NUM_DECKS * DEFAULT_DECK_LEN)


def score_without_aces(cards):
    aces_with_indexes = {}
    override_cards = []
    score = 0
    for index, card in enumerate(cards):
        condition = card[1] == 0
        if condition:
            aces_with_indexes[index] = card      ## WRÓCIĆ WAŻNE!!!!
        else:
            _, points, _ = card
            score += points
            override_cards.append(card)
    return score, aces_with_indexes, override_cards


def print_stat(player):
    stats = "\n"
    stats += col.MAGENTA + f"{player.name}" + col.WHITE + "'s turn       " + col.MAGENTA + "(˵ ͡° ͜ʖ ͡°˵)\n" \
             + col.WHITE + f"\n\tscore: {player.score}\n\tbet: {player.bet}\n\tbudget: {player.budget}\n"
    print(stats)


DECK = deepcopy(create_deck())


# FUNKCJA DO TWORZENIA LISTY GRACZY


def create_players(scores, players_cards, bets, players_names, budgets):
    players = []
    for i in range(NUM_PLAYERS):
        players.append(Player(cards=deepcopy(players_cards[i]), score=scores[i], bet=bets[i],
                              budget=budgets[i], name=players_names[i]))
    return players


Card = NewType("Card", Tuple[str, int, str])
Cards = NewType("Cards", List[Card])


# GŁÓWNA KLASA KTÓRA ZAWIERA WSZYSTKIE DANE O GRZE
# INFORMACJE PRZECHOWYWANE SĄ W POSTACI LIST (ROZWIĄZAUJE TO PROBLEM GRY DLA WIELU GRACZY)


class Game:

    def __init__(self, scores: List[int] = None, players_cards: List[Cards] = None,
                 players_bets: List[float] = None, dealer_cards: List[Cards] = None,
                 players_names: List[str] = None, budgets=None):
        self.__scores = scores if scores is not None else copy(NUM_PLAYERS * DEFAULT_SCORE)
        self.__bets = players_bets if players_bets is not None else copy(NUM_PLAYERS * DEFAULT_BET)
        self.__players_cards = players_cards if players_cards is not None else copy(NUM_PLAYERS * DEFAULT_CARDS)
        self.__players_names = players_names if players_names is not None else create_player_names()
        self.__budgets = budgets if budgets is not None else copy(NUM_PLAYERS * DEFAULT_BUDGET)

        self.pl_stood = []
        self.pl_broken = []
        self.pl_busted = []
        self.pl_split = []

        self.shared_budgets = {}
        self.dealer = Dealer(dealer_cards) if dealer_cards is not None else Dealer(DEFAULT_CARDS[0], 0)
        self.player_list = create_players(scores=self.__scores, budgets=self.__budgets,
                                          players_cards=self.__players_cards, bets=self.__bets,
                                          players_names=self.__players_names)

    def __str__(self) -> str:
        report = ""
        for index, player in enumerate(self.player_list):
            report += f"\nPlayer {index + 1}. data:\ncards: {player.cards}\n" \
                      f"score: {player.score}\nbet: {player.bet}\nbudget: {player.budget}\nname: {player.name}\n"

        return f"Created {len(self.player_list)} player(s):" + report

    def run_game(self):
        raise NotImplementedError

    def print_table(self):
        beg = "________________________________________________________\n" \
              "|\n" \
              "|    Dealer's cards:\n"

        cards = "" + add_cards_dealer(self.dealer.cards) + "|    \n|    "
        for player in self.player_list:
            cards += f"{player.name}'s cards:\n"
            cards += add_cards(player.cards) + "|    "
        cards += "\n|_______________________________________\n" if len(self.pl_stood) != 0 else "\n"
        for player_st in self.pl_stood:
            cards += f"|    {player_st.name}'s cards:\n"
            cards += add_cards(player_st.cards) + "|    \n"

        end = "|_______________________________________________________\n"

        print(beg + cards + end)

    def print_table_final_round(self):
        beg = "________________________________________________________\n" \
              "|\n" \
              "|    Dealer's cards:\n"

        cards = "" + add_cards(self.dealer.cards) + "|    \n|    "
        for player in self.player_list:
            cards += f"{player.name}'s cards:\n"
            cards += add_cards(player.cards) + "|    "
        cards += "\n|_______________________________________\n" if len(self.pl_stood) != 0 else "\n"
        for player_st in self.pl_stood:
            cards += f"|    {player_st.name}'s cards:\n"
            cards += add_cards(player_st.cards) + "|    \n"

        end = "|_______________________________________________________\n"

        print(beg + cards + end)

    # PONIŻSZE METODY SĄ DO DOPRACOWANIA / OBGADANIA Z KIMŚ KTO OGARNIA PĘTLĘ GRY

    # Poziom rundy

    def run_game_loop(self):
        return len(self.pl_broken) != NUM_PLAYERS

    def run_round_loop(self):
        return len(self.pl_busted + self.pl_stood) - len(self.pl_split) != NUM_PLAYERS

    def final_round(self):
        print("All players either lost or chose to stand!\n")
        time.sleep(3)
        self.calculate_and_verify_scores()
        self.print_table_final_round()
        self.dealer.draw_until_17_or_higher()
        self.print_table_final_round()
        self.calculate_round_outcome()

    def next_round(self):
        #self.print_table()
        self.calculate_and_verify_scores()
        self.player_action_loop()

    def first_round(self) -> None:
        for player in self.player_list:
            player.draw_hand()
        self.dealer.draw_hand()
        self.subtract_bets_from_budgets()
        self.print_table()
        self.calculate_and_verify_scores()
        self.player_action_loop()
        self.split_if_flagged()

    def player_action_loop(self):
        for player in self.player_list:
            print(player)
            print_stat(player)
            self.round_menu(player)

    def calculate_round_outcome(self):
        for player in self.pl_stood:
            difference = abs(self.dealer.score - 21) - abs(player.score - 21)
            if difference > 0:
                player.win()
                print(f"{player.name} won this round.\n")
            elif difference == 0:
                player.loss()
                print(f"{player.name} lost this round.\n")
            else:
                player.budget += player.bet
                print(f"{player.name} had the same score as dealer.\n")

    def calculate_and_verify_scores(self):
        for index, player in enumerate(self.player_list):
            player.add_points()
            if player.score > 21:
                print(col.RED + f"{player.name} has busted! (score > 21)" + col.WHITE)
                self.pl_busted.append(self.player_list.pop(index))

        #   Poziom gry

    def check_if_can_aff_new_round(self):
        override_pllist = []
        for player in self.player_list:
            if player.budget >= BET_MIN:
                player.budget -= player.bet
                override_pllist.append(player)
            else:
                player.budget = 0
                print(f"{player.name} can't afford a new bet and is out of game!")
                self.pl_broken.append(player)
        self.player_list = override_pllist

    def round_menu(self, player):
        can_use = [0]
        if player.can_hit():
            col_code = col.GREEN
            can_use.append(1)
        else:
            col_code = col.RED
        print(col_code + "\t\t1) hit" + col.WHITE)
        if player.can_double_down():
            col_code = col.GREEN
            can_use.append(2)
        else:
            col_code = col.RED
        print(col_code + "\t\t2) double down" + col.WHITE)
        if player.can_split():
            col_code = col.GREEN
            can_use.append(3)
        else:
            col_code = col.RED
        print(col_code + "\t\t3) split" + col.WHITE)
        if can_insure(dealer=self.dealer):
            col_code = col.GREEN
            can_use.append(4)
        else:
            col_code = col.RED
        print(col_code + "\t\t4) insure" + col.WHITE)
        print(col.GREEN + "\t\t0) stand\n" + col.WHITE)
        run = True
        override_pllist = []
        while run:
            c = input("I choose: ")
            if c == "1" and 1 in can_use:
                player.hit()
                run = False
                override_pllist.append(player)
            elif c == "2" and 2 in can_use:  # TRZEBA BEDZIE TO POPRAWIC
                player.double_down()
                run = False
                override_pllist.append(player)
            elif c == "3" and 3 in can_use:
                player.split()
                run = False
                override_pllist.append(player)
            elif c == "4" and 4 in can_use:
                player.insure()
                run = False
                override_pllist.append(player)
            elif c == "0":
                player.stand()
                run = False
                self.pl_stood.append(player)
            else:
                print("Invalid input, please try again.")
        self.player_list = override_pllist

    def subtract_bets_from_budgets(self):  # OBLICZA BUDŻET PO ODJĘCIU ZAKŁĄDU (PRZY WEJŚCIU DO NOWEJ RUNDY)
        for player in self.player_list:
            player.budget -= player.bet

    # def check_budgets(self):  # SPRAWDZA CZY GRACZA STAĆ NA WEJŚCIE DO NOWEJ RUNDY
    #     for player in self.player_list:
    #         if player.budget <= player.bet:  # POWINNO BYĆ <= min_bet (zakład ma jakąś minimalną wartość)
    #             Player.can_enter_new_round = False
    #             print(f"{player.name} is broken!")

    # TEJ FUNCKJI UŻYWA METODA DO REALIZACJI SPLIT'U, PRZYJMUJE ONA GRACZA I JEGO INDEX NA LIŚCIE GRACZY A NASTĘPNIE
    # ROZDZIELA GO NA "2 RĘCE" CZYLI DZIELI BUDŻET, KARTY I  ZMIENIA IMIONA.

    def create_hands(self, player, player_index):
        self.shared_budgets[f"{player.name} shared budget"] = SharedBudget(player.budget, player_index)
        first_hand = Player(cards=[deepcopy(player.cards[0])], score=deepcopy(player.score), bet=deepcopy(player.bet),
                            budget=0, name=f"{player.name}'s first hand")
        second_hand = Player(cards=[deepcopy(player.cards[1])], score=deepcopy(player.score), bet=deepcopy(player.bet),
                             budget=0, name=f"{player.name}'s second hand")
        first_hand.budget = self.shared_budgets[f"{player.name} shared budget"]
        second_hand.budget = self.shared_budgets[f"{player.name} shared budget"]
        return [first_hand, second_hand]

    # TUTAJ ZASTOSOWAŁEM TAKIE SŁABE ROZWIĄZANIE, JEŚLI GRACZ CHCE SPLITOWAĆ TO USTAWIA U NIEGO WARTOŚĆ POLA
    #

    def split_if_flagged(self):
        for player_index, player in enumerate(self.player_list):
            if player.do_split:
                hands = self.create_hands(player, player_index)
                self.pl_split.append(self.player_list.pop(player_index))
                self.player_list.insert(player_index, hands[0])
                self.player_list.insert(player_index + 1, hands[1])

            else:
                pass


class SharedBudget:  # KLASA UŻYWANA DO TWORZENIA WSPÓŁDZIELONYCH BUDŻETÓW (DLA SPLITU)
    def __init__(self, budget, index):
        self.budget = budget
        self.index = index

    # PONIŻSZE METODY IMPLEMENTUJĄ OPERATORY +, -, *, -=, +=, <, >, <=, >=, ==

    def __add__(self, other):
        return self.budget + other

    def __lt__(self, other):
        return self.budget < other

    def __gt__(self, other):
        return self.budget > other

    def __le__(self, other):
        return self.budget <= other

    def __ge__(self, other):
        return self.budget >= other

    def __sub__(self, other):
        return self.budget - other

    def __isub__(self, other):
        return self.budget - other

    def __iadd__(self, other):
        return self.budget + other

    def __mul__(self, other):
        return self.budget * other

    def __eq__(self, other):
        return self.budget == other

    def __str__(self):
        return f"Shared Budget of player {self.index + 1} budget: {self.budget}"

    def change_budget(self, x):  # NIE WIEM CZY TO POTRZEBNE LEPIEJ ODWOŁYWAĆ SIĘ BEZPOŚREDNIO DO POLA ?
        self.budget = x


class Entity(object):  # KLASA MACIERZYSTA DLA KLAS PLAYER I DEALER

    def __init__(self, cards=None, score=0):
        self.cards = cards if cards is not None else []
        self.score = score

    def draw(self):
        self.cards.append(DECK.pop(0))

    def draw_hand(self):
        self.draw()
        self.draw()


def can_insure(dealer):
    if dealer.cards[0][0] == "Ace":
        return True
    else:
        return False


class Player(Entity):

    def __init__(self, cards: list, score: int, bet: float, name: str, budget):
        super().__init__(cards=cards, score=score)
        self.bet = bet
        self.name = name
        self.budget = budget
        self.insurance = 0
        self.do_split: bool = False  #
        self.had_hit: bool = False  #
        self.had_split: bool = False  # TE ZMIENNE PRZECHOWUJĄ INFORMACJE O RUCHACH GRACZA TZN
        self.had_stood: bool = False  # JAKICH METOD UŻYŁ POTRZEBNE DO SPRAWDZANIA CZY NP GRACZ MOŻE
        self.had_doubled: bool = False  # SPLITOWAĆ (MOŻLIWE TYLKO W "1" TURZE)
        self.can_enter_new_round = True  # jeśli false gracz przegrywa

    def __str__(self):
        report = "Player __str__ called"
        report += f"\nPlayer data:\ncards: {self.cards}\n" \
                  f"score: {self.score}\nbet: {self.bet}\nbudget: {self.budget}\nname: {self.name}\n"

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

    def win(self):
        self.budget += 2 * self.bet
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

    # SPRAWDZA CZY GRACZ MOŻE UŻYĆ SPLIT
    def can_split(self):
        if len(self.cards) >= 2:
            _, card1, _ = self.cards[0]
            _, card2, _ = self.cards[1]

            if card1 == card2 and not self.had_hit and not self.had_split and not self.had_stood:
                return True
        else:
            return False

    # SPRAWDZA CZY GRACZ MOŻE UŻYĆ DOUBLE DOWN
    def can_double_down(self):
        if not self.had_hit and not self.had_stood and not self.had_doubled:
            return True
        else:
            return False

    # SPRAWDZA CZY GRACZ MOŻE UŻYĆ INSURANCE

    # ZWYKŁA FUNKCJA

    # METODY WŁAŚCIWE

    def hit(self):
        if self.can_hit():
            self.draw()
            self.had_hit = True
        else:
            print(col.RED + 'After doubling down you cannot draw any more cards')

    def stand(self):
        self.had_stood = True

    def double_down(self):
        if self.can_double_down():
            self.set_bet(2 * self.bet)
            self.hit()
            self.had_doubled = True
        else:
            print('You cannot double down')

    def split(self):  # USTAWIA FLAGĘ
        if self.can_split():
            self.do_split = True
        else:
            print('You cannot split')

    def insure(self):
        self.insurance = 0.5 * self.bet
        self.budget -= self.insurance


class Dealer(Entity):

    def __init__(self, cards: List[Cards] = None, score=None):
        super().__init__(cards=cards, score=score)

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
        time.sleep(5)
        if self.score < 17:
            print("dealer draws!\n")
            time.sleep(3)
            self.draw()
            self.add_points()
            self.draw_until_17_or_higher()
        else:
            pass
            print(f"Dealer's final score is {self.score}\n")
