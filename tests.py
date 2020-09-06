#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU TESTUJE KOD
#

import pygame
import pickle
#from logic import Cards
from menu_kon import Menu_kon
from classes import Game
import resources as rsrc
#from classes import can_insure

#from classes import Deck
width_w = 1000
height_w = 700

def center_text(text, list):
    x = list[0]
    y = list[1]
    w = list[2]
    h = list[3]
    return text.get_rect(center=(int(x + 0.5 * w), int(y + 0.5 * h)))


class Interface_GUI():
    def __del__(self):
        print("interface usuniety")
    def __init__(self, num_decks, hotseat, window, time, bet):
        self.num_decks = num_decks
        self.hotseat = hotseat
        self.time_left = time
        self.bet = bet
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 25)#('Arial', 25)
        self.font_arrow = pygame.font.Font("OpenSans-Regular.ttf", 20)#pygame.font.SysFont('Arial', 20)
        self.font_color = (0, 0, 0)
        self.basic_col = (29, 59, 207)
        self.bet_col = (29, 186, 207)
        self.time_col = (29, 207, 56)
        self.grey = (192, 192, 192)
        self.width_rect = 100
        self.height_rect = 50
        self.width_card = 80
        self.center_x = int((width_w - self.width_rect) / 2)
        self.dist = 50
        self.can_click = False
        self.load_it = 0

        self.y = height_w - self.dist - self.height_rect;
        self.x_start = int((width_w - 5 * self.width_rect - 4 * self.dist)/2)
        self.x_hit = self.x_start
        self.x_stand = self.x_start + self.dist + self.width_rect
        self.x_double = self.x_start + 2*(self.dist + self.width_rect)
        self.x_split = self.x_start + 3*(self.dist + self.width_rect)
        self.x_insure = self.x_start + 4*(self.dist + self.width_rect)

        self.button_back = pygame.Rect(self.dist, self.dist, self.width_rect+50, self.height_rect)
        self.button_hit = pygame.Rect(self.x_hit, self.y, self.width_rect, self.height_rect)
        self.button_stand = pygame.Rect(self.x_stand, self.y, self.width_rect, self.height_rect)
        self.button_double = pygame.Rect(self.x_double, self.y, self.width_rect, self.height_rect)
        self.button_split = pygame.Rect(self.x_split, self.y, self.width_rect, self.height_rect)
        self.button_time = pygame.Rect(950-self.dist-self.width_rect, self.dist, self.width_rect+50, self.height_rect)
        self.button_insure = pygame.Rect(self.x_insure, self.y, self.width_rect, self.height_rect)
        self.button_bet = pygame.Rect(self.x_double, self.y - self.dist - self.height_rect, self.width_rect, self.height_rect)
        self.button_player = pygame.Rect(self.x_double, self.y - self.dist - 2*self.height_rect, self.width_rect, self.height_rect)
