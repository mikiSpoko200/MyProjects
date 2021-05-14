#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import uuid
import random
import time
import webbrowser
from datetime import datetime


class Table:
    def __init__(self, url):
        self.url = url
        random.seed(123210912)
        a = "%32x" % random.getrandbits(128)
        rd = a[:12] + '4' + a[13:16] + 'a' + a[17:]
        self.id = uuid.UUID(rd).int
        self.scrape_and_parse()

    def scrape_and_parse(self):
        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(self.url).text

        # Parse the html content
        soup = BeautifulSoup(html_content, "lxml")
        title = soup.find('title').text
        title = title[:title.index("(")]
        self.name = title.strip()
        to_string = soup.get_text()
        to_list = to_string.split("\n")
        to_list = [elem.strip() for elem in to_list]
        to_list = [elem for elem in to_list if elem]

        kolejka = [index for index, elem in enumerate(to_list) if elem == "Kolejka"][1]
        uwaga = [index for index, elem in enumerate(to_list) if elem == "UWAGA!"][1]
        to_list = [elem for index, elem in enumerate(to_list) if kolejka < index < uwaga]

        num_p = 0

        for elem in to_list:
            if elem == '+':
                num_p += 1
        try:
            if "zaaw" in to_list:
                to_list.remove("zaaw")
            for i in range(3, len(to_list)-num_p, 5):
                if to_list[i] == "+":
                    to_list[i-1] = f"{to_list[i-1]} + {to_list[i+1]}"
                    to_list[i:] = to_list[i+2:]

            to_list = [[elem for elem in to_list[i:i + 5]] for i in range(0, len(to_list), 5)]
            self.parsed_data = to_list
        except IndexError:
            print('WYJEBAŁO PARSER COŚ MOGLI ZMIENIĆ!')
            webbrowser.open('https://www.youtube.com/watch?v=gnrgCtb4dKs&ab_channel=YourQuestionsAnswered')

    def check_for_new_groups(self):
        new_n = len(self.parsed_data)
        print(f"Aktualna ilość grup {self.name} : {new_n}")
        return new_n

    def gen_table(self):

        table = '<table class="container">\n'
        table += '  <thead>\n'
        table += f'    <h1><span class ="yellow">{self.name}</span></h1>\n'
        header = ["Prowadzący", "Termin zajęć", "Limit", "Zapisani", "Kolejka"]
        table += "    <tr>\n"
        for column in header:
            table += f"      <th><h1>{column}</h1></th>\n"
        table += "    </tr>\n"
        table += '  </thead>\n'

        table += '  <tbody>\n'
        for row in self.parsed_data:
            if row[-1] in [str(num) for num in range(1, 6)]:
                table += '    <tr style="color : orange">\n'
            elif row[-1] == '0':
                table += '    <tr style="color : green">\n'
            else:
                table += '    <tr style="color : #FB667A">\n'
            for column in row:
                table += f"      <td>{column}</td>\n"
            table += "    </tr>\n"
        table += '  </tbody>\n'
        table += "</table>"

        return table

    def __str__(self):
        return self.gen_table()


def gen_html(css_dir=None):
    with open("index.html", "w", encoding="utf-8") as html:
        if not os.path.getsize("index.html"):

            html.write(
                f'<!DOCTYPE html>\n'
                '<html lang="en">\n'
                '<head>\n'
                '  <meta charset="UTF-8">\n'
                '  <title>System Zapisów</title>\n')
            if css_dir:
                html.write(f'  <link rel="stylesheet" href="{css_dir}">\n')
            html.write(
               f'</head>\n'
                '<body>\n'
                '  <h1><span class="blue">&lt;</span>System<span class="blue">&gt;</span> <span class="yellow">Zapisów</span></h1>\n'
                '  <h2>CSS and HTML stolen from <a href="https://github.com/pablorgarcia" target="_blank">Pablo García</a></h2>\n'
                '<!-- insert_tab -->\n'
                '</body>\n'
                '</html>\n')

# TODO: path URL validation, id verification, utilize pickle


def add_table_to_html(ulr):
    table = Table(ulr)
    with open("index.html", "r", encoding="utf-8") as html:
        html_as_list = html.read().split("\n")
        insertion_index = html_as_list.index('<!-- insert_tab -->')
        html_as_list.pop(insertion_index)
        html_as_list.insert(insertion_index, str(table))
        html_as_list.insert(insertion_index + 1, "<br/>")
        html_as_list.insert(insertion_index + 2, "<!-- insert_tab -->")
        with open("index.html", "w", encoding="utf-8") as new_html:
            new_content = "\n".join([elem for elem in html_as_list if elem])
            new_html.write(new_content)


def add_tables(*args):
    for table in args:
        add_table_to_html(table)


def clear():
    os.system('cls')


def main():
    gen_html("style.css")
    url_ask = "https://zapisy.ii.uni.wroc.pl/courses/architektury-systemow-komputerowych-202021-letni"
    url_bazy = "https://zapisy.ii.uni.wroc.pl/courses/bazy-danych-202021-letni"
    url_net = "https://zapisy.ii.uni.wroc.pl/courses/kurs-programowania-pod-windows-w-technologii-net-202021-letni"
    url_met = "https://zapisy.ii.uni.wroc.pl/courses/metody-programowania-202021-letni"
    url_si = "https://zapisy.ii.uni.wroc.pl/courses/sztuczna-inteligencja-202021-letni"

    ig_ask = 5
    ig_si = 6
    ig_net = 2
    iterations = 1
    now = datetime.now()
    while True:
        t_ask = Table(url_ask)
        t_si = Table(url_si)
        t_net = Table(url_net)
        print(f"Program rozpoczął pracę o {now.hour}:{now.minute}:{now.second}\nIteracja {iterations} :\n")
        curr_ask = t_ask.check_for_new_groups()
        curr_si = t_si.check_for_new_groups()
        curr_net = t_net.check_for_new_groups()

        if curr_ask != ig_ask:
            print('NOWA GRUPA ASK!')
            webbrowser.open('https://www.youtube.com/watch?v=gnrgCtb4dKs&ab_channel=YourQuestionsAnswered')
        if curr_si != ig_si:
            print('NOWA GRUPA SI!')
            webbrowser.open('https://www.youtube.com/watch?v=gnrgCtb4dKs&ab_channel=YourQuestionsAnswered')
        if curr_net != ig_net:
            print('NOWA GRUPA .NET!')
            webbrowser.open('https://www.youtube.com/watch?v=gnrgCtb4dKs&ab_channel=YourQuestionsAnswered')

        time.sleep(20)
        clear()
        iterations += 1


main()
