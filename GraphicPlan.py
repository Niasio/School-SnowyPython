"""
SnownyPython - Python maze game with Turtle module
Author: Jimmy F.
Date: 23/03/2021
Version: 0.1

This class allows to manage all the aspect of the graph,
drawing and events for the player. The variables are contained here:
Matrix, Pas, TotalObjCollect, DictQuestions, DictObjets, coordInventaire

Usage:
    N/A
Enter:
    Character functions and decoded files
Results:
    The Graph
"""

from CONFIGS import * # All constant variables
from turtle import * # Turtle Python Module
from enum import Enum # Allows you to create the enum of the cells
from FileDecoding import * # Python script that decodes the files
from Character import * # Python script that takes care of the character's movements

def calculer_pas(matrice):
    """
    Calculates the size to be given to the cells so that the plan fits in the area of the window
    matrice: 2D List | Plan matrix
    Example: calculer_pas([[1,0,1,1],[0,0,1,0]]) = 72.5
    Returns: Float | Size
    """
    height = len(matrice) # Height of the game plan
    width = len(matrice[0]) # Width of the game plan
    
    maxWidth = abs(ZONE_PLAN_MINI[0]) + abs(ZONE_PLAN_MAXI[0]) # Maximum width of the plane in Turtle coordinate
    maxHeight = abs(ZONE_PLAN_MINI[1]) + abs(ZONE_PLAN_MAXI[1]) # Maximum height of the plane in Turtle coordinate
    
    return min(maxWidth/width,maxHeight/height)

def coordonnes(case, pas):
    """
    Calculates the coordinates (in pixels) of the lower left corner of a cell
    case: Tuple | Number of the cell
    pas: Float | Dimension of the square
    Example: coordonnes((1,5), 72.5) = (122.5, 55.0)
    Returns: Tuple | Coordinates
    """
    realCoord = [] # List of x ; y coordinates,
                   # we first put it in list because the tuple is an immutable object
    
    realCoord.append(ZONE_PLAN_MINI[0] + case[1] * pas)
    realCoord.append(ZONE_PLAN_MAXI[1] - pas - case[0] * pas)
        
    return tuple(realCoord)

def tracer_carre(dimension):
    """
    Allows you to draw a square with the Turtle "squarePencil"
    dimension: Float | Dimension of the square
    Example: tracer_carre(15) --> Draw a square of 15 pixels on the window
    """
    squarePencil.begin_fill()
    for i in range(4): # In range 4 allows to draw the 4 sides of the square
        squarePencil.forward(dimension)
        squarePencil.left(90)
    squarePencil.end_fill()
        
def tracer_case(case, couleur, pas):
    """
    Place the Turtle in the right position and prepare the right color of the square
    case: Tuple | Number of the cell
    couleur: String | Color of the cell
    pas: Float | Dimension of the square
    Example: tracer_case((1,5), "red", 15) --> Draw the (1,5) red cell of a 15 pixel square
    """
    coord = coordonnes(case,pas) # Tuple who will have the real Turtle coordinates
    
    squarePencil.color("black",couleur) # black = side color
                                        # couleur = color of filling

    squarePencil.up()
    squarePencil.goto(coord[0],coord[1])
    squarePencil.down()
    
    tracer_carre(pas)
    
def afficher_plan(matrice):
    """
    Display the plan
    matrice: 2D List | Plan matrix
    Example: afficher_plan([[1,0,1,1],[0,0,1,0]]) --> Allows to display the whole plan thanks to the matrix
    """
    for i in range(len(matrice)): # Each row
        for j in range(len(matrice[i])): # Each column
            tracer_case((i,j), COULEURS[matrice[i][j]], Pas)
            
    #TurtleScreen update
    update()
    
def deplacer(position, mouvement):
    """
    Allows to move the counter to the desired square, redraws the counter
    position: Tuple | Player's position
    mouvement: Tuple | Next player position
    Example: deplacer((1,5), (1,6)) = (1,5) or (1,6) if the move is possible
    Returns: Tuple | Player position (changed or unchanged)
    """
    if(isWin(position)): # If the player is on the victory cell.
        onkeypress(None, "Left")
        onkeypress(None, "Right")
        onkeypress(None, "Up")
        onkeypress(None, "Down")
        
        bye() # Bye bye Turtle
        return None
    elif(isFree(mouvement)): # If the player can move
        characterDot.clear() # Poof, the character disappears!
    
        coordMouvement = coordonnes(mouvement, Pas) # Tupple of the new Turtle real player coordinate
    
        characterDot.up()
        characterDot.goto(coordMouvement[0] + Pas/2, coordMouvement[1] + Pas/2) # Divide by 2 to get to the middle
        characterDot.down()
        characterDot.dot(Pas * RATIO_PERSONNAGE, COULEUR_PERSONNAGE)
    
        update()
    
        return mouvement
    else: # The player cannot move
        return position
    
