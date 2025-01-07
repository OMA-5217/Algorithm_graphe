from tkinter import *
from tkinter import Menu, filedialog, messagebox,simpledialog
import tkinter as tk
import json
import math
from collections import deque
import  random


root = Tk()
root.title("Menu")
root.geometry("600x500")
root.resizable(height=False,width=False)

sommet_list = [] 
arete_list = []
sommet_count = 0
selected_sommets = []
modifications_apportees = False

# Section principale : Canvas (zone de dessin) et panneau d'affichage
canvas = Canvas(root, bg="white", width=600)
canvas.pack(fill="both", expand=True)

panneau_affichage = Frame(root, bg="white", width=200)
panneau_affichage.pack( fill="both",expand=True)



contenu_affichage = Text(panneau_affichage, wrap="none", bg="white", height=5, width=10)
contenu_affichage.pack(padx=10, pady=10, fill="both", expand=True)


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
    if  verifier_sauvegarde():
        root.destroy()

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
    notifier_modification()

# Nouveau dictionnaire pour stocker les distances des arêtes
arete_distances = {}
arete_etiquettes = {}

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
    
    # Quand deux sommets sont sélectionnés, on crée l'arête
    if len(selected_sommets) == 2:
        x1, y1, num1 = selected_sommets[0]
        x2, y2, num2 = selected_sommets[1]

        # Vérification si l'arête existe déjà
        if ((x1, y1), (x2, y2)) in arete_list or ((x2, y2), (x1, y1)) in arete_list:
            messagebox.showwarning("Erreur", "Une arête existe déjà entre ces sommets.")
            selected_sommets = []
            return  # Ne crée pas d'arête si elle existe déjà

        # Demander à l'utilisateur de saisir une distance
        distance = simpledialog.askinteger("Distance", "Entrez la distance de l'arête (en entier) :", parent=root)
        if distance is None:
            selected_sommets = []
            return  # Annuler la création de l'arête si aucune distance n'est fournie

        # Création de l'arête si elle n'existe pas encore
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
        arete_list.append(((x1, y1), (x2, y2)))
        arete_distances[((x1, y1), (x2, y2))] = distance

        # Générer une étiquette unique pour l'arête (E1, E2, ...)
        etiquette = f"E{len(arete_list)}"
        arete_etiquettes[((x1, y1), (x2, y2))] = etiquette
        
        # Affichage de l'étiquette et de la distance légèrement au-dessus de l'arête
        x_text = (x1 + x2) / 2
        y_text = (y1 + y2) / 2 - 10  # Décalage vertical pour afficher au-dessus
        canvas.create_text(x_text, y_text + 10, text=etiquette, font=("Arial", 12, "bold"), fill="red")  # Afficher l'étiquette
        canvas.create_text(x_text, y_text - 10, text=str(distance), font=("Arial", 12, "bold"), fill="blue")  # Afficher la distance

        selected_sommets = []
        notifier_modification()


def creation_arete_orientee(event):
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
    
    # Quand deux sommets sont sélectionnés, on crée l'arête orientée
    if len(selected_sommets) == 2:
        x1, y1, num1 = selected_sommets[0]
        x2, y2, num2 = selected_sommets[1]

        # Vérification si l'arête existe déjà dans le sens donné
        if ((x1, y1), (x2, y2)) in arete_list:
            messagebox.showwarning("Erreur", "Une arête orientée existe déjà dans ce sens entre ces sommets.")
            selected_sommets = []
            return  # Ne crée pas d'arête si elle existe déjà

        # Demander à l'utilisateur de saisir une distance
        distance = simpledialog.askinteger("Distance", "Entrez la distance de l'arête orientée (en entier) :", parent=root)
        if distance is None:
            selected_sommets = []
            return  # Annuler la création de l'arête si aucune distance n'est fournie

        # Création de l'arête orientée
        arete_list.append(((x1, y1), (x2, y2)))
        arete_distances[((x1, y1), (x2, y2))] = distance

        # Générer une étiquette unique pour l'arête (E1, E2, ...)
        etiquette = f"E{len(arete_list)}"
        arete_etiquettes[((x1, y1), (x2, y2))] = etiquette

        # Dessiner une ligne avec une flèche pour représenter l'arête orientée
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black", width=2)

        # Affichage de l'étiquette et de la distance légèrement au-dessus de l'arête
        x_text = (x1 + x2) / 2
        y_text = (y1 + y2) / 2 - 10  # Décalage vertical pour afficher au-dessus
        canvas.create_text(x_text, y_text + 10, text=etiquette, font=("Arial", 12, "bold"), fill="red")  # Afficher l'étiquette
        canvas.create_text(x_text, y_text - 10, text=str(distance), font=("Arial", 12, "bold"), fill="blue")  # Afficher la distance

        selected_sommets = []
        notifier_modification()       

