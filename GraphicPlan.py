from CONFIGS import * # All constant variables
from turtle import * # Turtle Python Module
from enum import Enum
from FileDecoding import *
from Character import *

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

def calculer_pas(matrice):
    """
    Calculates the size to be given to the cells so that the plan fits in the area of the window
    matrice: 2D List | Plan matrix 
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
    """
    for i in range(len(matrice)): # Each row
        for j in range(len(matrice[i])): # Each column
            tracer_case((i,j), COULEURS[matrice[i][j]], Pas)
            
    #TurtleScreen update
    update()
    
def deplacer(matrice, position, mouvement):
    """
    Allows to move the counter to the desired square, redraws the counter
    matrice: 2D List | Plan matrix
    position: Tuple | Player's position
    mouvement: Tuple | Next player position
    Returns: Tuple | Player position (changed or unchanged)
    """
    if(isFree(mouvement)): # If the player can move
        characterDot.clear()
    
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
        return True
    
def ramasser_objet(cell):
    """
    Allows you to pick up an item, display it in the inventory
    cell: Tuple | Number of the cell
    """
    global TotalObjCollect # Total number of collected objects,
                             # allows the display of the object number,
                             # global to allow its modification
    
    inventaire.up()
    inventaire.goto(coordInventaire[0],coordInventaire[1] - 15 * TotalObjCollect) # We remove -15 to simulate a line break
    inventaire.down()
    inventaire.write("N°" + str(TotalObjCollect+1) + ": " + DictObjets[cell], font=("Verdana", 10, "normal"))
    
    annonce.clear()
    annonce.write("Vous avez trouvé: " + DictObjets[cell], font=("Verdana", 12, "bold")) # We display the announce

    TotalObjCollect += 1
    
    tracer_case(cell, COULEUR_CASES, Pas)
    Matrix[cell[0]][cell[1]] = 0 # We redefine the cell to 0 because now empty
    
def poser_question(case):
    """
    Ask a question to the player and return if the answer is correct or not
    case: Tuple | Number of the cell
    Returns: Boolean | Indicates whether the answer is correct or not
    """
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
    
def win_game():
    """
    Shows the player that he has won
    """
    annonce.clear()
    annonce.write("Vous avez gagné !! Bravo, c'est la fête :D", font=("Verdana", 12, "bold"))
    
class Case(Enum):
    """
    Enumeration of the cells, allows not to make mistakes when using these types.
    """
    EMPTY = 0
    WALL = 1
    VICTORY = 2
    DOOR = 3
    OBJECT = 4
    
Matrix = lire_matrice(fichier_plan) # 2D list that contains all the values of the game cells
Pas = calculer_pas(Matrix) # Float of the gap between each square (= 1 side of a square)
TotalObjCollect = 0 # Total number of collected objects
DictObjets = creer_dictionnaire(fichier_objets) # Object dictionary, format = cell:object (tuple:string)
DictQuestions = creer_dictionnaire(fichier_questions) # Questions dictionary, format = cell:answer (tuple:string)
coordInventaire = (POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - 15) # Real Turtle coordinate of the first line of the inventory display

afficher_plan(Matrix)
deplacer(Matrix, POSITION_DEPART, POSITION_DEPART)