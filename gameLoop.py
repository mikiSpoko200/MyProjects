import classes as cl
import utility as ut
import os


Game = cl.Game()

fail_break = 0

Game.first_round()
while Game.run_round_loop() and fail_break < 100:
    Game.next_round()
    ut.print_player_list(Game)
Game.final_round()