def activer_mode_sommet():
    canvas.bind("<Button-1>", creation_sommet)
    messagebox.showinfo("Mode Sommet", "Cliquez sur la zone blanche pour ajouter des sommets")

def activer_mode_arete_non_orientee():
    canvas.bind("<Button-1>", creation_arete)
    messagebox.showinfo("Mode Arête", "Cliquez sur deux sommets pour ajouter une arête")

def activer_mode_arete_orientee():
    canvas.bind("<Button-1>", creation_arete_orientee)
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
            notifier_modification()
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
            notifier_modification()
            return



def redraw_canvas():
    """Redessine le graphe sur le canvas sans changer la structure des sommets et arêtes."""
    canvas.delete("all")  # Efface tout sur le canvas

    # Dessiner les sommets
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
        canvas.create_text(x, y, text=f"{i + 1}", font=("Arial", 12), fill="black")  # Étiquette du sommet

    # Dessiner les arêtes orientées
    for idx, ((x1, y1), (x2, y2)) in enumerate(arete_list):
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black", width=2)

        # Calcul de la position pour afficher l'étiquette et la distance au centre de l'arête
        x_text = (x1 + x2) / 2
        y_text = (y1 + y2) / 2 - 10  # Décalage vertical pour afficher au-dessus

        # Afficher l'étiquette de l'arête
        etiquette = arete_etiquettes.get(((x1, y1), (x2, y2)), None)
        if etiquette:
            canvas.create_text(x_text, y_text + 10, text=etiquette, font=("Arial", 12, "bold"), fill="red")

        # Afficher la distance de l'arête
        distance = arete_distances.get(((x1, y1), (x2, y2)), None)
        if distance is not None:
            canvas.create_text(x_text, y_text - 10, text=str(distance), font=("Arial", 12, "bold"), fill="blue")



def nouveau_fichier():
    global sommet_list, arete_list, sommet_count, selected_sommets
    if not verifier_sauvegarde():
        return
    sommet_list = []
    arete_list = []
    sommet_count = 0
    selected_sommets = []
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
                reset_modifications()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")

def enregistrer_fichier():
    fichier = filedialog.asksaveasfilename(
        title="Enregistrer sous",
        defaultextension=".json",
        filetypes=(("Fichiers JSON", "*.json"),)
    )
    # Vérifie si l'utilisateur a sélectionné un emplacement
    if fichier:
        try:
            with open(fichier, 'w') as f:
                # Crée un dictionnaire contenant les sommets et les arêtes avec distances et étiquettes
                data = {
                    "sommets": sommet_list,
                    "aretes": [
                        {
                            "sommet1": list(arete[0]),
                            "sommet2": list(arete[1]),
                            "distance": arete_distances.get(arete, 0),
                            "etiquette": arete_etiquettes.get(arete, f"E{idx + 1}")
                        }
                        for idx, arete in enumerate(arete_list)
                    ]
                }
                json.dump(data, f, indent=4)
            reset_modifications()
            messagebox.showinfo("Enregistrer", f"Fichier enregistré sous : {fichier}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")




# Fonction pour afficher le graphe
#def afficher_graphe():
  #  for (x1, y1), (x2, y2) in arete_list:
      #  canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
   # messagebox.showinfo("Affichage", "Affichage du graphe terminé")
def afficher_graphe():
    global sommet_list, arete_list
    fichier = filedialog.askopenfilename(title="Ouvrir un graphe", filetypes=(("Fichiers JSON", "*.json"),))
    if fichier:
        try:
            with open(fichier, 'r') as f:
                data = json.load(f)
                charger_graphe(data)
               
                messagebox.showinfo("Graphe chargé", "Le graphe a été chargé avec succès.")
            for (x1, y1), (x2, y2) in arete_list:
                 canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le graphe : {e}")


# Fonction pour afficher des informations dans le panneau
def afficher_dans_panneau(texte):
    contenu_affichage.delete(1.0, END)
    contenu_affichage.insert(END, texte)

