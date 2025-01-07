from tkinter import *
from tkinter import Menu, filedialog, messagebox
import json
import math

root = Tk()
root.title("Menu")
root.geometry("600x400")

sommet_list = []
arete_list = []
sommet_count = 0
selected_sommets = []
fichier_actuel = None  # Variable pour suivre le fichier en cours d'édition
modifications_apportees = False  # Variable pour suivre les modifications

# Canvas
canvas = Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

def notifier_modification():
    """Marque le graphe comme modifié."""
    global modifications_apportees
    modifications_apportees = True

def reset_modifications():
    """Réinitialise l'état des modifications."""
    global modifications_apportees
    modifications_apportees = False


def creation_sommet(event):
    global sommet_count
    x, y = event.x, event.y
    rayon_min = 40

    for (sx, sy) in sommet_list:
        distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
        if distance < rayon_min:
            messagebox.showwarning("Erreur", "Un sommet est déjà trop proche.")
            return

    sommet_count += 1
    sommet_list.append((x, y))
    radius = 15
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
    canvas.create_text(x, y, text=str(sommet_count), font=("Arial", 12))
    notifier_modification()

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

        if ((x1, y1), (x2, y2)) in arete_list or ((x2, y2), (x1, y1)) in arete_list:
            messagebox.showwarning("Erreur", "Une arête existe déjà entre ces sommets.")
            selected_sommets = []
            return

        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
        arete_list.append(((x1, y1), (x2, y2)))
        selected_sommets = []
        notifier_modification()

def activer_mode_sommet():
    canvas.bind("<Button-1>", creation_sommet)
    messagebox.showinfo("Mode Sommet", "Cliquez sur la zone blanche pour ajouter des sommets")

def activer_mode_arete():
    canvas.bind("<Button-1>", creation_arete)
    messagebox.showinfo("Mode Arête", "Cliquez sur deux sommets pour ajouter une arête")   

def verifier_sauvegarde():
    """Vérifie si des modifications doivent être enregistrées avant de poursuivre."""
    if modifications_apportees:
        reponse = messagebox.askyesnocancel("Enregistrer", "Des modifications ont été apportées. Voulez-vous les enregistrer ?")
        if reponse:  # Oui
            enregistrer_fichier()
            return True
        elif reponse is None:  # Annuler
            return False
    return True

def fermeture_fenetre():
    """Intercepte la fermeture de la fenêtre et vérifie les modifications."""
    if verifier_sauvegarde():
        root.destroy()

# --- Fonctionnalités d'affichage ---
def afficher_graphe():
    """Affiche le graphe à partir des sommets et arêtes existants."""
    canvas.delete("all")
    recharger_canvas()

def calculer_matrice_adjacence():
    """Calcule et affiche la matrice d'adjacence."""
    taille = len(sommet_list)
    matrice = [[0] * taille for _ in range(taille)]
    
    for (x1, y1), (x2, y2) in arete_list:
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][j] = 1
        matrice[j][i] = 1  # Graphe non orienté
    
    afficher_matrice("Matrice d'adjacence", matrice)

def calculer_matrice_incidence():
    """Calcule et affiche la matrice d'incidence."""
    taille_sommets = len(sommet_list)
    taille_aretes = len(arete_list)
    matrice = [[0] * taille_aretes for _ in range(taille_sommets)]
    
    for index, ((x1, y1), (x2, y2)) in enumerate(arete_list):
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][index] = 1
        matrice[j][index] = 1  # Graphe non orienté
    
    afficher_matrice("Matrice d'incidence", matrice)

def afficher_matrice(titre, matrice):
    """Affiche une matrice dans une nouvelle fenêtre."""
    fenetre = Toplevel(root)
    fenetre.title(titre)
    
    for i, ligne in enumerate(matrice):
        for j, val in enumerate(ligne):
            Label(fenetre, text=str(val), borderwidth=1, relief="solid", width=3).grid(row=i, column=j)


