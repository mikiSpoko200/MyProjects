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

        self.losers = []
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

    def print_table(self):
        beg = "________________________________________________________\n" \
              "|\n" \
              "|    Dealer's cards:\n"

        cards = "" + add_cards_dealer(self.dealer.cards) + "\n"
        for player in self.player_list:
            cards += f"|    {player.name}'s cards:\n"
            cards += add_cards(player.cards) + "\n"

        end = "|_______________________________________________________\n"

        print(beg + cards + end)

    def print_stat(self):


    # PONIŻSZE METODY SĄ DO DOPRACOWANIA / OBGADANIA Z KIMŚ KTO OGARNIA PĘTLĘ GRY

    def first_round(self) -> None:
        for player in self.player_list:
            player.draw_hand()
        self.dealer.draw_hand()
        self.subtract_bets_from_budgets()
        self.calculate_scores()
        self.print_table()
        self.player_action_loop()


    def player_action_loop(self):
        for player in self.player_list:
            stats = "\n"
            stats += col.MAGENTA + f"{player.name}" + col.WHITE + "'s turn       " + col.MAGENTA + "(˵ ͡° ͜ʖ ͡°˵)\n"\
                + col.WHITE + f"score: {player.score}\nbet: {player.bet}\nbudget: {player.budget}\n"
            print(stats)
            self.round_menu(player)

    def calculate_scores(self):
        for player in self.player_list:
            player.calculate_score()
            if player.score > 21:
                print(col.RED + "Busted! (score > 21)")

    def enter_new_round(self):
        for player in self.player_list:
            if player.budget >= BET_MIN:
                player.budget -= player.bet
            else:
                print(f"{player.name} can't afford a new bet and is out of game!")
                self.losers.append(player)
                self.player_list.remove(player)



    def round_menu(self, player):
        print(f"{player.name}'s turn\n choose your action: ")
        if player.can_hit():
            col_code = col.GREEN
        else:
            col_code = col.RED
        print(col_code + "1) hit\n" + col.WHITE)
        if player.can_double_down():
            col_code = col.GREEN
        else:
            col_code = col.RED
        print(col_code + "2) double down\n" + col.WHITE)
        if player.can_split():
            col_code = col.GREEN
        else:
            col_code = col.RED
        print(col_code + "3) split\n" + col.WHITE)
        if player.can_insure(dealer=self.dealer):
            col_code = col.GREEN
        else:
            col_code = col.RED
        print(col_code + "4) insure\n" + col.WHITE)
        print("0) stand")

        choice = input("I choose: ")
        if choice == 1:
            player.hit()
        if choice == 2:
            player.double_down()
        if choice == 3:
            player.split()
        if choice == 4:
            pass
        if choice == 0:
            player.stand()

    def subtract_bets_from_budgets(self):  # OBLICZA BUDŻET PO ODJĘCIU ZAKŁĄDU (PRZY WEJŚCIU DO NOWEJ RUNDY)
        for player in self.player_list:
            player.budget -= player.bet
            self.player_list.remove(player)

    def check_budgets(self):  # SPRAWDZA CZY GRACZA STAĆ NA WEJŚCIE DO NOWEJ RUNDY
        for player in self.player_list:
            if player.budget <= player.bet:  # POWINNO BYĆ <= min_bet (zakład ma jakąś minimalną wartość)
                Player.can_enter_new_round = False
                print(f"{player.name} is broken!")

    def after_each_move(self):
        raise NotImplementedError

    # def calculate_round_outcome(self):

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
                self.player_list.pop(player_index)
                self.player_list.insert(player_index, hands[0])
                self.player_list.insert(player_index + 1, hands[1])
            else:
                pass


class Entity(object):  # KLASA MACIERZYSTA DLA KLAS PLAYER I DEALER

    def __init__(self, cards=None, score=0):
        self.cards = cards if cards is not None else []
        self.score = score

    def calculate_score(self):
        self.score = 0
        for card in self.cards:
            _, point, _ = card
            self.score += point

    def draw(self):
        self.cards.append(DECK.pop(0))

    def draw_hand(self):
        self.draw()
        self.draw()


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

    def set_bet(self, new_bet=None):
        if new_bet is None:
            new_bet = input(col.GREEN + "Input new bet value: \n")

        if self.budget >= new_bet >= BET_MIN:
            self.bet = new_bet
        else:
            print(col.RED + "You cannot set your bet to that value\n")

    # METODY SPRAWDZAJĄCE:

    def can_hit(self):
        if not self.had_doubled and not self.had_stood:
            return True
        else:
            return False

    # SPRAWDZA CZY GRACZ MOŻE UŻYĆ SPLIT
    def can_split(self):
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

    def can_insure(self, dealer):
        if can_insure(dealer=dealer) and self.budget >= 0.5 * self.bet:
            self.insurance = 0.5 * self.bet
            self.budget -= self.insurance

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


class Dealer(Entity):

    def __init__(self, cards: List[Cards] = None, score=None):
        super().__init__(cards=cards, score=score)

    def check_for_ace(self):
        if self.get_visible_card()[0] == 'Ace':
            return True
        else:
            return False

    def get_visible_card(self):
        return self.cards[0]

    def check_if_score_higher_than_or_eq_to_17(self):
        if self.score >= 17:
            return True
        else:
            return False
