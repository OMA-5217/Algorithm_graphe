#
from tkinter import *
import os
from tkinter import filedialog,messagebox
#import math




class textEditor:
    def __init__(self,master,content):
        self.master=master
        self.content=content

#creation de la fenerte principale
    def creation(self):
       self.master=Tk()
       self.master.title("Menu")
       self.master.geometry("400x300")
       self.master.resizable(height=False,width=False)
   
    def add_text(self):
       self.content=Text(self.master)
       self.content.pack(expand= True ,fill= 'both')


    def generate(self):
       self.master.mainloop()    



    #----------------------------
    # creation de fonction
     #------------------------- 
    #un fonction permetant de ferme un fenetre
    def ferme(self):
      # pour quitte le fenetre princiale
      # self.master se la nom de la fenetre principale 
      self.master.quit()

    #un fonction permetant de cree un Nouveau fenetre 
    def Nouveau(self):
       messagebox.showinfo("Nouveau","Ouvrire un Nouveau" )
       os.popen("python main.py")

     #un fonction permetant de ouvrire importe quelle fichier html ou python etc...
    def Ouvrir(self):
          messagebox.showinfo("Ouvrire","Ouvrirev Fichier" )
          # je selection un fichier a la aide de filedialog 
          file=filedialog.askopenfilename( initialdir ="/",title="selection un fichier",
                                          # le type de fichier 
                                           filetype=(("text file","*.txt"),("all files","*.*")))
          # le fichier selection je le ouvrire en monde ecrire   
          f=open(file,'r')
          r=f.read()
          # la fermeture de fichier
          f.close()
          self.content.insert("1.0",r)
          
        
    def Enregistrer(self):
        messagebox.showinfo("Enregistrer","Fichier Enregistrer ")
        fichier=filedialog.asksaveasfilename(title="Enregistrer",defaultextension="*.*",
                                             filetypes=(("text files","*.txt"),("All files","*.*")))
        f=open(fichier,"w")
        s=self.content.get("1,0",END)
        w=f.write(s)
        f.close()



     #un fonction permetant de Enregistre sous un repertoire qui existe
    def Enregistrer_sous(self):
             messagebox.showinfo("Enregistrer sous","Enregistrer sous" )
             fichier=filedialog.asksaveasfilename(defaultextension="*.*",
                                                  initialdir="/",
                                                  title="Enregistrer sous", 
                                                  filetypes=(("Text files","*.txt"),
                                                            ("All files ","*.*")))
                                                  
             f=open(fichier,'W')
             
             s=self.content.get("1.0",END)
             f.write(s)
             f.close()

     #---------------------------------------Sommets est Aretes-----------------
    #def creation_sommets(self):
       
      #----------------------
      # creation de menu
      #--------------------
    def creation_Menu(self):
         monmenu=Menu(self.master)
         menuFichier=Menu(monmenu, tearoff=False)
         monmenu.add_cascade(label="Fichier",menu=menuFichier)
         menuFichier.add_command(label="Nouveau",command=self.Nouveau)
         menuFichier.add_command(label="Ouvrir",command=self.Ouvrir)
         menuFichier.add_command(label="Enregistre")
         menuFichier.add_command(label="Enregistre sous",command=self.Enregistrer_sous)
         menuFichier.add_command(label="fermer",command=self.ferme)
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
         
         #je associ monmenu a la fenetre principale
         self.master.config(menu=monmenu)
   