# Fonctions liées aux matrices et chaînes
def afficher_matrice_adjacence():
    n = len(sommet_list)
    matrice = [[0] * n for _ in range(n)]

    for (x1, y1), (x2, y2) in arete_list:
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][j] = matrice[j][i] = 1  # Graphe non orienté

    texte = "Matrice d'adjacence :\n"
    for i, ligne in enumerate(matrice):
        texte += f"{i + 1} : " + "  ".join(map(str, ligne)) + "\n"  # Numérotation des sommets

    #texte += "\n".join(["| ".join(map(str, ligne)) for ligne in matrice])
    afficher_dans_panneau(texte)

def afficher_matrice_incidence():
    if not sommet_list or not arete_list:
        messagebox.showwarning("Erreur", "Le graphe est vide.")
        return

    n = len(sommet_list)  # Nombre de sommets
    m = len(arete_list)   # Nombre d'arêtes
    matrice = [[0] * m for _ in range(n)]

    # Remplir la matrice d'incidence
    for k, ((x1, y1), (x2, y2)) in enumerate(arete_list):
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][k] = matrice[j][k] = 1  # Graphe non orienté

    # Générer les étiquettes des arêtes
    etiquettes_aretes = [f"E{k + 1}" for k in range(m)]

    # Construire le texte de la matrice avec les étiquettes
    texte = "Matrice d'incidence :\n"
    texte += "   " + " ".join(etiquettes_aretes) + "\n"  # Ligne des étiquettes
    for i, ligne in enumerate(matrice):
        texte += f"{i + 1} : " + "  ".join(map(str, ligne)) + "\n"  # Numérotation des sommets

    # Afficher dans le panneau
    afficher_dans_panneau(texte)

def verifier_chaine_eulerienne():
    def trouver_chaine_eulerienne():
        # Crée une copie des arêtes pour ne pas les modifier directement
        aretes_restantes = arete_list[:]
        chemin = []

        def dfs(sommet, chemin):
            for i, ((x1, y1), (x2, y2)) in enumerate(aretes_restantes):
                if sommet == (x1, y1) or sommet == (x2, y2):
                    # Retirer l'arête utilisée et continuer le parcours
                    prochain_sommet = (x2, y2) if sommet == (x1, y1) else (x1, y1)
                    chemin.append((sommet, prochain_sommet))
                    aretes_restantes.pop(i)
                    dfs(prochain_sommet, chemin)
                    break

        # Trouver un sommet de départ avec un degré impair ou le premier sommet disponible
        sommet_depart = sommet_list[0]
        for (x, y) in sommet_list:
            degre = sum(1 for ar in arete_list if (x, y) in ar)
            if degre % 2 != 0:
                sommet_depart = (x, y)
                break

        dfs(sommet_depart, chemin)
        return chemin if not aretes_restantes else None

    chemin_eulerien = trouver_chaine_eulerienne()

    if chemin_eulerien:
        texte = "Chaîne eulérienne trouvée :\n"
        texte += " -> ".join(f"({sommet_list.index(s1)+1})" for s1, _ in chemin_eulerien)
        afficher_dans_panneau(texte)

        # Dessiner la chaîne eulérienne en rouge
        for (s1, s2) in chemin_eulerien:
            x1, y1 = s1
            x2, y2 = s2
            canvas.create_line(x1, y1, x2, y2, fill="green", width=3)
    else:
        afficher_dans_panneau("Erreur : Pas de chaîne eulérienne trouvée.")

