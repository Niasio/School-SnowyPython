from GraphicPlan import *
    
def deplacer_gauche():
    """
    Predicts the movement of the player going left
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Left") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0], characterPosition[1] - 1) # Tupple of the calculation of the new position 
    characterPosition = deplacer(MATRICE, characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    onkeypress(deplacer_gauche, "Left")
    
def deplacer_droite():
    """
    Predicts the movement of the player going right
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Right") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0], characterPosition[1] + 1) # Tupple of the calculation of the new position 
    characterPosition = deplacer(MATRICE, characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    onkeypress(deplacer_droite, "Right")
    
def deplacer_haut():
    """
    Predicts the movement of the player going up
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Up") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0] - 1, characterPosition[1]) # Tupple of the calculation of the new position 
    characterPosition = deplacer(MATRICE, characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    onkeypress(deplacer_haut, "Up")
    
def deplacer_bas():
    """
    Predicts the movement of the player going down
    """
    global characterPosition # Position of the current player,
                             # it must be declared in global because otherwise it cannot be modified
    
    onkeypress(None, "Down") # Allows to block the command in case of prolonged pressure, it avoids errors
    
    newPosition = (characterPosition[0] + 1, characterPosition[1]) # Tupple of the calculation of the new position 
    characterPosition = deplacer(MATRICE, characterPosition, newPosition) # We redefine here by a tupple the position of the character
    
    onkeypress(deplacer_bas, "Down")

characterPosition = POSITION_DEPART # Position of the current player