from CONFIGS import * # All constant variables

def tryParseToInt(number):
    """
    Allows to parse a variable in int
    number: Int | Number to try to parse
    Returns: Int | The int, or 0 if the parse don't work
    """
    try:
        return int(number)
    except:
        print("Error! Impossible to parse this variable")
        return 0

def lire_matrice(fichier):
    """
    Allows to interpret the file in a matrix
    fichier: String | File name to read
    Returns: 2D List | Matrix
    """
    matrix = [] # Matrix (2D list) of the game plan
    
    with open(fichier) as file:
        data = file.readlines() # Contains all rows as a list (1 row = 1 item)
    
    for i in data: # i will have the line
        IntList = [] # Matrix which will contain in item integer
        for j in i.split(): # j will have each digit of the line i
            IntList.append(tryParseToInt(j))
        
        matrix.append(IntList)
        
    return matrix

def creer_dictionnaire(fichier_des_objets):
    """
    Reads and interprets the object file
    fichier_des_objets: String | File name
    Returns: Dictionary | Item dictionary for Object or Questions, format = cell:item (tuple:string)
    """
    dictObj = {} # Item dictionary, format = cell:item (tuple:string)
    
    with open(fichier_des_objets, mode="r", encoding="utf-8") as file:
        data = file.readlines() # Contains all rows as a list (1 row = 1 item)
        
        for i in data:
            cell, item = eval(i) # Defines according to the type of cast a value to the variable
            dictObj[cell] = item
            
    return dictObj