def colorer_chemin():
    if len(sommet_list) < 2:
        afficher_dans_panneau("Erreur : Il faut au moins deux sommets.")
        return

    def trouver_tous_les_chemins(sommet_depart, sommet_arrivee, visite, chemin_actuel, chemins):
        visite.add(sommet_depart)
        chemin_actuel.append(sommet_depart)

        if sommet_depart == sommet_arrivee:
            # Ajouter une copie du chemin actuel à la liste des chemins
            chemins.append(list(chemin_actuel))
        else:
            # Explorer les voisins du sommet actuel
            for (x1, y1), (x2, y2) in arete_list:
                voisin = None
                if sommet_list.index((x1, y1)) == sommet_depart and sommet_list.index((x2, y2)) not in visite:
                    voisin = sommet_list.index((x2, y2))
                elif sommet_list.index((x2, y2)) == sommet_depart and sommet_list.index((x1, y1)) not in visite:
                    voisin = sommet_list.index((x1, y1))

                if voisin is not None:
                    trouver_tous_les_chemins(voisin, sommet_arrivee, visite, chemin_actuel, chemins)

        # Backtracking
        visite.remove(sommet_depart)
        chemin_actuel.pop()

    def choisir_chemin():
        def valider():
            try:
                sommet_depart = int(source.get()) - 1
                sommet_arrivee = int(cible.get()) - 1

                if sommet_depart < 0 or sommet_depart >= len(sommet_list) or sommet_arrivee < 0 or sommet_arrivee >= len(sommet_list):
                    raise ValueError("Sommet hors limite.")

                chemins = []
                trouver_tous_les_chemins(sommet_depart, sommet_arrivee, set(), [], chemins)

                if chemins:
                    texte = f"Chemins possibles entre {sommet_depart + 1} et {sommet_arrivee + 1} :\n"
                    for chemin in chemins:
                        texte += " -> ".join(map(lambda x: str(x + 1), chemin)) + "\n"

                        # Colorer chaque chemin avec une couleur unique
                        couleur = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                        for i in range(len(chemin) - 1):
                            x1, y1 = sommet_list[chemin[i]]
                            x2, y2 = sommet_list[chemin[i + 1]]
                            canvas.create_line(x1, y1, x2, y2, fill=couleur, width=3)

                    afficher_dans_panneau(texte)
                else:
                    afficher_dans_panneau("Erreur : Aucun chemin trouvé.")
                
                fenetre.destroy()
            except Exception:
                afficher_dans_panneau("Erreur : Entrées invalides.")

        fenetre = Toplevel(root)
        fenetre.title("Sélectionner les sommets")

        Label(fenetre, text="Sommet de départ (1 - {}) :".format(len(sommet_list))).pack()
        source = Entry(fenetre)
        source.pack()

        Label(fenetre, text="Sommet d'arrivée (1 - {}) :".format(len(sommet_list))).pack()
        cible = Entry(fenetre)
        cible.pack()

        Button(fenetre, text="Valider", command=valider).pack()

    choisir_chemin()


# Fonction pour le parcours en largeur
def parcours_largeur():
    if not sommet_list:
        messagebox.showwarning("Erreur", "Le graphe est vide.")
        return

    def bfs(sommet_depart):
        visite = set()
        file = deque([sommet_depart])
        resultat = []

        while file:
            sommet_actuel = file.popleft()
            if sommet_actuel not in visite:
                visite.add(sommet_actuel)
                resultat.append(sommet_actuel)
                # Ajouter les voisins non visités
                for (x1, y1), (x2, y2) in arete_list:
                    if sommet_actuel == sommet_list.index((x1, y1)) + 1:
                        voisin = sommet_list.index((x2, y2)) + 1
                    elif sommet_actuel == sommet_list.index((x2, y2)) + 1:
                        voisin = sommet_list.index((x1, y1)) + 1
                    else:
                        continue
                    if voisin not in visite:
                        file.append(voisin)
        return resultat

    sommet_depart = simpledialog.askinteger("Parcours en largeur", f"Entrez le sommet de départ (1-{len(sommet_list)}) :")
    if sommet_depart and 1 <= sommet_depart <= len(sommet_list):
        resultat = bfs(sommet_depart)
        texte = f"Parcours en largeur depuis {sommet_depart} : {' -> '.join(map(str, resultat))}"
        afficher_dans_panneau(texte)
    else:
        messagebox.showwarning("Erreur", "Sommet de départ invalide.")

# Fonction pour le parcours en profondeur
def parcours_profondeur():
    if not sommet_list:
        messagebox.showwarning("Erreur", "Le graphe est vide.")
        return

    def dfs(sommet_actuel, visite, resultat):
        visite.add(sommet_actuel)
        resultat.append(sommet_actuel)
        # Parcourir les voisins
        for (x1, y1), (x2, y2) in arete_list:
            if sommet_actuel == sommet_list.index((x1, y1)) + 1:
                voisin = sommet_list.index((x2, y2)) + 1
            elif sommet_actuel == sommet_list.index((x2, y2)) + 1:
                voisin = sommet_list.index((x1, y1)) + 1
            else:
                continue
            if voisin not in visite:
                dfs(voisin, visite, resultat)

    sommet_depart = simpledialog.askinteger("Parcours en profondeur", f"Entrez le sommet de départ (1-{len(sommet_list)}) :")
    if sommet_depart and 1 <= sommet_depart <= len(sommet_list):
        visite = set()
        resultat = []
        dfs(sommet_depart, visite, resultat)
        texte = f"Parcours en profondeur depuis {sommet_depart} : {' -> '.join(map(str, resultat))}"
        afficher_dans_panneau(texte)
    else:
        messagebox.showwarning("Erreur", "Sommet de départ invalide.")