def isFree(cell):
    """
    Allows to know if a cell is available to move or not.
    Launch a specific function for a certain type of cell.
    cell: Tuple | Number of the cell
    Example: isFree((1,5)) = True - If free cell for the character
    Returns: Boolean | Indicates if the player can move.
    """
    try:
        typeOfCase = Matrix[cell[0]][cell[1]] # Integer which will have the number of the type of cell
    except: # In case the player tries to go outside the plan
        return False
    
    if (typeOfCase == Case.EMPTY.value): # 0 = Empty cell
        return True
    elif (typeOfCase == Case.VICTORY.value): # 2 = Exit / victory cell
        win_game()
        return True
    elif (typeOfCase == Case.DOOR.value): # 3 = Door cell
        if(poser_question(cell)):
            return True
        else:
            return False
    elif (typeOfCase == Case.OBJECT.value): # 4 = Object cell
        ramasser_objet(cell)
        return True
    else: # Other, wall (=1) for example
        return False
    
def ramasser_objet(cell):
    """
    Allows you to pick up an item, display it in the inventory
    cell: Tuple | Number of the cell
    Example: ramasser_objet((1,6)) --> Allows to write next to the plan the recovered object
    """
    global TotalObjCollect # Total number of collected objects,
                           # allows the display of the object number,
                           # global to allow its modification
    
    try: # We manage if the cell does not exist in the dictionary
        inventaire.up()
        inventaire.goto(coordInventaire[0],coordInventaire[1] - 15 * TotalObjCollect) # We remove -15 to simulate a line break
        inventaire.down()
        inventaire.write("N°" + str(TotalObjCollect+1) + ": " + DictObjets[cell], font=("Verdana", 10, "normal"))
    
        annonce.clear()
        annonce.write("Vous avez trouvé: " + DictObjets[cell], font=("Verdana", 12, "bold")) # We display the announce

        TotalObjCollect += 1
    
        tracer_case(cell, COULEUR_CASES, Pas)
        Matrix[cell[0]][cell[1]] = 0 # We redefine the cell to 0 because now empty
    except:
        print("ERROR - No objects assigned to this cell!")
    
def poser_question(case):
    """
    Ask a question to the player and return if the answer is correct or not
    case: Tuple | Number of the cell
    Example: poser_question((1,5)) = True - If the player has answered the question correctly
    Returns: Boolean | Indicates whether the answer is correct or not
    """
    try: # We manage if the cell does not exist in the dictionary
        annonce.clear()
        annonce.write("Cette porte est fermée.", font=("Verdana", 12, "bold"))
    
        reponse = textinput("Porte", DictQuestions[case][0]) # Will contain the player's answer in string
        listen() # Allows you to listen to the commands again, because stopped by the question
    
        if(reponse == DictQuestions[case][1]): # If the answer is correct
            tracer_case(case, COULEUR_CASES, Pas)
            Matrix[case[0]][case[1]] = 0 # We redefine the cell to 0 because now empty
        
            annonce.clear()
            annonce.write("La porte s'ouvre", font=("Verdana", 12, "bold"))
        
            return True
        else: # If the answer is wrong
            annonce.clear()
            annonce.write("Mauvaise réponse", font=("Verdana", 12, "bold"))
            return False
    except:
        print("ERROR - No door assigned to this cell, return False!")
        return False
    
def win_game():
    """
    Shows the player that he has won
    Example: win_game() --> Tells the player that he has won
    """
    annonce.clear()
    annonce.write("Vous avez gagné !! Bravo, c'est la fête :D", font=("Verdana", 12, "bold"))
    
def isWin(cell):
    """
    Allows to know if the cell is the one of victory
    cell: Tuple | Number of the cell
    Exemple: isWin((1,5)) = True - If the player is on the winning cell
    Returns: Boolean | Tells if the player is on the victory cell or not
    """
    if (Matrix[cell[0]][cell[1]] == Case.VICTORY.value): # 2 = Exit / victory cell
        return True
    else:
        return False
    
class Case(Enum):
    """
    Enumeration of the cells, allows not to make mistakes when using these types.
    Example: Case.DOOR.value = 3
    """
    EMPTY = 0
    WALL = 1
    VICTORY = 2
    DOOR = 3
    OBJECT = 4
    
#Turtle animation off
#We do this to save a lot of time
tracer(0, 0)

squarePencil = Turtle() # Creation of the turtle to draw the squares
squarePencil.ht()
squarePencil.speed(10)

characterDot = Turtle() # Turtle that will be given to the player
characterDot.ht()

inventaire = Turtle() # Turtle assigned to inventory display
inventaire.ht()
inventaire.up()
inventaire.goto(POINT_AFFICHAGE_INVENTAIRE[0],POINT_AFFICHAGE_INVENTAIRE[1])
inventaire.down()
inventaire.write("Inventaire", font=("Verdana", 10, "bold"))

annonce = Turtle() # Turtle assigned to display announcements.
annonce.ht()
annonce.up()
annonce.goto(POINT_AFFICHAGE_ANNONCES[0],POINT_AFFICHAGE_ANNONCES[1])
annonce.down()
    
Matrix = lire_matrice(fichier_plan) # 2D list that contains all the values of the game cells
Pas = calculer_pas(Matrix) # Float of the gap between each square (= 1 side of a square)
TotalObjCollect = 0 # Total number of collected objects
DictObjets = creer_dictionnaire(fichier_objets) # Object dictionary, format = cell:object (tuple:string)
DictQuestions = creer_dictionnaire(fichier_questions) # Questions dictionary, format = cell:answer (tuple:string)
coordInventaire = (POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - 15) # Real Turtle coordinate of the first line of the inventory display

afficher_plan(Matrix) # Display the plan thanks to the matrix recovered by the file
deplacer(POSITION_DEPART, POSITION_DEPART) # Moves the player to the starting position