from tkinter import *
from tkinter import Menu, filedialog, messagebox
import os
import json
import math

root = Tk()
root.title("Menu")
root.geometry("600x500")
root.resizable(height=False,width=False)

sommet_list = []
arete_list = []
sommet_count = 0
selected_sommets = []

# Section principale : Canvas (zone de dessin) et panneau d'affichage
canvas = Canvas(root, bg="white", width=600)
canvas.pack(fill="both", expand=True)

#un section en bas pour afficher des information comme le matrice dans le fenetre parincipale
panneau_affichage = Frame(root, bg="white", width=200)
panneau_affichage.pack( fill="both",expand=True)

# le partir qui sa sera affiche dans panneau
contenu_affichage = Text(panneau_affichage, wrap="none", bg="white", height=10, width=10)
contenu_affichage.pack(fill="both", expand=True)

#creatrion de sommet 
def creation_sommet(event):
    #la meme que seul qui declare
    global sommet_count
    x, y = event.x, event.y  #copteur les coordonne clic dans le canvas
    rayon_min = 40  # Distance minimale entre deux sommets

    # Vérification de la proximité des autres sommets
    for (sx, sy) in sommet_list:
        distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
        if distance < rayon_min:
            messagebox.showwarning("Erreur", "Un sommet est déjà trop proche.")
            return  # Ne crée pas de sommet si un autre est trop proche

    # Si aucune proximité détectée, créer le sommet
    sommet_count += 1
    sommet_list.append((x, y)) #ajoute des sommets
    radius = 15
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black") # dessin un cercle
    canvas.create_text(x, y, text=str(sommet_count), font=("Arial", 12)) #ajoute un numero au centre du sommet
#creation des aretes
def creation_arete(event):
    global selected_sommets
    x, y = event.x, event.y
    sommet_proche = None
    distance_min = float('inf') #initialisation la distance_min a l'infini
  #parcourt  les sommets  pour trouve celui le plus proche a 20pixels ou moins
    for i, (sx, sy) in enumerate(sommet_list):
        distance = math.sqrt((sx - x) ** 2 + (sy - y) ** 2)
        if distance < distance_min and distance <= 20:
            distance_min = distance
            sommet_proche = (sx, sy, i + 1)
    #Ajoute le sommet trouve a selected_sommets
    if sommet_proche:
        selected_sommets.append(sommet_proche)
     #quand deux sommets sont selection les coordonnes de chacun son stockees
    if len(selected_sommets) == 2:
        x1, y1, num1 = selected_sommets[0]
        x2, y2, num2 = selected_sommets[1]

        # Vérification si l'arête existe déjà
        if ((x1, y1), (x2, y2)) in arete_list or ((x2, y2), (x1, y1)) in arete_list:
            messagebox.showwarning("Erreur", "Une arête existe déjà entre ces sommets.")
            selected_sommets = []
            return  # Ne crée pas d'arête si elle existe déjà

        # Création de l'arête si elle n'existe pas encore dans le arete list
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
        arete_list.append(((x1, y1), (x2, y2)))
        selected_sommets = []
# associe a un clic gouche a la fonction de creation de sommets
def activer_mode_sommet():
    canvas.bind("<Button-1>", creation_sommet)
    messagebox.showinfo("Mode Sommet", "Cliquez sur la zone blanche pour ajouter des sommets")

# associe a un clic gouche a la fonction de creation de aretes
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
#cette foncetion 
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




# Fonction pour afficher le graphe
def afficher_graphe():
    for (x1, y1), (x2, y2) in arete_list:
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
    messagebox.showinfo("Affichage", "Affichage du graphe terminé")


# Fonction pour afficher des informations dans le panneau
def afficher_dans_panneau(texte):
    contenu_affichage.delete(1.0, END)
    contenu_affichage.insert(END, texte)


