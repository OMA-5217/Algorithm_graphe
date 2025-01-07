from tkinter import *
from tkinter import Menu, filedialog, messagebox
import json
import math
from collections import defaultdict, deque

# Fenêtre principale
root = Tk()
root.title("Graphe")
root.geometry("800x600")

sommet_list = []
arete_list = []
sommet_count = 0
selected_sommets = []
fichier_actuel = None
modifications_apportees = False

# Canvas
canvas = Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# Notification de modification
def notifier_modification():
    global modifications_apportees
    modifications_apportees = True

# Réinitialisation des modifications
def reset_modifications():
    global modifications_apportees
    modifications_apportees = False

# Vérifier si le fichier doit être enregistré avant de continuer
def verifier_sauvegarde():
    if modifications_apportees:
        reponse = messagebox.askyesnocancel(
            "Enregistrer", "Des modifications ont été apportées. Voulez-vous les enregistrer ?")
        if reponse:  # Oui
            enregistrer_fichier()
        elif reponse is None:  # Annuler
            return False
    return True

# Fonction pour calculer et afficher la matrice d'adjacence
def afficher_matrice_adjacence():
    if not sommet_list:
        messagebox.showwarning("Erreur", "Aucun graphe chargé.")
        return

    taille = len(sommet_list)
    matrice = [[0] * taille for _ in range(taille)]

    for (x1, y1), (x2, y2) in arete_list:
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][j] = 1
        matrice[j][i] = 1  # Pour les graphes non orientés

    # Afficher la matrice dans une nouvelle fenêtre
    fenetre_matrice = Toplevel(root)
    fenetre_matrice.title("Matrice d'Adjacence")
    for i in range(taille):
        for j in range(taille):
            Label(fenetre_matrice, text=str(matrice[i][j]), width=3, borderwidth=1, relief="solid").grid(row=i, column=j)

# Fonction pour calculer et afficher la matrice d'incidence
def afficher_matrice_incidence():
    if not sommet_list or not arete_list:
        messagebox.showwarning("Erreur", "Aucun graphe chargé.")
        return

    sommets = len(sommet_list)
    aretes = len(arete_list)
    matrice = [[0] * aretes for _ in range(sommets)]

    for k, ((x1, y1), (x2, y2)) in enumerate(arete_list):
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][k] = 1
        matrice[j][k] = 1  # Pour les graphes non orientés

    # Afficher la matrice dans une nouvelle fenêtre
    fenetre_matrice = Toplevel(root)
    fenetre_matrice.title("Matrice d'Incidence")
    for i in range(sommets):
        for j in range(aretes):
            Label(fenetre_matrice, text=str(matrice[i][j]), width=3, borderwidth=1, relief="solid").grid(row=i, column=j)

# Fonction pour déterminer l'existence d'une chaîne eulérienne
def verifier_chaine_eulerienne():
    if not sommet_list or not arete_list:
        messagebox.showwarning("Erreur", "Aucun graphe chargé.")
        return

    degres = [0] * len(sommet_list)
    for (x1, y1), (x2, y2) in arete_list:
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        degres[i] += 1
        degres[j] += 1

    odd_count = sum(1 for d in degres if d % 2 != 0)

    if odd_count == 0:
        messagebox.showinfo("Chaîne eulérienne", "Le graphe contient un circuit eulérien.")
    elif odd_count == 2:
        messagebox.showinfo("Chaîne eulérienne", "Le graphe contient une chaîne eulérienne.")
    else:
        messagebox.showwarning("Chaîne eulérienne", "Aucune chaîne eulérienne n'existe.")

