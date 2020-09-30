#!/usr/bin/python
# -*- coding: utf-8 -*-

import TwentyFortyEight.engine as eng
import tkinter as tk
import numpy as np

a = np.array([[1,2,3], [4,5,6], [7,8,9]])
b = np.array([[1,2,3], [4,6,6], [7,8,9]])
comp = a == b
print(comp.any())
