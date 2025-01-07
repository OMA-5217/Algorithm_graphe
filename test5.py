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

# Mode d'effacement pour supprimer un sommet
def activer_mode_effacer_sommet():
    canvas.bind("<Button-1>", effacer_sommet)
    messagebox.showinfo("Mode Effacer Sommet", "Cliquez sur un sommet pour l'effacer")

# Mode d'effacement pour supprimer une arête
def activer_mode_effacer_arete():
    canvas.bind("<Button-1>", effacer_arete)
    messagebox.showinfo("Mode Effacer Arête", "Cliquez sur une arête pour l'effacer")

# Fonction pour effacer un sommet cliqué
def effacer_sommet(event):
    global sommet_list, arete_list
    x, y = event.x, event.y
    rayon = 15

    for i, (sx, sy) in enumerate(sommet_list):
        if (sx - rayon <= x <= sx + rayon) and (sy - rayon <= y <= sy + rayon):
            arete_list = [ar for ar in arete_list if (ar[0] != (sx, sy) and ar[1] != (sx, sy))]
            sommet_list.pop(i)
            redraw_canvas()
            return

# Fonction pour effacer une arête cliquée
def effacer_arete(event):
    global arete_list
    x, y = event.x, event.y

    for i, ((x1, y1), (x2, y2)) in enumerate(arete_list):
        distance = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / math.hypot(x2 - x1, y2 - y1)
        if distance < 5:
            arete_list.pop(i)
            redraw_canvas()
            return

def redraw_canvas():
    canvas.delete("all")
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

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

menu_enregistrer = Menu(menu_fichier, tearoff=0)
menu_enregistrer.add_command(label="Enregistrer", command=enregistrer_fichier)
menu_enregistrer.add_command(label="Enregistrer sous", command=enregistrer_fichier)
menu_fichier.add_cascade(label="Enregistrer", menu=menu_enregistrer)

menu_fichier.add_command(label="Fermer", command=root.quit)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

menu_creation = Menu(menu_bar, tearoff=0)
menu_creation.add_command(label="Sommet", command=activer_mode_sommet)
menu_creation.add_command(label="Arête", command=activer_mode_arete)

# Sous-menu Effacer dans le menu Création
menu_effacer = Menu(menu_creation, tearoff=0)
menu_effacer.add_command(label="Effacer un sommet", command=activer_mode_effacer_sommet)
menu_effacer.add_command(label="Effacer une arête", command=activer_mode_effacer_arete)
menu_creation.add_cascade(label="Effacer", menu=menu_effacer)

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


root.config(menu=menu_bar)
root.mainloop()