def effacer_sommet():
    global sommet_list, arete_list
    if not sommet_list:
        messagebox.showwarning("Erreur", "Aucun sommet à effacer.")
        return

    def suppression_sommet(event):
        x, y = event.x, event.y
        sommet_proche = None
        distance_min = float('inf')

        for i, (sx, sy) in enumerate(sommet_list):
            distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
            if distance < distance_min and distance <= 20:
                distance_min = distance
                sommet_proche = i

        if sommet_proche is not None:
            sommet_efface = sommet_list.pop(sommet_proche)

            # Supprimer les arêtes associées
            arete_list[:] = [arete for arete in arete_list if sommet_efface not in arete]

            canvas.delete("all")
            recharger_canvas()
            notifier_modification()
            canvas.unbind("<Button-1>")
        else:
            messagebox.showwarning("Erreur", "Aucun sommet proche trouvé pour effacer.")

    canvas.bind("<Button-1>", suppression_sommet)
    messagebox.showinfo("Effacer Sommet", "Cliquez sur un sommet pour l'effacer avec ses arêtes associées.")

def effacer_arete():
    
    global arete_list
    if not arete_list:
        messagebox.showwarning("Erreur", "Aucune arête à effacer.")
        return

    def suppression_arete(event):
        x, y = event.x, event.y
        arete_proche = None
        distance_min = float('inf')

        for i, ((x1, y1), (x2, y2)) in enumerate(arete_list):
            # Trouver le point milieu de l'arête pour calculer la distance
            xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
            distance = math.sqrt((xm - x) ** 2 + (ym - y)** 2)
            if distance < distance_min and distance <= 20:
                distance_min = distance
                arete_proche = i

        if arete_proche is not None:
            arete_list.pop(arete_proche)
            canvas.delete("all")
            recharger_canvas()
            notifier_modification()
            canvas.unbind("<Button-1>")
        else:
            messagebox.showwarning("Erreur", "Aucune arête proche trouvée pour effacer.")

    canvas.bind("<Button-1>", suppression_arete)
    messagebox.showinfo("Effacer Arête", "Cliquez sur une arête pour l'effacer.")

def recharger_canvas():
    # Recharge les sommets
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))

    # Recharge les arêtes
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

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

# --- Ajout dans le menu ---
menu_bar = Menu(root)

# Menu Fichier
menu_fichier = Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", command=nouveau_fichier)
menu_fichier.add_command(label="Ouvrir", command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer", command=enregistrer_fichier)
menu_fichier.add_command(label="Enregistrer sous", command=lambda: enregistrer_fichier())
menu_fichier.add_command(label="Fermer", command=lambda: root.quit() if verifier_sauvegarde() else None)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

# Menu Création
menu_creation = Menu(menu_bar, tearoff=0)
menu_creation.add_command(label="Sommet", command=activer_mode_sommet)
menu_creation.add_command(label="Arête", command=activer_mode_arete)

# Sous-menu Effacer
menu_effacer = Menu(menu_creation, tearoff=0)
menu_effacer.add_command(label="Sommet", command=effacer_sommet)
menu_effacer.add_command(label="Arête", command=effacer_arete)
menu_creation.add_cascade(label="Effacer", menu=menu_effacer)

menu_bar.add_cascade(label="Création", menu=menu_creation)

# Menu Affichage
menu_affichage = Menu(menu_bar, tearoff=0)
menu_affichage.add_command(label="Afficher Graphe", command=afficher_graphe)
menu_affichage.add_command(label="Matrice d'adjacence", command=calculer_matrice_adjacence)
menu_affichage.add_command(label="Matrice d'incidence", command=calculer_matrice_incidence)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)

root.config(menu=menu_bar)

# Intercepter la fermeture de la fenêtre avec le bouton "X"
root.protocol("WM_DELETE_WINDOW", fermeture_fenetre)

root.mainloop()