def afficher_plus_court_chemin():
    if len(sommet_list) < 2 or not arete_list:
        afficher_dans_panneau("Erreur : Le graphe doit contenir au moins deux sommets et des arêtes.")
        return

    def dijkstra(depart, arrivee):
        # Initialisation
        n = len(sommet_list)
        distances = [float('inf')] * n
        predecesseurs = [-1] * n
        distances[depart] = 0
        visite = set()

        for _ in range(n):
            # Trouver le sommet non visité avec la plus petite distance
            sommet_actuel = -1
            min_distance = float('inf')
            for i in range(n):
                if i not in visite and distances[i] < min_distance:
                    sommet_actuel = i
                    min_distance = distances[i]

            if sommet_actuel == -1:
                break  # Tous les sommets accessibles ont été visités

            visite.add(sommet_actuel)

            # Mettre à jour les distances des voisins
            for (x1, y1), (x2, y2) in arete_list:
                voisin = -1
                if sommet_list[sommet_actuel] == (x1, y1):
                    voisin = sommet_list.index((x2, y2))
                elif sommet_list[sommet_actuel] == (x2, y2):
                    voisin = sommet_list.index((x1, y1))

                if voisin != -1 and voisin not in visite:
                    distance = arete_distances[((x1, y1), (x2, y2))]
                    if distances[sommet_actuel] + distance < distances[voisin]:
                        distances[voisin] = distances[sommet_actuel] + distance
                        predecesseurs[voisin] = sommet_actuel

        # Reconstruire le chemin
        chemin = []
        sommet_courant = arrivee
        while sommet_courant != -1:
            chemin.insert(0, sommet_courant)
            sommet_courant = predecesseurs[sommet_courant]

        return chemin, distances[arrivee]

    def choisir_sommets():
        def valider():
            try:
                sommet_depart = int(source.get()) - 1
                sommet_arrivee = int(cible.get()) - 1

                if sommet_depart < 0 or sommet_depart >= len(sommet_list) or sommet_arrivee < 0 or sommet_arrivee >= len(sommet_list):
                    raise ValueError("Indices de sommets non valides.")

                chemin, distance = dijkstra(sommet_depart, sommet_arrivee)

                if distance == float('inf'):
                    afficher_dans_panneau("Erreur : Aucun chemin trouvé entre les sommets sélectionnés.")
                else:
                    texte = f"Plus court chemin avec Algorithme Dijkstra ({distance} unités) :\n"
                    texte += " -> ".join(f"{i + 1}" for i in chemin)
                    afficher_dans_panneau(texte)

                    # Colorer le chemin sur le canvas
                    for i in range(len(chemin) - 1):
                        x1, y1 = sommet_list[chemin[i]]
                        x2, y2 = sommet_list[chemin[i + 1]]
                        canvas.create_line(x1, y1, x2, y2, fill="green", width=3)

                fenetre.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        fenetre = Toplevel(root)
        fenetre.title("Choisir les sommets")
        Label(fenetre, text="Sommet de départ :").pack(pady=5)
        source = Entry(fenetre)
        source.pack(pady=5)

        Label(fenetre, text="Sommet d'arrivée :").pack(pady=5)
        cible = Entry(fenetre)
        cible.pack(pady=5)

        Button(fenetre, text="Valider", command=valider).pack(pady=10)

    choisir_sommets()



