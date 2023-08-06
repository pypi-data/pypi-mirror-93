import colorama
import random
import curses
from curses import *
noecho()
initscr()

def createWindow(height, width, x, y):
    win = newwin(height, width, x, y)
    return win

def Border(win):
    win.border()

def addString(String, win, Type, x, y):
    if Type == False:
        win.addstr(x, y, String)
    if Type != False:
        win.addstr(x, y, String, Type)

def addColorString(String, win, x, y, colorPAIR):
    win.addstr(x, y, String, colorPAIR)


