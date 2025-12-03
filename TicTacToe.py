import random  # Pour que l'IA choisisse une case au hasard

def creer_plateau():
    plateau = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    return plateau


def afficher_plateau(plateau):
    print("-------------")
    for ligne in plateau:
        print("|", ligne[0], "|", ligne[1], "|", ligne[2], "|")
        print("-------------")


def demander_coup(plateau):
    # Demande un coup au joueur humain
    ligne = input("Choisis une ligne (0, 1 ou 2) : ")
    colonne = input("Choisis une colonne (0, 1 ou 2) : ")

    # Vérifie que ce sont des nombres
    while not ligne.isdigit() or not colonne.isdigit():
        print("Tu dois entrer un nombre.")
        ligne = input("Choisis une ligne (0, 1 ou 2) : ")
        colonne = input("Choisis une colonne (0, 1 ou 2) : ")

    ligne = int(ligne)
    colonne = int(colonne)

    # Vérifie que la position existe
    while ligne < 0 or ligne > 2 or colonne < 0 or colonne > 2:
        print("Position invalide.")
        ligne = int(input("Choisis une ligne (0, 1 ou 2) : "))
        colonne = int(input("Choisis une colonne (0, 1 ou 2) : "))

    # Vérifie si la case est libre
    while plateau[ligne][colonne] != " ":
        print("Case occupée, choisis-en une autre.")
        ligne = int(input("Choisis une ligne (0, 1 ou 2) : "))
        colonne = int(input("Choisis une colonne (0, 1 ou 2) : "))

    return ligne, colonne


def a_gagne(plateau, joueur):
    # Vérifie les lignes
    if plateau[0][0] == joueur and plateau[0][1] == joueur and plateau[0][2] == joueur:
        return True
    if plateau[1][0] == joueur and plateau[1][1] == joueur and plateau[1][2] == joueur:
        return True
    if plateau[2][0] == joueur and plateau[2][1] == joueur and plateau[2][2] == joueur:
        return True

    # Vérifie les colonnes
    if plateau[0][0] == joueur and plateau[1][0] == joueur and plateau[2][0] == joueur:
        return True
    if plateau[0][1] == joueur and plateau[1][1] == joueur and plateau[2][1] == joueur:
        return True
    if plateau[0][2] == joueur and plateau[1][2] == joueur and plateau[2][2] == joueur:
        return True

    # Vérifie les diagonales
    if plateau[0][0] == joueur and plateau[1][1] == joueur and plateau[2][2] == joueur:
        return True
    if plateau[0][2] == joueur and plateau[1][1] == joueur and plateau[2][0] == joueur:
        return True

    return False


def plateau_plein(plateau):
    # Vérifie s'il reste une case vide
    for ligne in plateau:
        for case in ligne:
            if case == " ":
                return False
    return True


def coup_ia_niveau1(plateau):
    """
    IA niveau 1 : choisit une case libre au hasard.
    """
    cases_vides = []
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == " ":
                cases_vides.append((i, j))

    # On choisit une case aléatoire parmi les cases vides
    return random.choice(cases_vides)



#   PROGRAMME PRINCIPAL


# Choix du mode de jeu
mode = ""
while mode not in ["1", "2"]:
    print("Choisis le mode de jeu :")
    print("1 - Joueur vs Joueur (1v1)")
    print("2 - Joueur vs Ordinateur (IA niveau 1)")
    mode = input("Ton choix (1 ou 2) : ")

vs_ordi = (mode == "2")

plateau = creer_plateau()
joueur = "X"  # Le joueur humain principal sera toujours "X"

if vs_ordi:
    print("Mode Joueur vs Ordinateur")
    print("Tu joues avec 'X', l'ordinateur joue avec 'O'.")
else:
    print("Mode Joueur vs Joueur (1v1)")

while True:
    afficher_plateau(plateau)
    print("Tour du joueur :", joueur)

    # Si on est en mode vs ordi et que c'est au tour de l'ordi
    if vs_ordi and joueur == "O":
        print("L'ordinateur réfléchit...")
        ligne, colonne = coup_ia_niveau1(plateau)
        print("L'ordinateur joue en :", ligne, colonne)
    else:
        # Tour d'un joueur humain
        ligne, colonne = demander_coup(plateau)

    plateau[ligne][colonne] = joueur

    if a_gagne(plateau, joueur):
        afficher_plateau(plateau)
        if vs_ordi and joueur == "O":
            print("L'ordinateur a gagné !")
        else:
            print("Le joueur", joueur, "a gagné !")
        break

    if plateau_plein(plateau):
        afficher_plateau(plateau)
        print("Match nul !")
        break

    # Change de joueur
    if joueur == "X":
        joueur = "O"
    else:
        joueur = "X"
