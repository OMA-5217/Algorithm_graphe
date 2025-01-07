# Ca se pour import tout le classe de bibiotheque de tkinter
from tkinter import *
from tkinter import filedialog,messagebox
import os
# En cree un nouveau fenetre
fenetre= Tk()
# En defini  la taille ou geometry de mon fenetre 
fenetre.geometry('400x300')
# En donne un Nom de  mon fenetre
fenetre.title('Menu')
# il premet de empeche ou autorise de se redimantion
fenetre.resizable(height=False,width=False)

 #un fonction permetant de ferme un fenetre
def ferme():
      # pour quitte le fenetre princiale
      # self.master se la nom de la fenetre principale 
      fenetre.quit()

    #un fonction permetant de cree un Nouveau fenetre 
def Nouveau():
       messagebox.showinfo("Nouveau","Ouvrire un Nouveau" )
       os.popen("python main.py")

     #un fonction permetant de ouvrire importe quelle fichier html ou python etc...
def Ouvrir():
        messagebox.showinfo("Ouvrire","Ouvrirev Fichier" )
          # je selection un fichier a la aide de filedialog 
        file=filedialog.askopenfilename( initialdir ="/",title="selection un fichier",
                                          # le type de fichier 
                                           filetype=(("text file","*.txt"),("all files","*.*")))
          # le fichier selection je le ouvrire en monde ecrire   
       
        
        
def Enregistrer():
        messagebox.showinfo("Enregistrer","Fichier Enregistrer ")
        fichier=filedialog.asksaveasfilename(title="Enregistrer",defaultextension="*.*",
                                             filetypes=(("text files","*.txt"),("All files","*.*")))
       



     #un fonction permetant de Enregistre sous un repertoire qui existe
def Enregistrer_sous():
    messagebox.showinfo("Enregistrer sous","Enregistrer sous" )
    fichier=filedialog.asksaveasfilename(defaultextension="*.*",
                                                  initialdir="/",
                                                  title="Enregistrer sous", 
                                                  filetypes=(("Text files","*.txt"),
                                                            ("All files ","*.*")))
                                                  
    


monmenu=Menu(fenetre)
menuFichier=Menu(monmenu, tearoff=False)
monmenu.add_cascade(label="Fichier",menu=menuFichier)
menuFichier.add_command(label="Nouveau",command=Nouveau)
menuFichier.add_command(label="Ouvrir",command=Ouvrir)
menuFichier.add_command(label="Enregistre")
menuFichier.add_command(label="Enregistre sous",command=Enregistrer_sous)
menuFichier.add_command(label="fermer",command=ferme)
#la cree un  menu  de creation avec son sous menu
menuCreation=Menu(monmenu, tearoff=False)
monmenu.add_cascade(label="Creation", menu=menuCreation)
menuCreation.add_command(label="Sommet")
menuCreation.add_command(label="Arete")
         
menuAffichage=Menu(monmenu,tearoff=False)
monmenu.add_cascade(label="Affichage", menu=menuAffichage)
menuAffichage.add_command(label="graphe")
menuAffichage.add_command(label="chaines")
menuAffichage.add_command(label="matrices")
           
          # la creation de menu de excution avec son sous menu
menuExecution=Menu(monmenu,tearoff=False)

monmenu.add_cascade(label="Execution", menu=menuExecution)
menuExecution.add_command(label="plus court chemin")
menuExecution.add_command(label="coloration")
          
          # la creation de menu de Etdition avec son sous menu 
menuEdition=Menu(monmenu,tearoff=False)
monmenu.add_cascade(label="Edition", menu=menuEdition)
menuEdition.add_command(label="grahe")

fenetre.config(menu=monmenu)
fenetre.mainloop()