def afficher_plus_court_chemin_bellman_ford():
    if len(sommet_list) < 2 or not arete_list:
        afficher_dans_panneau("Erreur : Le graphe doit contenir au moins deux sommets et des arêtes.")
        return

    def bellman_ford(depart, arrivee):
        n = len(sommet_list)
        distances = [float('inf')] * n
        predecesseurs = [-1] * n
        distances[depart] = 0

        # Relaxation des arêtes
        for _ in range(n - 1):
            for (x1, y1), (x2, y2) in arete_list:
                u = sommet_list.index((x1, y1))
                v = sommet_list.index((x2, y2))
                poids = arete_distances[((x1, y1), (x2, y2))]
                if distances[u] + poids < distances[v]:
                    distances[v] = distances[u] + poids
                    predecesseurs[v] = u
                if distances[v] + poids < distances[u]:
                    distances[u] = distances[v] + poids
                    predecesseurs[u] = v

        # Vérification des cycles de poids négatif
        for (x1, y1), (x2, y2) in arete_list:
            u = sommet_list.index((x1, y1))
            v = sommet_list.index((x2, y2))
            poids = arete_distances[((x1, y1), (x2, y2))]
            if distances[u] + poids < distances[v]:
                return None, "Erreur : Cycle de poids négatif détecté."

        # Reconstruire le chemin
        chemin = []
        sommet_courant = arrivee
        while sommet_courant != -1:
            chemin.insert(0, sommet_courant)
            sommet_courant = predecesseurs[sommet_courant]

        return chemin, distances[arrivee]

    def choisir_sommets():
        def valider():
            try:
                sommet_depart = int(source.get()) - 1
                sommet_arrivee = int(cible.get()) - 1

                if sommet_depart < 0 or sommet_depart >= len(sommet_list) or sommet_arrivee < 0 or sommet_arrivee >= len(sommet_list):
                    raise ValueError("Indices de sommets non valides.")

                chemin, result = bellman_ford(sommet_depart, sommet_arrivee)

                if chemin is None:
                    afficher_dans_panneau(result)
                elif result == float('inf'):
                    afficher_dans_panneau("Erreur : Aucun chemin trouvé entre les sommets sélectionnés.")
                else:
                    texte = f"Plus court chemin avec Algorithme Bellman-Ford ({result} unités) :\n"
                    texte += " -> ".join(f"{i + 1}" for i in chemin)
                    afficher_dans_panneau(texte)

                    # Colorer le chemin sur le canvas
                    for i in range(len(chemin) - 1):
                        x1, y1 = sommet_list[chemin[i]]
                        x2, y2 = sommet_list[chemin[i + 1]]
                        canvas.create_line(x1, y1, x2, y2, fill="green", width=3)

                fenetre.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        fenetre = Toplevel(root)
        fenetre.title("Choisir les sommets")
        Label(fenetre, text="Sommet de départ :").pack(pady=5)
        source = Entry(fenetre)
        source.pack(pady=5)

        Label(fenetre, text="Sommet d'arrivée :").pack(pady=5)
        cible = Entry(fenetre)
        cible.pack(pady=5)

        Button(fenetre, text="Valider", command=valider).pack(pady=10)

    choisir_sommets()


def charger_graphe(data):
    """Charge les données du graphe depuis un fichier JSON."""
    global sommet_list, arete_list, sommet_count, arrete_num, arete_distances, arete_etiquettes
    try:
        # Vérification des clés attendues
        sommets = data.get("sommets", [])
        aretes = data.get("aretes", [])

        # Validation des types
        if not isinstance(sommets, list) or not isinstance(aretes, list):
            raise ValueError("Format invalide : 'sommets' et 'aretes' doivent être des listes.")

        # Mise à jour des données globales
        sommet_list = [tuple(sommet) for sommet in sommets]
        arete_list = [(tuple(arete["sommet1"]), tuple(arete["sommet2"])) for arete in aretes]
        arete_distances = {((tuple(arete["sommet1"]), tuple(arete["sommet2"]))): arete["distance"] for arete in aretes}
        arete_etiquettes = {((tuple(arete["sommet1"]), tuple(arete["sommet2"]))): arete["etiquette"] for arete in aretes}

        sommet_count = len(sommet_list)
        arrete_num = len(arete_list)

        # Recharge le canvas
        canvas.delete("all")

        # Dessiner les sommets
        for i, (x, y) in enumerate(sommet_list):
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="yellow", outline="black")
            canvas.create_text(x, y, text=f"{i + 1}", font=("Arial", 12), fill="black")

        # Dessiner les arêtes orientées avec étiquettes et distances
        for ((x1, y1), (x2, y2)) in arete_list:
            # Dessin de l'arête orientée
            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black", width=2)

            # Position pour l'étiquette au centre de l'arête
            x_text = (x1 + x2) / 2
            y_text = (y1 + y2) / 2 - 10

            # Récupérer la distance et l'étiquette de l'arête
            distance = arete_distances.get(((x1, y1), (x2, y2)), None)
            etiquette = arete_etiquettes.get(((x1, y1), (x2, y2)), None)

            # Ajouter l'étiquette et la distance
            if etiquette:
                canvas.create_text(x_text, y_text + 10, text=etiquette, font=("Arial", 12, "bold"), fill="red")
            if distance is not None:
                canvas.create_text(x_text, y_text - 10, text=str(distance), font=("Arial", 12, "bold"), fill="blue")

        # Réinitialiser les modifications locales
        reset_modifications()

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger le graphe : {e}")

