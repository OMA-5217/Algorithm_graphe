# Ca se pour import tout le classe de bibiotheque de tkinter
from tkinter import *
#   
import os
#
from ProjetPython import *

# En cree un nouveau fenetre
fenetre= Tk()
# En defini la taille de mon fenetre 
fenetre.geometry('400x300')
# En donne un Nom a mon fenetre
fenetre.title('Menu')
# il premet de empeche ou autorise de se redimantion
fenetre.resizable(height=False,width=False)

#--------------------------fuction-----------
def ferme():
    # pour quitte le fenetre princiale
    # self.master se la nom de la fenetre principale 
    fenetre.quit()

#un fonction permetant de cree un Nouveau fenetre 
def Nouveau():
    os.popen("python main.py")

#--------------------------------------------



# --1)creation  le barres de menu 
mon_menu=Menu(fenetre)



#creation des menu principaux  tearoff permet eface le ture -----
menuFichier=Menu(mon_menu, tearoff=False)
menuCreation=Menu(mon_menu, tearoff=False)
menuAffichage=Menu(mon_menu,tearoff=False)
menuExecution=Menu(mon_menu,tearoff=False)
menuEdition=Menu(mon_menu,tearoff=False)


# Ajoute des menu principaux a la barres des menu

mon_menu.add_cascade(label="Fichier", menu=menuFichier)
mon_menu.add_cascade(label="Creation", menu=menuCreation)
mon_menu.add_cascade(label="Affichage", menu=menuAffichage)
mon_menu.add_cascade(label="Execution", menu=menuExecution)
mon_menu.add_cascade(label="Edition", menu=menuEdition)


##--3) Ajouti  de commande au menu  principal  fichier 

menuFichier.add_command(label="Nouveau",command=Nouveau)
menuFichier.add_command(label="Ouvrir")
menuFichier.add_command(label="Enregistre")
menuFichier.add_command(label="Enregistre sous")
menuFichier.add_command(label="fermer",command=ferme)

# 4) Ajoute de commande au menu principal Creation

menuCreation.add_command(label="Sommet")
menuCreation.add_command(label="Arete")


# 5) Ajoute de commande au menu principal Affîchage
menuAffichage.add_command(label="graphe")
menuAffichage.add_command(label="chaines")
menuAffichage.add_command(label="matrices")


# -6) Ajoute de commande au menu principal Execution 

menuExecution.add_command(label="plus court chemin")
menuExecution.add_command(label="coloration")

# -7) Ajoute de commande au menu principal Edition 
menuEdition.add_command(label="grahe")




fenetre.config(menu=mon_menu,bg='silver')
#Affche mon fenetre 
fenetre.mainloop()



