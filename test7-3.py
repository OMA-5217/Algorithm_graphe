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

def effacer_sommet(event):
    global sommet_list, arete_list
    x, y = event.x, event.y
    sommet_a_effacer = None
    rayon_selection = 20

    for i, (sx, sy) in enumerate(sommet_list):
        distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
        if distance <= rayon_selection:
            sommet_a_effacer = (sx, sy)
            break

    if sommet_a_effacer:
        sommet_list.remove(sommet_a_effacer)
        arete_list = [arete for arete in arete_list if sommet_a_effacer not in arete]
        canvas.delete("all")
        recharger_affichage()
        notifier_modification()
    else:
        messagebox.showwarning("Erreur", "Aucun sommet trouvé à proximité.")

def effacer_arete(event):
    global arete_list
    x, y = event.x, event.y
    arete_a_effacer = None
    rayon_selection = 5

    for (x1, y1), (x2, y2) in arete_list:
        distance = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        if distance <= rayon_selection:
            arete_a_effacer = ((x1, y1), (x2, y2))
            break

    if arete_a_effacer:
        arete_list.remove(arete_a_effacer)
        canvas.delete("all")
        recharger_affichage()
        notifier_modification()
    else:
        messagebox.showwarning("Erreur", "Aucune arête trouvée à proximité.")

def recharger_affichage():
    """Recharge les sommets et arêtes sur le canvas à partir des listes."""
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

def activer_mode_effacer_sommet():
    canvas.bind("<Button-1>", effacer_sommet)
    messagebox.showinfo("Mode Effacer Sommet", "Cliquez sur un sommet pour l'effacer avec ses arêtes associées")

def activer_mode_effacer_arete():
    canvas.bind("<Button-1>", effacer_arete)
    messagebox.showinfo("Mode Effacer Arête", "Cliquez sur une arête pour l'effacer")


def rafraichir_canvas():
    """Réinitialise le canvas et redessine les sommets et arêtes."""
    canvas.delete("all")
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
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
        fichier_actuel = filedialog.asksaveasfilename(
            title="Enregistrer sous", defaultextension=".json", filetypes=(("Fichiers JSON", "*.json"),)
        )
    if fichier_actuel:
        try:
            data = {
                "sommets": [list(s) for s in sommet_list],  # Convertit les tuples en listes
                "aretes": [[list(a[0]), list(a[1])] for a in arete_list]  # Convertit les paires en listes
            }
            with open(fichier_actuel, 'w') as f:
                json.dump(data, f, indent=4)
            reset_modifications()
            messagebox.showinfo("Enregistrer", f"Fichier enregistré sous : {fichier_actuel}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")
def charger_graphe(data):
    global sommet_list, arete_list, sommet_count
    try:
        nouveau_fichier()
        sommet_list = data.get("sommets", [])
        arete_list = data.get("aretes", [])
        if not isinstance(sommet_list, list) or not isinstance(arete_list, list):
            raise ValueError("Format des données incorrect")

        sommet_count = len(sommet_list)
        for i, (x, y) in enumerate(sommet_list):
            radius = 15
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
            canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
        for (x1, y1), (x2, y2) in arete_list:
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger le graphe : {e}")

menu_bar = Menu(root)

menu_fichier = Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", command=nouveau_fichier)
menu_fichier.add_command(label="Ouvrir", command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer", command=enregistrer_fichier)
menu_fichier.add_command(label="Enregistrer sous", command=lambda: enregistrer_fichier())
menu_fichier.add_command(label="Fermer", command=lambda: root.quit() if verifier_sauvegarde() else None)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

menu_creation = Menu(menu_bar, tearoff=0)
menu_creation.add_command(label="Sommet", command=activer_mode_sommet)
menu_creation.add_command(label="Arête", command=activer_mode_arete)
# Sous-menu Effacer dans le menu Création
menu_effacer = Menu(menu_creation, tearoff=0)
menu_effacer.add_command(label="Effacer un sommet", command=activer_mode_effacer_sommet)
menu_effacer.add_command(label="Effacer une arête",command=activer_mode_effacer_arete)
menu_creation.add_cascade(label="Effacer", menu=menu_effacer)
menu_bar.add_cascade(label="Création", menu=menu_creation)

root.config(menu=menu_bar)

# Intercepter la fermeture de la fenêtre avec le bouton "X"
root.protocol("WM_DELETE_WINDOW", fermeture_fenetre)

root.mainloop()