menu_bar = Menu(root)

menu_fichier = Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", command=nouveau_fichier)
menu_fichier.add_command(label="Ouvrir", command=ouvrir_fichier)

menu_enregistrer = Menu(menu_fichier, tearoff=0)
menu_enregistrer.add_command(label="Enregistrer", command=enregistrer_fichier)
menu_enregistrer.add_command(label="Enregistrer sous", command=enregistrer_fichier)
menu_fichier.add_cascade(label="Enregistrer", menu=menu_enregistrer)

menu_fichier.add_command(label="Fermer", command=lambda: root.quit() if verifier_sauvegarde() else None)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

#menu creatrion 
menu_creation = Menu(menu_bar, tearoff=0)
menu_creation.add_command(label="Sommet", command=activer_mode_sommet)
menu_aretes=Menu(menu_creation,tearoff=0)
menu_aretes.add_command(label="Orientes",command=activer_mode_arete_orientee)
menu_aretes.add_command(label="Non Orientee",command=activer_mode_arete_non_orientee)
menu_creation.add_cascade(label="Aretes",menu=menu_aretes)



# Sous-menu Effacer dans le menu Création
menu_effacer = Menu(menu_creation, tearoff=0)
menu_effacer.add_command(label=" sommet", command=activer_mode_effacer_sommet)
menu_effacer.add_command(label=" Arête", command=activer_mode_effacer_arete)
menu_creation.add_cascade(label="Effacer", menu=menu_effacer)

menu_bar.add_cascade(label="Création", menu=menu_creation)


# Mise à jour du menu Affichage
menu_affichage = Menu(menu_bar, tearoff=0)
menu_affichage.add_command(label="Graphe",command=afficher_graphe)
menu_martices=Menu(menu_affichage,tearoff=0)
menu_martices.add_command(label="Adjacent",command=afficher_matrice_adjacence)
menu_martices.add_command(label="Incident",command=afficher_matrice_incidence)
menu_affichage.add_cascade(label="Matrice",menu=menu_martices)
menu_affichage.add_command(label="Chaîne eulérienne", command=verifier_chaine_eulerienne)
menu_affichage.add_command(label="Chemin", command=colorer_chemin)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)


# Mise à jour du menu Parcours
menu_parcours=Menu(menu_bar,tearoff=0)
menu_parcours.add_command(label="En Largeur",command=parcours_largeur)
menu_parcours.add_command(label="En pronfondeur",command=parcours_profondeur)
menu_bar.add_cascade(label="Parcours",menu=menu_parcours)



# ---- Menu Exécution ----
menu_execution = Menu(menu_bar, tearoff=0)
menu_plus_chemin=Menu(menu_execution,tearoff=0)
menu_plus_chemin.add_command(label="Dijkstra",command=afficher_plus_court_chemin)
menu_plus_chemin.add_command(label="Beallfe fort",command=afficher_plus_court_chemin_bellman_ford)
menu_execution.add_cascade(label="Plus court chemin",menu=menu_plus_chemin)
menu_execution.add_command(label="Coloration", command=lambda: messagebox.showinfo("Exécution", "Exécution de la coloration"))
menu_bar.add_cascade(label="Exécution", menu=menu_execution)

# ---- Menu Édition ----
menu_edition = Menu(menu_bar, tearoff=0)
menu_edition.add_command(label="Graphe", command=lambda: messagebox.showinfo("Édition", "Édition du graphe"))
menu_bar.add_cascade(label="Édition", menu=menu_edition)

root.config(menu=menu_bar)

# Intercepter la fermeture de la fenêtre avec le bouton "X"
root.protocol("WM_DELETE_WINDOW", fermeture_fenetre)


root.mainloop()