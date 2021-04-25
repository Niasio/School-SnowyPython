from Character import *

while True:
    listen()
    onkeypress(deplacer_gauche, "Left")
    onkeypress(deplacer_droite, "Right")
    onkeypress(deplacer_haut, "Up")
    onkeypress(deplacer_bas, "Down")
    mainloop()