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
    # On demande une ligne et une colonne, et on recommence si ce n'est pas valide
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
    # Vérifie si une case est vide
    for ligne in plateau:
        for case in ligne:
            if case == " ":
                return False
    return True