# Fonction pour trouver un chemin entre deux sommets
def trouver_chemin():
    if not sommet_list or not arete_list:
        messagebox.showwarning("Erreur", "Aucun graphe chargé.")
        return

    def demander_sommets():
        try:
            sommet1 = int(entry_s1.get()) - 1
            sommet2 = int(entry_s2.get()) - 1

            if sommet1 < 0 or sommet2 < 0 or sommet1 >= len(sommet_list) or sommet2 >= len(sommet_list):
                raise ValueError

            # Appeler l'algorithme pour trouver le chemin
            chemin = bfs(sommet1, sommet2)
            if chemin:
                colorier_chemin(chemin)
            else:
                messagebox.showwarning("Erreur", "Aucun chemin trouvé.")
        except ValueError:
            messagebox.showerror("Erreur", "Saisissez des numéros de sommets valides.")

    def bfs(start, end):
        queue = deque([start])
        visited = set()
        parents = {start: None}

        while queue:
            current = queue.popleft()
            if current == end:
                path = []
                while current is not None:
                    path.append(current)
                    current = parents[current]
                return path[::-1]

            visited.add(current)
            for (x1, y1), (x2, y2) in arete_list:
                i, j = sommet_list.index((x1, y1)), sommet_list.index((x2, y2))
                if current in (i, j):
                    neighbor = j if current == i else i
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                        parents[neighbor] = current
        return None

    def colorier_chemin(chemin):
        for i in range(len(chemin) - 1):
            x1, y1 = sommet_list[chemin[i]]
            x2, y2 = sommet_list[chemin[i + 1]]
            canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

    # Fenêtre pour demander les sommets
    fenetre_chemin = Toplevel(root)
    fenetre_chemin.title("Chemin entre deux sommets")
    Label(fenetre_chemin, text="Sommet 1 :").grid(row=0, column=0)
    entry_s1 = Entry(fenetre_chemin)
    entry_s1.grid(row=0, column=1)
    Label(fenetre_chemin, text="Sommet 2 :").grid(row=1, column=0)
    entry_s2 = Entry(fenetre_chemin)
    entry_s2.grid(row=1, column=1)
    Button(fenetre_chemin, text="Trouver", command=demander_sommets).grid(row=2, columnspan=2)


def nouveau_fichier():
    global sommet_list, arete_list, sommet_count, selected_sommets, fichier_actuel
    if not verifier_sauvegarde():
        return
    sommet_list = []
    arete_list = []
    sommet_count = 0
    selected_sommets = []
    fichier_actuel = None
    canvas.delete("all")
    reset_modifications()
    messagebox.showinfo("Nouveau", "Nouvelle interface vierge créée")

def ouvrir_fichier():
    global fichier_actuel
    if not verifier_sauvegarde():
        return
    fichier = filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=(("Fichiers JSON", "*.json"),))
    if fichier:
        try:
            with open(fichier, 'r') as f:
                data = json.load(f)
                charger_graphe(data)
                fichier_actuel = fichier
                reset_modifications()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")

def enregistrer_fichier():
    global fichier_actuel
    if not fichier_actuel:
        fichier_actuel = filedialog.asksaveasfilename(title="Enregistrer sous", defaultextension=".json", filetypes=(("Fichiers JSON", "*.json"),))
    if fichier_actuel:
        try:
            data = {"sommets": sommet_list, "aretes": arete_list}
            with open(fichier_actuel, 'w') as f:
                json.dump(data, f)
            reset_modifications()
            messagebox.showinfo("Enregistrer", f"Fichier enregistré sous : {fichier_actuel}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")

def charger_graphe(data):
    global sommet_list, arete_list, sommet_count
    nouveau_fichier()
    sommet_list = data["sommets"]
    sommet_count = len(sommet_list)
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    arete_list = data["aretes"]
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)            


# Menu
menu_bar = Menu(root)
menu_affichage = Menu(menu_bar, tearoff=0)
menu_affichage.add_command(label="Graphe", command=ouvrir_fichier)
menu_affichage.add_command(label="Matrice d'Adjacence", command=afficher_matrice_adjacence)
menu_affichage.add_command(label="Matrice d'Incidence", command=afficher_matrice_incidence)
menu_affichage.add_command(label="Chaîne eulérienne", command=verifier_chaine_eulerienne)
menu_affichage.add_command(label="Chemin", command=trouver_chemin)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)

root.config(menu=menu_bar)
root.mainloop()