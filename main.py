"""
SnownyPython - Python maze game with Turtle module
Author: Jimmy F.
Date: 23/03/2021
Version: 0.1

This class allows to execute the game
"""

from Character import *

listen() #Allows you to listen to what the player is going to type on his keyboard

#Definition of keys with movement functions
onkeypress(deplacer_gauche, "Left") 
onkeypress(deplacer_droite, "Right")
onkeypress(deplacer_haut, "Up")
onkeypress(deplacer_bas, "Down")

mainloop() #Tells the window to wait for the user to do something,
           #although in this case there’s not much for the user to do except close the window