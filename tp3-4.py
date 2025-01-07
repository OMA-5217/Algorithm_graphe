from tkinter import *
from tkinter import Menu, filedialog, messagebox
import os  # Importation du module os pour ouvrir les fichiers avec l'application par défaut
import json  # Importation pour enregistrers
import math

# Créer la fenêtre principale
root = Tk()
root.title("Menu")
root.geometry("600x400")

# Variables pour gérer les sommets et arêtes
 # Liste des sommets (chaque sommet est un tuple (x, y))
sommet_list = [] 
# Liste des arêtes (chaque arête est un tuple ((x1, y1), (x2, y2)))
arete_list = [] 
# Compteur pour numérotation des sommets  
sommet_count = 0 
# Liste pour sélectionner deux sommets pour une arête
selected_sommets = []  
canvas_actif=None
vertices=[]
edges=[]
selected_vertex=None
# Créer un canevas pour dessiner les sommets et arêtes
canvas = Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# Fonction pour dessiner un sommet là où on clique sur le canevas
def creation_sommet(event):
    global sommet_count
    x, y = event.x, event.y  # Coordonnées du clic
    sommet_count += 1  # Incrémenter le numéro du sommet
    sommet_list.append((x, y))  # Ajouter le sommet à la liste
    radius = 15  # Rayon du cercle (sommet)
    
    # Dessiner le sommet (un cercle)
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
    
    # Ajouter un numéro au centre du sommet
    canvas.create_text(x, y, text=str(sommet_count), font=("Arial", 12))

# Fonction pour créer une arête entre deux sommets
def creation_arete(event):
    global selected_sommets
    x, y = event.x, event.y
    # Rechercher le sommet le plus proche du clic
    sommet_proche = None
    distance_min = float('inf')
    
    for i, (sx, sy) in enumerate(sommet_list):
        distance = math.sqrt((sx - x) **2 + (sy - y) ** 2)
        if distance < distance_min and distance <= 20:  # Seuil pour sélectionner un sommet
            distance_min = distance
            sommet_proche = (sx, sy, i + 1)  # (coordonnées, numéro du sommet)
    
    if sommet_proche:
        selected_sommets.append(sommet_proche)
    
    # Si deux sommets sont sélectionnés, tracer une arête
    if len(selected_sommets) == 2:
        x1, y1, num1 = selected_sommets[0]
        x2, y2, num2 = selected_sommets[1]
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)  # Tracer une arête (ligne)
        arete_list.append(((x1, y1), (x2, y2)))  # Ajouter l'arête à la liste
        selected_sommets = []  # Réinitialiser la sélection

# Mode d'ajout de sommets
def activer_mode_sommet():
    # Lier l'événement clic gauche à la fonction de création de sommet
    canvas.bind("<Button-1>", creation_sommet)
    messagebox.showinfo("Mode Sommet", "Cliquez sur la zone blanche pour ajouter des sommets")

# Mode d'ajout d'arêtes
def activer_mode_arete():
    # Lier l'événement clic gauche à la fonction de création d'arête
    canvas.bind("<Button-1>", creation_arete)
    messagebox.showinfo("Mode Arête", "Cliquez sur deux sommets pour ajouter une arête")

# Fonction pour "Nouveau"
def nouveau_fichier():
    global sommet_list, arete_list, sommet_count, selected_sommets
    # Réinitialiser les variables des sommets et arêtes
    sommet_list = []
    arete_list = []
    sommet_count = 0
    selected_sommets = []
    
    # Effacer tout le contenu du canevas (sommets, arêtes, etc.)
    canvas.delete("all")
    
    messagebox.showinfo("Nouveau", "Nouvelle interface vierge créée")

# Fonction pour "Ouvrir" un graphe depuis un fichier
def ouvrir_fichier():
    fichier = filedialog.askopenfilename(
        title="Ouvrir un fichier",
        filetypes=(("Fichiers JSON", "*.json"),)
    )
    
    if fichier:
        try:
            with open(fichier, 'r') as f:
                data = json.load(f)
                charger_graphe(data)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")



def enregistrer_fichier():
    fichier = filedialog.asksaveasfilename(
        title="Enregistrer sous",
        defaultextension=".json",
        filetypes=(("Fichiers JSON", "*.json"),)
    )
    if fichier:
        try:
            with open(fichier, 'w') as f:
                data = {"sommets": sommet_list, "aretes": arete_list}
                json.dump(data, f)
            messagebox.showinfo("Enregistrer", f"Fichier enregistré sous : {fichier}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")

# Fonction pour charger un graphe à partir de données JSON
def charger_graphe(data):
    global sommet_list, arete_list, sommet_count
    nouveau_fichier()  # Réinitialiser l'interface avant de charger le nouveau graphe
    
    # Charger les sommets
    sommet_list = data["sommets"]
    sommet_count = len(sommet_list)  # Mettre à jour le compteur de sommets
    
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    
    # Charger les arêtes
    arete_list = data["aretes"]
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

# ---- Menu Fichier ----
menu_bar = Menu(root)

menu_fichier = Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", command=nouveau_fichier)
menu_fichier.add_command(label="Ouvrir", command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer",command=enregistrer)
menu_fichier.add_command(label="Enregistrer sous", command=enregistrer_fichier)
#menu_fichier.add_command(label="Enregistrer sous", command=enregistrer_sous_fichier)
menu_fichier.add_command(label="Fermer", command=root.quit)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

# ---- Menu Création ----
menu_creation = Menu(menu_bar, tearoff=0)
menu_creation.add_command(label="Sommet", command=activer_mode_sommet)
menu_creation.add_command(label="Arête", command=activer_mode_arete)
menu_bar.add_cascade(label="Création", menu=menu_creation)

# ---- Menu Affichage ----
menu_affichage = Menu(menu_bar, tearoff=0)
menu_affichage.add_command(label="Graphe", command=lambda: messagebox.showinfo("Affichage", "Affichage du graphe"))
menu_affichage.add_command(label="Chaînes", command=lambda: messagebox.showinfo("Affichage", "Affichage des chaînes"))
menu_affichage.add_command(label="Matrices", command=lambda: messagebox.showinfo("Affichage", "Affichage des matrices"))
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)

# ---- Menu Exécution ----
menu_execution = Menu(menu_bar, tearoff=0)
menu_execution.add_command(label="Plus court chemin", command=lambda: messagebox.showinfo("Exécution", "Exécution du plus court chemin"))
menu_execution.add_command(label="Coloration", command=lambda: messagebox.showinfo("Exécution", "Exécution de la coloration"))
menu_bar.add_cascade(label="Exécution", menu=menu_execution)

# ---- Menu Édition ----
menu_edition = Menu(menu_bar, tearoff=0)
menu_edition.add_command(label="Graphe", command=lambda: messagebox.showinfo("Édition", "Édition du graphe"))
menu_bar.add_cascade(label="Édition", menu=menu_edition)

# Afficher la barre de menus dans la fenêtre principale
root.config(menu=menu_bar)

# Lancer la boucle principale de l'interface
root.mainloop()