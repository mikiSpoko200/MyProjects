import classes as cl
import utility as ut
import pygame as pg


Game = cl.Game()
Game.first_round()

dude = Game.player_list[0]
Game.print_table()
dude.split()
Game.split_if_flagged()
Game.print_table()
print(ut.print_stat(dude))

