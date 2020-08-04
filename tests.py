#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU TESTUJE KOD
#

# import classes as cl
#
# game = cl.Game()
# game.dealer.cards.append(('6', 6, 'Diamond'))
# game.dealer.cards.append(('7', 7, 'Diamond'))
# print(cl.add_cards(game.dealer.cards))

a = [x for x in range(1,6)]
print(a)
for elem in a:
    if elem == 3:
        a.remove(elem)
    else:
        pass

print(a)