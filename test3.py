from tkinter import *
from tkinter import Menu, filedialog, messagebox
import os
import json
import math

root = Tk()
root.title("Menu")
root.geometry("600x400")

sommet_list = []
arete_list = []
sommet_count = 0
selected_sommets = []

canvas = Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

def creation_sommet(event):
    global sommet_count
    x, y = event.x, event.y
    sommet_count += 1
    sommet_list.append((x, y))
    radius = 15
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
    canvas.create_text(x, y, text=str(sommet_count), font=("Arial", 12))

def creation_arete(event):
    global selected_sommets
    x, y = event.x, event.y
    sommet_proche = None
    distance_min = float('inf')

    for i, (sx, sy) in enumerate(sommet_list):
        distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
        if distance < distance_min and distance <= 20:
            distance_min = distance
            sommet_proche = (sx, sy, i + 1)

    if sommet_proche:
        selected_sommets.append(sommet_proche)

    if len(selected_sommets) == 2:
        x1, y1, num1 = selected_sommets[0]
        x2, y2, num2 = selected_sommets[1]
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
        arete_list.append(((x1, y1), (x2, y2)))
        selected_sommets = []

def activer_mode_sommet():
    canvas.bind("<Button-1>", creation_sommet)
    messagebox.showinfo("Mode Sommet", "Cliquez sur la zone blanche pour ajouter des sommets")

def activer_mode_arete():
    canvas.bind("<Button-1>", creation_arete)
    messagebox.showinfo("Mode Arête", "Cliquez sur deux sommets pour ajouter une arête")

def effacer_sommets():
    global sommet_list, sommet_count
    sommet_list = []
    sommet_count = 0
    canvas.delete("all")
    # Redessiner uniquement les arêtes, s'il en reste
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
    messagebox.showinfo("Effacer Sommets", "Tous les sommets ont été effacés.")

def effacer_aretes():
    global arete_list
    arete_list = []
    canvas.delete("all")
    # Redessiner uniquement les sommets, s'il en reste
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    messagebox.showinfo("Effacer Arêtes", "Toutes les arêtes ont été effacées.")

def nouveau_fichier():
    global sommet_list, arete_list, sommet_count, selected_sommets
    sommet_list = []
    arete_list = []
    sommet_count = 0
    selected_sommets = []
    canvas.delete("all")
    messagebox.showinfo("Nouveau", "Nouvelle interface vierge créée")

def ouvrir_fichier():
    fichier = filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=(("Fichiers JSON", "*.json"),))
    if fichier:
        try:
            with open(fichier, 'r') as f:
                data = json.load(f)
                charger_graphe(data)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")

def enregistrer_fichier():
    fichier = filedialog.asksaveasfilename(title="Enregistrer sous", defaultextension=".json", filetypes=(("Fichiers JSON", "*.json"),))
    if fichier:
        try:
            with open(fichier, 'w') as f:
                data = {"sommets": sommet_list, "aretes": arete_list}
                json.dump(data, f)
            messagebox.showinfo("Enregistrer", f"Fichier enregistré sous : {fichier}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")

def charger_graphe(data):
    global sommet_list, arete_list, sommet_count
    nouveau_fichier()
    sommet_list = data["sommets"]
    sommet_count = len(sommet_list)
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    arete_list = data["aretes"]
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

menu_bar = Menu(root)

menu_fichier = Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", command=nouveau_fichier)
menu_fichier.add_command(label="Ouvrir", command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer sous", command=enregistrer_fichier)
menu_fichier.add_command(label="Fermer", command=root.quit)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

menu_creation = Menu(menu_bar, tearoff=0)
menu_creation.add_command(label="Sommet", command=activer_mode_sommet)
menu_creation.add_command(label="Arête", command=activer_mode_arete)

# Sous-menu Effacer dans menu Création
menu_effacer = Menu(menu_creation, tearoff=0)
menu_effacer.add_command(label="Effacer Sommets", command=effacer_sommets)
menu_effacer.add_command(label="Effacer Arêtes", command=effacer_aretes)
menu_creation.add_cascade(label="Effacer", menu=menu_effacer)

menu_bar.add_cascade(label="Création", menu=menu_creation)

menu_affichage = Menu(menu_bar, tearoff=0)
menu_affichage.add_command(label="Graphe", command=lambda: messagebox.showinfo("Affichage", "Affichage du graphe"))
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)

menu_execution = Menu(menu_bar, tearoff=0)
menu_execution.add_command(label="Plus court chemin", command=lambda: messagebox.showinfo("Exécution", "Exécution du plus court chemin"))
menu_bar.add_cascade(label="Exécution", menu=menu_execution)

menu_edition = Menu(menu_bar, tearoff=0)
menu_edition.add_command(label="Graphe", command=lambda: messagebox.showinfo("Édition", "Édition du graphe"))
menu_bar.add_cascade(label="Édition", menu=menu_edition)

root.config(menu=menu_bar)
root.mainloop()