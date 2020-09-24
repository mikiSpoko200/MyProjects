#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU TESTUJE KOD
#

with open('menu_console.py', 'rb') as f:
    for line in f:
        line_list = []
        for char in line:
            line_list.append("%02X" % (char))
        print(' '.join(line_list))
    f.close()