# Fonctions liées aux matrices adjance
def afficher_matrice_adjacence():
    n = len(sommet_list)
    matrice = [[0] * n for _ in range(n)]

    for (x1, y1), (x2, y2) in arete_list:
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][j] = matrice[j][i] = 1  # Graphe non orienté

    texte = "Matrice d'adjacence :\n"
    texte += "\n".join([" ".join(map(str, ligne)) for ligne in matrice])
    afficher_dans_panneau(texte)

def afficher_matrice_incidence():
    n = len(sommet_list)
    m = len(arete_list)
    matrice = [[0] * m for _ in range(n)]

    for k, ((x1, y1), (x2, y2)) in enumerate(arete_list):
        i = sommet_list.index((x1, y1))
        j = sommet_list.index((x2, y2))
        matrice[i][k] = matrice[j][k] = 1  # Graphe non orienté

    texte = "Matrice d'incidence :\n"
    texte += "\n".join([" ".join(map(str, ligne)) for ligne in matrice])
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

    def dfs(chemin, cible, visite):
        sommet_actuel = chemin[-1]
        if sommet_actuel == cible:
            return chemin
        
        for (x1, y1), (x2, y2) in arete_list:
            voisin = None
            if sommet_list.index((x1, y1)) == sommet_actuel and sommet_list.index((x2, y2)) not in visite:
                voisin = sommet_list.index((x2, y2))
            elif sommet_list.index((x2, y2)) == sommet_actuel and sommet_list.index((x1, y1)) not in visite:
                voisin = sommet_list.index((x1, y1))
            
            if voisin is not None:
                chemin.append(voisin)
                visite.add(voisin)
                result = dfs(chemin, cible, visite)
                if result:
                    return result
                chemin.pop()
                visite.remove(voisin)

        return None

    def choisir_chemin():
        def valider():
            try:
                s, c = int(source.get()) - 1, int(cible.get()) - 1
                chemin = dfs([s], c, {s})
                if chemin:
                    texte = f"Chemin trouvé : {' -> '.join(map(str, [x + 1 for x in chemin]))}\n"
                    for i in range(len(chemin) - 1):
                        x1, y1 = sommet_list[chemin[i]]
                        x2, y2 = sommet_list[chemin[i + 1]]
                        canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
                    afficher_dans_panneau(texte)
                else:
                    afficher_dans_panneau("Erreur : Aucun chemin trouvé.")
                fenetre.destroy()
            except Exception:
                afficher_dans_panneau("Erreur : Entrées invalides.")

        fenetre = Toplevel(root)
        fenetre.title("Sélectionner le chemin")

        Label(fenetre, text="sommets depart  (1 - {}) :".format(len(sommet_list))).pack()
        source = Entry(fenetre)
        source.pack()

        Label(fenetre, text="Sommets arrive (1 - {}) :".format(len(sommet_list))).pack()
        cible = Entry(fenetre)
        cible.pack()

        Button(fenetre, text="Entre", command=valider).pack()

    choisir_chemin()

def charger_graphe(data):
    global sommet_list, arete_list, sommet_count
    nouveau_fichier()
    sommet_list = data["sommets"]
    #met a joure le compteur des sommet en fonction de liste de chargee
    sommet_count = len(sommet_list)
    for i, (x, y) in enumerate(sommet_list):
        radius = 15
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12))
    #extrait la list des arete depuis le fichier json
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


# Mise à jour du menu Affichage
menu_affichage = Menu(menu_bar, tearoff=0)
menu_affichage.add_command(label="Graphe",command=afficher_graphe)
menu_martices=Menu(menu_affichage,tearoff=0)
menu_martices.add_command(label="Matrice adjacent",command=afficher_matrice_adjacence)
menu_martices.add_command(label="Matrice incident",command=afficher_matrice_incidence)
menu_affichage.add_cascade(label="Matrice",menu=menu_martices)
menu_affichage.add_command(label="Chaîne eulérienne", command=verifier_chaine_eulerienne)
menu_affichage.add_command(label="Chemin", command=colorer_chemin)
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