import sys

from ttt import tttai

print("Welcome to Tic Tac Toe by Lux!")

if "--pvp" in sys.argv or "-p" in sys.argv:
    tttai.Board().pvp()
    exit()

if "--pve" in sys.argv or "-e" in sys.argv:
    tttai.Board().pve()
    exit()

PvE = "pve"
PvP = "pvp"

selection = None

while True:
    selection = input("PvE or PvP? (enter your choice): ")
    if selection == PvE:
        tttai.Board().pve()
        exit()
    elif selection == PvP:
        tttai.Board().pvp()
        exit()
    else:
        print("Not a valid input, try again.")