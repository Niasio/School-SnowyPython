"""
SnownyPython - Python maze game with Turtle module
Author: Jimmy F.
Date: 23/03/2021
Version: 0.1

This class allows to define the movements of the player
and to define the starting position of the variable:
characterPosition

Usage:
    N/A
Enter:
    The functions and variables of the GraphicPlan class
Results:
    Player's movements
"""

from GraphicPlan import * # Python script that has the function of drawing
    
def deplacer_gauche():
    """
    Predicts the movement of the player going left
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Left") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0], characterPosition[1] - 1) # Tupple of the calculation of the new position 
    characterPosition = deplacer(characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    if (characterPosition != None): # Allows to know if there is a position of returned (because if win, non-existent position)
        onkeypress(deplacer_gauche, "Left")
    
def deplacer_droite():
    """
    Predicts the movement of the player going right
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Right") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0], characterPosition[1] + 1) # Tupple of the calculation of the new position 
    characterPosition = deplacer(characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    if (characterPosition != None): # Allows to know if there is a position of returned (because if win, non-existent position)
        onkeypress(deplacer_droite, "Right")
    
def deplacer_haut():
    """
    Predicts the movement of the player going up
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Up") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0] - 1, characterPosition[1]) # Tupple of the calculation of the new position 
    characterPosition = deplacer(characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    if (characterPosition != None): # Allows to know if there is a position of returned (because if win, non-existent position)
        onkeypress(deplacer_haut, "Up")
    
def deplacer_bas():
    """
    Predicts the movement of the player going down
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Down") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0] + 1, characterPosition[1]) # Tupple of the calculation of the new position 
    characterPosition = deplacer(characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    if (characterPosition != None): # Allows to know if there is a position of returned (because if win, non-existent position)
        onkeypress(deplacer_bas, "Down")
    
characterPosition = POSITION_DEPART # Position of the current player