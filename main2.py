from tkinter import *
import os

from   test2  import *


app = textEditor("fen","contenu")

app.creation()
app.add_text()
app.creation_Menu()
app.creer_canvas()
app.generate()


f=open(fichier,'W')
             
    
    f.write()
    f.close()