#        self.cards = Cards(self.num_decks)
        self.it_x = 0
        self.it_y = 0
        self.odslon = False
        self.in_split = False
        self.game = Game()
        self.game.first_round()
        self.game.first_turn()
        print(self.game)
        self.current_player = self.game.pllst[0]
        self.split_bust = [-1,-1,-1,-1,-1,-1,-1,-1]



    def draw(self, window):
        self.basic_col = (29, 59, 207) if self.can_click else (192, 192, 192)
        hit_col = self.basic_col
        stand_col = self.basic_col
        if len(self.current_player.hands_nt) == 0:
            double_col = self.grey
            split_col = self.grey
            insure_col = self.grey
        else:
            double_col = self.basic_col if self.current_player.hands_nt[0].can_DD() else self.grey
            split_col = self.basic_col if self.current_player.hands_nt[0].can_split() else self.grey
            insure_col = self.basic_col if self.current_player.hands_nt[0].can_insure(self.game.dealer) else self.grey

        if self.load_it > 1:
            pygame.draw.rect(window, hit_col, self.button_back)
            text_back = self.font.render("Undo move", True, self.font_color)
            window.blit(text_back, center_text(text_back, self.button_back))

        pygame.draw.rect(window, hit_col, self.button_hit)
        pygame.draw.rect(window, stand_col, self.button_stand)
        pygame.draw.rect(window, double_col, self.button_double)
        pygame.draw.rect(window, split_col, self.button_split)
        pygame.draw.rect(window, insure_col, self.button_insure)
        pygame.draw.rect(window, self.bet_col, self.button_bet)

        def create_text(text, antialias=True, colour=self.font_color):
            return self.font.render(text, antialias, colour)

        text_hit = create_text("Hit")
        text_stand = create_text("Stand")
        text_double = create_text("Double")
        text_split = create_text("Split")
        text_insure = create_text("Insure")
        text_bet = create_text(str(self.bet) + "$")
        text_player = create_text(self.current_player.name)

        text_time = create_text("0 s left" if self.time_left <= 0 else f"{self.time_left:.2f} s left")

        if self.hotseat:
            pygame.draw.rect(window, self.time_col, self.button_time)
            window.blit(text_time, center_text(text_time, self.button_time))
        window.blit(text_hit, center_text(text_hit, self.button_hit))
        window.blit(text_stand, center_text(text_stand, self.button_stand))
        window.blit(text_double, center_text(text_double, self.button_double))
        window.blit(text_split, center_text(text_split, self.button_split))
        window.blit(text_insure, center_text(text_insure, self.button_insure))
        window.blit(text_bet, center_text(text_bet, self.button_bet))
        window.blit(text_player, center_text(text_player, self.button_player))
        #print("d")
        #pygame.display.flip()
        #self.update_cards(window)#false

    def check_all_buttons(self, pos, window):

        if self.can_click:
            self.basic_col = (29, 59, 207)
            print(self.load_it)
            if self.load_it > 1 and self.click(self.button_back, pos[0], pos[1]):
                print("undo")
                return "undo"

            player = self.current_player
            hand = self.current_player.hands_nt[0]

            elif self.click(self.button_hit, pos[0], pos[1]):
                print("Hit")
                # if self.cards.in_split:
                #     self.cards.hit_split()
                # else:
                self.current_player.hit(hand, self.game.draw)
                    #busted = self.cards.hit()
                    #if busted:
                        #self.update_cards(window)
                        #self.cards.odslon = True
                        #print('test')
                        #menu_kon = Menu_kon(0, 1, window)
                        #return ("end_busted", menu_kon)
                return "hit"

            elif self.click(self.button_stand, pos[0], pos[1]):
                print("Stand")
                self.game.pllst[self.current_player].stand(self.game.pllst[self.current_player].hands_nt[0])
                #else:
                #krupier = self.cards.krupier()
                #self.cards.odslon = True
                #self.update_cards(window) ####################
                #menu_kon = Menu_kon(krupier[0], krupier[1], window)
                #return ("end", )#menu_kon)
            elif self.current_player.hands_nt[0].can_split() and self.click(self.button_split, pos[0], pos[1]):
                print("Split")
                self.current_player.split(self.game.pllst[self.current_player].hands_nt[0])
                print(self.game)
            elif self.current_player.hands_nt[0].can_DD() and self.click(self.button_double, pos[0], pos[1]):
                print("Double")
                self.current_player.DD(self.game.pllst[self.current_player].hands_nt[0],  self.game.draw)
            elif self.current_player.hands_nt[0].can_insure(self.game.dealer) and self.click(self.button_insure, pos[0], pos[1]):
                print("insure")
                self.current_player.insure(self.game.pllst[self.current_player].hands_nt[0])
            else:
                return "nothing_clicked"
        else:
            return "nothing_clicked"
            self.basic_col = (192, 192,192)
        #self.update_cards(window)
        return ("", "")


    def click(self, button, x, y):
        if button.x < x < button.x + button.w and button.y < y < button.y + button.h:
            return True

    def update_cards(self, window, it):
        self.game.pllst[self.current_player].choice_processing_functions()
        self.can_click = False
        x_0 = 0
        split = len(self.game.pllst[self.current_player].hands_nt) + len(
            self.game.pllst[self.current_player].hands_busted) + len(
            self.game.pllst[self.current_player].hands_stand) == 2
        if split and len(self.game.pllst[self.current_player].hands_nt) == 1:
            self.split_bust[self.current_player] = self.game.pllst[self.current_player].hands_busted
        #print(self.game.pllst[self.current_player].hands_nt[0].cards)
        if split:
            if len(self.game.pllst[self.current_player].hands_nt) == 0:
                if self.split_bust[self.current_player]:
                    talia = self.game.pllst[self.current_player].hands_busted[0].cards
                else:
                    talia = self.game.pllst[self.current_player].hands_stand[0].cards
            elif len(self.game.pllst[self.current_player].hands_nt) == 1:
                if self.split_bust[self.current_player]:
                    talia = self.game.pllst[self.current_player].hands_busted[0].cards
                else:
                    talia = self.game.pllst[self.current_player].hands_stand[0].cards
            else:
                talia = self.game.pllst[self.current_player].hands_nt[0].cards
        elif len(self.game.pllst[self.current_player].hands_busted) == 1:
            talia = self.game.pllst[self.current_player].hands_busted[0].cards
        elif len(self.game.pllst[self.current_player].hands_nt) == 1:
            talia = self.game.pllst[self.current_player].hands_nt[0].cards
        else:
            talia = self.game.pllst[self.current_player].hands_stand[0].cards
        while x_0 < len(talia) and x_0 <it:
            x = talia[x_0]
            #print(x)
            if split and len(self.game.pllst[self.current_player].hands_nt) == 1:
                nazwa_pliku = x[0] + "_" + x[2] + "_g.png"
            else:nazwa_pliku = x[0] + "_" + x[2] + ".png"
            #nazwa_pliku = x[0] + "_" + x[2] + ".png"
            #print(nazwa_pliku)
            img = pygame.image.load(nazwa_pliku)
            if split:
                x_start = 665
                window.blit(img,
                            (int(600 + (((x_0 + 1) * 2) - 1) * 300 / (len(talia) * 2) - 0.5 * self.width_card),
                             350))
            else:
                x_start = 425
                window.blit(img,
                            (int(200 + (((x_0 + 1) * 2) - 1) * 600 / (len(talia) * 2) - 0.5 * self.width_card),
                             350))

            #window.blit(img, (x_start + (x_0 * 80), 350 ))
            if self.it_x == x_0:
                #pygame.time.wait(1000)
                self.it_x += 1
            #pygame.display.update(0, self.y/2, width_w, self.y/2)
            x_0 += 1

        s_0 = 0

        if len(self.game.pllst[self.current_player].hands_nt) == 2:
            cards_split = self.game.pllst[self.current_player].hands_nt[1].cards
        elif split:
            if len(self.game.pllst[self.current_player].hands_nt) == 1:
                cards_split = self.game.pllst[self.current_player].hands_nt[0].cards
            elif len(self.game.pllst[self.current_player].hands_busted) == 2:
                cards_split = self.game.pllst[self.current_player].hands_busted[1].cards
            elif len(self.game.pllst[self.current_player].hands_stand) == 2:
                cards_split = self.game.pllst[self.current_player].hands_stand[1].cards
            elif self.split_bust[self.current_player]:
                cards_split = self.game.pllst[self.current_player].hands_stand[1].cards
        else:
            cards_split = []


        while s_0 < len(cards_split) and s_0 + x_0 < it:    ##################
            x = cards_split[s_0]
            # print(it)
            if len(self.game.pllst[self.current_player].hands_nt) == 2:
                nazwa_pliku = x[0] + "_" + x[2] + "_g.png"
            else:
                nazwa_pliku = x[0] + "_" + x[2] + ".png"
            # print(nazwa_pliku)
            img = pygame.image.load(nazwa_pliku)

            window.blit(img,
                        (int(100 + (((s_0 + 1) * 2) - 1) * 300 / (len(cards_split) * 2) - 0.5 * self.width_card), 350))
            #window.blit(img, (170 + (s_0 * 80), 350))
            # if self.it_x == x_0:
            # pygame.time.wait(1000)
            #   self.it_x += 1
            # pygame.display.update(0, self.y/2, width_w, self.y/2)
            s_0 += 1

            #print(x)
        #print("")
        #pygame.time.wait(1000)
        y_0 = 0
        len_dealer = len(self.game.dealer.hand.cards)
        while y_0 < len_dealer and s_0 + y_0 + x_0 <it:
            y = self.game.dealer.hand.cards[y_0]
            nazwa_pliku = y[0] + "_" + y[2] + ".png"
            #print(nazwa_pliku)
            if not self.odslon and len(self.game.dealer.hand.cards) == 2 and y_0 == 1:
                window.blit(pygame.image.load("tyl.png"), (int(100 + (((y_0+1)*2)-1)*800/(len_dealer*2)-0.5*self.width_card), 100))
                #window.blit(pygame.image.load("tyl.png"), (425 + (y_0 * 80), 100))
            else:
                #window.blit(pygame.image.load(nazwa_pliku), (425 + (y_0 * 80), 100))
                window.blit(pygame.image.load(nazwa_pliku), (int(100 +(((y_0+1)*2)-1) * 800 / (len_dealer * 2) - 0.5 * self.width_card), 100))
            if self.it_y == y_0:
                #pygame.time.wait(1000)
                #print("xd")
                self.it_y += 1
            #pygame.display.update(0, 0, width_w, self.y/2)
            y_0 += 1
        #print(self.cards.talia_krupiera)



        if y_0 == len(self.game.dealer.hand.cards):
            self.can_click = True
            #print(y)


