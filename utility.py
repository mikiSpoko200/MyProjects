#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU PLANUJE DODAWAĆ FUNKCJE, KTÓRE MAJĄ UŁATWIĆ MI TESTOWANIE KODU
#

import resources

import colours as col


def print_player_list(game):
    for i in range(0, resources.NUM_PLAYERS):
        print(game.player_list[i])


def card_to_string(card):
    value = card[0]
    colour = card[2]
    colour_to_ASCII = {"Spade": "♠", "Heart": "♥", "Diamond": "♦", "Club": "♣"}
    value_to_ASCII = {"Ace": "A", "Jack": "J", "Queen": "Q", "King": "K", "2": "2", "3": "3",
                      "4": "4", "5": "5", '6': "6", '7': "7", '8': "8", '9': "9", '10': "10"}
    colour_in_ASCII = colour_to_ASCII[colour]
    value_in_ASCII = value_to_ASCII[value]
    if value_in_ASCII != "10":
        return f"|‾‾‾|\n" \
               f"|{value_in_ASCII}{colour_in_ASCII} |\n" \
               f"|___|\n"
    else:
        return f"|‾‾‾|\n" \
               f"|{value_in_ASCII}{colour_in_ASCII}|\n" \
               f"|___|\n"


def add_cards_dealer(cards):
    modified_cards = [cards[0], "|\‾/|\n"
                                "| X |\n"
                                "|/_\|\n"]
    return add_cards(modified_cards)


def add_cards(cards):

    cards_str = []
    for card in cards:
        if type(card) == tuple:
            cards_str.append(card_to_string(card))
        else:
            cards_str.append(card)

    added_cards = "|    "
    for card in cards_str:
        added_cards += card[0:5] + "  "
    added_cards += "\n|    "
    for card in cards_str:
        added_cards += card[6:11] + "  "
    added_cards += "\n|    "
    for card in cards_str:
        added_cards += card[12:17] + "  "
    added_cards += "\n|    "
    return added_cards


