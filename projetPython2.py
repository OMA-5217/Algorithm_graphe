# Ca se pour import tout le classe de bibiotheque de tkinter
from tkinter import *
# En cree un nouveau fenetre
fenetre= Tk()
# En defini  la taille ou geometry de mon fenetre 
fenetre.geometry('400x300')
# En donne un Nom de  mon fenetre
fenetre.title('Menu')
# il premet de empeche ou autorise de se redimantion
fenetre.resizable(height=False,width=False)

#creation de bouton fichier
bouton= Button(fenetre,text="fichier",bg='silver')
#affiche mon bouton

bouton.grid(row=0 ,column=0)

#creation de bouton creation 
bouton= Button(fenetre,text="Creation",bg='silver')
#affiche mon bouton
#bouton.pack()
bouton.grid(row=0 ,column=1)

#creation de bouton de Affichage 
bouton= Button(fenetre,text="Affichage",bg='silver')
#affiche mon bouton
#bouton.pack()
bouton.grid(row=0 ,column=2)

#creation de bouton de Execution
bouton= Button(fenetre,text="Execution",bg='silver')
#affiche mon bouton
#bouton.pack()
bouton.grid(row=0 ,column=3)

#creation de bouton de Edition 
bouton= Button(fenetre,text="Edition",bg='silver')
#affiche mon bouton row est column permet de donne la ligne est le colone
#bouton.pack()
bouton.grid(row=0 ,column=4)



# il permet de affiche 
fenetre.mainloop()
