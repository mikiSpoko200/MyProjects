import classes as cl
import utility as ut
import os


Game = cl.Game()

Game.first_round()
while Game.run_game_loop():
    Game.next_round()
Game.final_round()
