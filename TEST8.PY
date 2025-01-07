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
 
# Création du canvas dans la fenêtre principale avec un fond blanc
canvas = Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

def creation_sommet(event):
    global sommet_count
    x, y = event.x, event.y
    rayon_min = 40  # Distance minimale entre deux sommets

    # Vérification de la proximité des autres sommets
    for (sx, sy) in sommet_list:
        distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
        if distance < rayon_min:
            messagebox.showwarning("Erreur", "Un sommet est déjà trop proche.")
            return  # Ne crée pas de sommet si un autre est trop proche

    # Si aucune proximité détectée, créer le sommet
    sommet_count += 1
    sommet_list.append((x, y))
    radius = 15
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
    canvas.create_text(x, y, text=str(sommet_count), font=("Arial", 12))

def creation_arete(event):
    global selected_sommets
    x, y = event.x, event.y
    sommet_proche = None
    distance_min = float('inf')

    # Parcourt les sommets pour trouver celui le plus proche à 20 pixels ou moins
    for i, (sx, sy) in enumerate(sommet_list):
        distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
        if distance < distance_min and distance <= 20:
            distance_min = distance
            sommet_proche = (sx, sy, i + 1)

    # Ajoute le sommet trouvé à selected_sommets
    if sommet_proche:
        selected_sommets.append(sommet_proche)

    # Quand deux sommets sont sélectionnés, les coordonnées de chacun sont stockées
    if len(selected_sommets) == 2:
        x1, y1, num1 = selected_sommets[0]
        x2, y2, num2 = selected_sommets[1]

        # Vérification si l'arête existe déjà
        if ((x1, y1), (x2, y2)) in arete_list or ((x2, y2), (x1, y1)) in arete_list:
            messagebox.showwarning("Erreur", "Une arête existe déjà entre ces sommets.")
            selected_sommets = []
            return  # Ne crée pas d'arête si elle existe déjà

        # Création de l'arête si elle n'existe pas encore dans la liste d'arêtes
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
        arete_list.append(((x1, y1), (x2, y2)))
        selected_sommets = []

# Fonction pour afficher le graphe
def afficher_graphe():
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
    messagebox.showinfo("Affichage", "Affichage du graphe terminé")

# Fonction pour vérifier la présence d'une chaîne entre deux sommets
def est_chaine(sommet_depart, sommet_arrivee):
    visite = {i: False for i in range(1, sommet_count + 1)}

    def dfs(sommet):
        if sommet == sommet_arrivee:
            return True
        visite[sommet] = True
        for (x1, y1), (x2, y2) in arete_list:
            voisin = sommet_list.index((x2, y2)) + 1 if sommet_list.index((x1, y1)) + 1 == sommet else sommet_list.index((x1, y1)) + 1
            if not visite[voisin]:
                if dfs(voisin):
                    return True
        return False

    return dfs(sommet_depart)

# Widgets pour l'affichage des matrices
matrice_frame = Frame(canvas)
matrice_frame.pack(side=BOTTOM, fill="x")

def afficher_matrice(matrice, titre):
    for widget in matrice_frame.winfo_children():
        widget.destroy()
    
    Label(matrice_frame, text=titre, font=("Arial", 14, "bold")).pack(anchor=W)
    for row in matrice:
        row_text = ' '.join(map(str, row))
        Label(matrice_frame, text=row_text, font=("Arial", 12)).pack(anchor=W)

def matrice_adjacence():
    matrice = [[0] * sommet_count for _ in range(sommet_count)]
    for (x1, y1), (x2, y2) in arete_list:
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][j] = matrice[j][i] = 1
    afficher_matrice(matrice, "Matrice d'Adjacence")

def matrice_incidence():
    matrice = [[0] * len(arete_list) for _ in range(sommet_count)]
    for index, ((x1, y1), (x2, y2)) in enumerate(arete_list):
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][index] = matrice[j][index] = 1
    afficher_matrice(matrice, "Matrice d'Incidence")

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
    # si un sommet est trouve il est supprime avec les aretes asscocies
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
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
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
    # verifie si le utilisateura a selection un emplacement 
    if fichier:
        try:
            with open(fichier, 'w') as f:

                # cree un  dictionnteur qui contients les list de sommet est list de arets
                data = {"sommets": sommet_list, "aretes": arete_list}
                json.dump(data, f)
            messagebox.showinfo("Enregistrer", f"Fichier enregistré sous : {fichier}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")
   
def charger_graphe(data):
    global sommet_list, arete_list, sommet_count
    nouveau_fichier()
    sommet_list = data["sommets"]
    #met a joure le compteur des sommet en fonction de liste de chargee
    sommet_count = len(sommet_list)
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    #extrait la list des arete depuis le fichier json
    arete_list = data["aretes"]
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

# Configuration du menu
menu_bar = Menu(root)

menu_fichier = Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", command=nouveau_fichier)
menu_fichier.add_command(label="Ouvrir", command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer", command=enregistrer_fichier)
menu_fichier.add_command(label="Fermer", command=root.quit)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

menu_creation = Menu(menu_bar, tearoff=0)
menu_creation.add_command(label="Sommet", command=activer_mode_sommet)
menu_creation.add_command(label="Arête", command=activer_mode_arete)

menu_effacer = Menu(menu_creation, tearoff=0)
menu_effacer.add_command(label="Effacer un sommet", command=activer_mode_effacer_sommet)
menu_effacer.add_command(label="Effacer une arête", command=activer_mode_effacer_arete)
menu_creation.add_cascade(label="Effacer", menu=menu_effacer)

menu_bar.add_cascade(label="Création", menu=menu_creation)

menu_affichage = Menu(menu_bar, tearoff=0)
menu_affichage.add_command(label="Afficher Graphe", command=afficher_graphe)
menu_matrices=Menu(menu_affichage,tearoff=0)
menu_matrices.add_command(label="Matrices Adjacence", command=matrice_adjacence)
menu_matrices.add_command(label="Matrices Incidence", command=matrice_incidence)
menu_affichage.add_cascade(label="Matrices",menu=menu_matrices)
menu_affichage.add_command(label="chaine",command=est_chaine)
menu_affichage.add_command(label="chemin")
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)

root.config(menu=menu_bar)
root.mainloop()