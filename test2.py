from tkinter import *
import os
from tkinter import filedialog, messagebox
import math


class textEditor:
    def __init__(self, master,content):
        self.master = master
        self.content = content
        self.sommet_list = []  # Liste des sommets
        self.arete_list = []  # Liste des arêtes
        self.sommet_count = 0  # Compteur pour numérotation des sommets
        self.selected_sommets = []  # Liste pour sélectionner deux sommets pour une arête
        self.canvas = None

    def creation(self):
        self.master=Tk()
        self.master.title("Menu")
        self.master.geometry("400x300")
        self.master.resizable(height=False, width=False)

    def add_text(self):
        self.content = Text(self.master)
        self.content.pack(expand=True, fill='both')

    def generate(self):
        self.master.mainloop()

    def ferme(self):
        self.master.quit()

    def Nouveau(self):
        messagebox.showinfo("Nouveau", "Ouvrir un Nouveau")
        os.popen("python main.py")

    def Ouvrir(self):
        messagebox.showinfo("Ouvrir", "Ouvrir un fichier")
        file = filedialog.askopenfilename(initialdir="/", title="Sélectionner un fichier",
                                          filetypes=(("text file", ".txt"), ("all files", ".*")))
        with open(file, 'r') as f:
            r = f.read()
        self.content.insert("1.0", r)

    def Enregistrer(self):
        messagebox.showinfo("Enregistrer", "Fichier enregistré")
        fichier = filedialog.asksaveasfilename(title="Enregistrer", defaultextension=".",
                                               filetypes=(("text files", ".txt"), ("All files", ".*")))
        with open(fichier, "w") as f:
            s = self.content.get("1.0", END)
            f.write(s)

    def Enregistrer_sous(self):
        messagebox.showinfo("Enregistrer sous", "Enregistrer sous")
        fichier = filedialog.asksaveasfilename(defaultextension=".", initialdir="/",
                                               title="Enregistrer sous", filetypes=(("Text files", ".txt"), ("All files", ".*")))
        with open(fichier, 'w') as f:
            s = self.content.get("1.0", END)
            f.write(s)

    #---------------------------Sommets est aretes-------------------
    def creer_canvas(self):
        self.canvas = Canvas(self.master, bg="white")
        self.canvas.pack(fill="both", expand=True)

      
      # Fonction pour dessiner un sommet
    def creation_sommet(self, event):
        x, y = event.x, event.y
        self.sommet_count += 1
        self.sommet_list.append((x, y))
        radius = 15
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
        self.canvas.create_text(x, y, text=str(self.sommet_count), font=("Arial", 12))

    # Fonction pour créer une arête
    def creation_arete(self, event):
        x, y = event.x, event.y
        sommet_proche = None
        distance_min = float('inf')
        
        for i, (sx, sy) in enumerate(self.sommet_list):
            distance = math.sqrt((sx - x) * 2 + (sy - y) * 2)
            if distance < distance_min and distance <= 20:
                distance_min = distance
                sommet_proche = (sx, sy, i + 1)
        
        if sommet_proche:
            self.selected_sommets.append(sommet_proche)
        
        if len(self.selected_sommets) == 2:
            x1, y1, num1 = self.selected_sommets[0]
            x2, y2, num2 = self.selected_sommets[1]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            self.arete_list.append(((x1, y1), (x2, y2)))
            self.selected_sommets = []

    def activer_creation_sommets(self):
        self.canvas.bind("<Button-1>", self.creation_sommet)

    def activer_creation_aretes(self):
        self.canvas.bind("<Button-1>", self.creation_arete)        

    def creation_Menu(self):
        monmenu = Menu(self.master)
        menuFichier = Menu(monmenu, tearoff=False)
        monmenu.add_cascade(label="Fichier", menu=menuFichier)
        menuFichier.add_command(label="Nouveau", command=self.Nouveau)
        menuFichier.add_command(label="Ouvrir", command=self.Ouvrir)
        menuFichier.add_command(label="Enregistrer", command=self.Enregistrer)
        menuFichier.add_command(label="Enregistrer sous", command=self.Enregistrer_sous)
        menuFichier.add_command(label="Fermer", command=self.ferme)

        # Menu de création pour les sommets et arêtes
        menuCreation = Menu(monmenu, tearoff=False)
        monmenu.add_cascade(label="Création", menu=menuCreation)
        menuCreation.add_command(label="Sommet", command=self.activer_creation_sommets)
        menuCreation.add_command(label="Arête", command=self.activer_creation_aretes)
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
        
        self.master.config(menu=monmenu)    