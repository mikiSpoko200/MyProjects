#!/usr/bin/python
# -*- coding: utf-8 -*-

class foo:
    def __init__(self):
        self.a = 1

    def __str__(self):
        return "__str__() of foo called"


class bar(foo):
    def __init__(self):
        super().__init__()
        self.b = 2

    def __str__(self):
        return "__str__() of bar called"


A = foo()
B = bar()


print(A.__class__.__name__)
print(B.__class__.__name__)

a = str(A)
print(str(B) + a)