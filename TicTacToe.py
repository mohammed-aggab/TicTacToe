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
    """
    Demande un coup au joueur humain et vérifie que :
    - il tape bien des nombres
    - la position existe (0, 1 ou 2)
    - la case est libre
    """
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
    """
    Vérifie si 'joueur' a gagné.
    """
    # Lignes
    if plateau[0][0] == joueur and plateau[0][1] == joueur and plateau[0][2] == joueur:
        return True
    if plateau[1][0] == joueur and plateau[1][1] == joueur and plateau[1][2] == joueur:
        return True
    if plateau[2][0] == joueur and plateau[2][1] == joueur and plateau[2][2] == joueur:
        return True

    # Colonnes
    if plateau[0][0] == joueur and plateau[1][0] == joueur and plateau[2][0] == joueur:
        return True
    if plateau[0][1] == joueur and plateau[1][1] == joueur and plateau[2][1] == joueur:
        return True
    if plateau[0][2] == joueur and plateau[1][2] == joueur and plateau[2][2] == joueur:
        return True

    # Diagonales
    if plateau[0][0] == joueur and plateau[1][1] == joueur and plateau[2][2] == joueur:
        return True
    if plateau[0][2] == joueur and plateau[1][1] == joueur and plateau[2][0] == joueur:
        return True

    return False


def plateau_plein(plateau):
    """
    Vérifie s'il reste une case vide.
    """
    for ligne in plateau:
        for case in ligne:
            if case == " ":
                return False
    return True


# IA NIVEAU 1 

def coup_ia_niveau1(plateau):
    """
    IA niveau 1 : choisit une case libre au hasard.
    """
    cases_vides = []
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == " ":
                cases_vides.append((i, j))

    return random.choice(cases_vides)


#  IA NIVEAU 2

def ia_bloquer_adversaire(plateau, signe_adversaire):
    """
    Cherche une case où l'adversaire pourrait gagner au prochain coup,
    et renvoie cette position pour la bloquer.
    Retourne (ligne, colonne) ou None s'il n'y a rien à bloquer.
    """
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == " ":
                # On simule le coup de l'adversaire
                plateau[i][j] = signe_adversaire
                if a_gagne(plateau, signe_adversaire):
                    # Il gagnerait ici -> on bloque
                    plateau[i][j] = " "
                    return i, j
                # On annule la simulation
                plateau[i][j] = " "
    return None


def coup_ia_niveau2(plateau, signe_ia, signe_adversaire):
    """
    IA niveau 2 :
    1) Si l'IA peut gagner maintenant, elle joue le coup gagnant.
    2) Sinon, si l'adversaire peut gagner au prochain coup, elle bloque.
    3) Sinon, elle joue une case aléatoire (niveau 1).
    """
    # 1) Chercher un coup gagnant pour l'IA
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == " ":
                plateau[i][j] = signe_ia
                if a_gagne(plateau, signe_ia):
                    plateau[i][j] = " "  # on annule la simulation
                    return i, j
                plateau[i][j] = " "

    # 2) Bloquer l'adversaire s'il peut gagner
    blocage = ia_bloquer_adversaire(plateau, signe_adversaire)
    if blocage is not None:
        return blocage

    # 3) Sinon, jouer au hasard
    return coup_ia_niveau1(plateau)


#  IA NIVEAU 3 

def trouver_coup_gagnant(plateau, joueur):
    """
    Cherche si 'joueur' peut gagner en un coup.
    Retourne (ligne, colonne) du coup gagnant ou None.
    """
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == " ":
                plateau[i][j] = joueur
                if a_gagne(plateau, joueur):
                    plateau[i][j] = " "
                    return (i, j)
                plateau[i][j] = " "
    return None


def coup_ia_niveau3(plateau, signe_ia, signe_adversaire):
    """
    IA niveau 3  :
    1) Si l'IA peut gagner  elle joue ce coup.
    2) Sinon, si l'adversaire peut gagner  elle le bloque.
    3) Sinon, elle prend le centre si possible.
    4) Sinon, elle prend un coin au hasard.
    5) Sinon, elle joue une case libre au hasard.
    """

    # 1) Coup gagnant pour l'IA
    coup_gagnant = trouver_coup_gagnant(plateau, signe_ia)
    if coup_gagnant:
        return coup_gagnant

    # 2) Bloquer l'adversaire
    coup_bloque = trouver_coup_gagnant(plateau, signe_adversaire)
    if coup_bloque:
        return coup_bloque

    # 3) Prendre le centre
    if plateau[1][1] == " ":
        return (1, 1)

    # 4) Prendre un coin
    coins = [(0, 0), (0, 2), (2, 0), (2, 2)]
    coins_libres = [(i, j) for (i, j) in coins if plateau[i][j] == " "]
    if coins_libres:
        return random.choice(coins_libres)

    # 5) Sinon, jouer une case libre au hasard
    return coup_ia_niveau1(plateau)


# PROGRAMME PRINCIPAL 

# Choix du mode de jeu
mode = ""
while mode not in ["1", "2", "3", "4"]:
    print("Choisis le mode de jeu :")
    print("1 - Joueur vs Joueur (1v1)")
    print("2 - Joueur vs Ordinateur (IA niveau 1 : au hasard)")
    print("3 - Joueur vs Ordinateur (IA niveau 2 : bloque + gagne)")
    print("4 - Joueur vs Ordinateur (IA niveau 3 : stratégie forte)")
    mode = input("Ton choix (1, 2, 3 ou 4) : ")

vs_ordi = (mode in ["2", "3", "4"])
niveau_ia = 0
if mode == "2":
    niveau_ia = 1
elif mode == "3":
    niveau_ia = 2
elif mode == "4":
    niveau_ia = 3

plateau = creer_plateau()
joueur = "X"  # Le joueur humain principal sera toujours "X"

if vs_ordi:
    if niveau_ia == 1:
        print("Mode Joueur vs Ordinateur (IA niveau 1 - au hasard)")
    elif niveau_ia == 2:
        print("Mode Joueur vs Ordinateur (IA niveau 2 - bloque l'adversaire et tente de gagner)")
    elif niveau_ia == 3:
        print("Mode Joueur vs Ordinateur (IA niveau 3 - stratégie forte pour collégien)")
    print("Tu joues avec 'X', l'ordinateur joue avec 'O'.")
else:
    print("Mode Joueur vs Joueur (1v1)")

# Boucle de jeu
while True:
    afficher_plateau(plateau)
    print("Tour du joueur :", joueur)

    # Tour de l'ordinateur
    if vs_ordi and joueur == "O":
        print("L'ordinateur réfléchit...")
        if niveau_ia == 1:
            ligne, colonne = coup_ia_niveau1(plateau)
        elif niveau_ia == 2:
            ligne, colonne = coup_ia_niveau2(plateau, "O", "X")
        elif niveau_ia == 3:
            ligne, colonne = coup_ia_niveau3(plateau, "O", "X")
        print("L'ordinateur joue en :", ligne, colonne)
    else:
        # Tour d'un joueur humain
        ligne, colonne = demander_coup(plateau)

    plateau[ligne][colonne] = joueur

    # Vérifier la victoire
    if a_gagne(plateau, joueur):
        afficher_plateau(plateau)
        if vs_ordi and joueur == "O":
            print("L'ordinateur a gagné !")
        else:
            print("Le joueur", joueur, "a gagné !")
        break

    # Vérifier le match nul
    if plateau_plein(plateau):
        afficher_plateau(plateau)
        print("Match nul !")
        break

    # Changer de joueur
    if joueur == "X":
        joueur = "O"
    else:
        joueur = "X"
