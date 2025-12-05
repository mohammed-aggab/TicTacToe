import random
import pygame

# =========================================================
#               FONCTIONS LOGIQUES DU MORPION
# =========================================================

# --- Création du plateau de jeu (3x3 cases vides) ---
def creer_plateau():
    plateau = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    return plateau


# --- Affichage du plateau dans la console (mode texte) ---
def afficher_plateau(plateau):
    print("-------------")
    for ligne in plateau:
        print("|", ligne[0], "|", ligne[1], "|", ligne[2], "|")
        print("-------------")


# --- Demander un coup valide au joueur humain dans la console ---
def demander_coup(plateau):
    # On demande une ligne et une colonne au joueur
    ligne = input("Choisis une ligne (0, 1 ou 2) : ")
    colonne = input("Choisis une colonne (0, 1 ou 2) : ")

    # On vérifie que ce sont bien des chiffres
    while not ligne.isdigit() or not colonne.isdigit():
        print("Tu dois entrer un nombre.")
        ligne = input("Choisis une ligne (0, 1 ou 2) : ")
        colonne = input("Choisis une colonne (0, 1 ou 2) : ")

    ligne = int(ligne)
    colonne = int(colonne)

    # On vérifie que la position existe sur le plateau
    while ligne < 0 or ligne > 2 or colonne < 0 or colonne > 2:
        print("Position invalide.")
        ligne = int(input("Choisis une ligne (0, 1 ou 2) : "))
        colonne = int(input("Choisis une colonne (0, 1 ou 2) : "))

    # On vérifie que la case est libre
    while plateau[ligne][colonne] != " ":
        print("Case occupée, choisis-en une autre.")
        ligne = int(input("Choisis une ligne (0, 1 ou 2) : "))
        colonne = int(input("Choisis une colonne (0, 1 ou 2) : "))

    return ligne, colonne


# --- Tester si un joueur a gagné ---
def a_gagne(plateau, joueur):
    # Lignes
    if plateau[0][0] == joueur and plateau[0][1] == joueur and plateau[0][2] == joueur: return True
    if plateau[1][0] == joueur and plateau[1][1] == joueur and plateau[1][2] == joueur: return True
    if plateau[2][0] == joueur and plateau[2][1] == joueur and plateau[2][2] == joueur: return True

    # Colonnes
    if plateau[0][0] == joueur and plateau[1][0] == joueur and plateau[2][0] == joueur: return True
    if plateau[0][1] == joueur and plateau[1][1] == joueur and plateau[2][1] == joueur: return True
    if plateau[0][2] == joueur and plateau[1][2] == joueur and plateau[2][2] == joueur: return True

    # Diagonales
    if plateau[0][0] == joueur and plateau[1][1] == joueur and plateau[2][2] == joueur: return True
    if plateau[0][2] == joueur and plateau[1][1] == joueur and plateau[2][0] == joueur: return True

    return False


# --- Tester si le plateau est complètement rempli ---
def plateau_plein(plateau):
    for ligne in plateau:
        for case in ligne:
            if case == " ":
                return False
    return True


# --- IA niveau 1 : joue complètement au hasard ---
def coup_ia_niveau1(plateau):
    cases_vides = []
    for indice_ligne in range(3):
        for indice_colonne in range(3):
            if plateau[indice_ligne][indice_colonne] == " ":
                cases_vides.append((indice_ligne, indice_colonne))
    return random.choice(cases_vides)


# --- IA : tester si l'adversaire peut gagner au prochain coup et le bloquer ---
def ia_bloquer_adversaire(plateau, signe_adversaire):
    for indice_ligne in range(3):
        for indice_colonne in range(3):
            if plateau[indice_ligne][indice_colonne] == " ":
                # On simule le coup de l'adversaire
                plateau[indice_ligne][indice_colonne] = signe_adversaire
                if a_gagne(plateau, signe_adversaire):
                    # Si ça lui faisait gagner, on bloque ici
                    plateau[indice_ligne][indice_colonne] = " "
                    return indice_ligne, indice_colonne
                # Sinon on annule
                plateau[indice_ligne][indice_colonne] = " "
    return None


# --- IA niveau 2 : essaye de gagner, sinon bloque, sinon hasard ---
def coup_ia_niveau2(plateau, signe_ia, signe_adversaire):
    # 1) Cherche d'abord un coup gagnant pour l'IA
    for indice_ligne in range(3):
        for indice_colonne in range(3):
            if plateau[indice_ligne][indice_colonne] == " ":
                plateau[indice_ligne][indice_colonne] = signe_ia
                if a_gagne(plateau, signe_ia):
                    plateau[indice_ligne][indice_colonne] = " "
                    return indice_ligne, indice_colonne
                plateau[indice_ligne][indice_colonne] = " "


    # 3) Sinon joue au hasard
    return coup_ia_niveau1(plateau)


# --- Chercher un coup qui donne la victoire immédiate à un joueur ---
def trouver_coup_gagnant(plateau, joueur):
    for indice_ligne in range(3):
        for indice_colonne in range(3):
            if plateau[indice_ligne][indice_colonne] == " ":
                plateau[indice_ligne][indice_colonne] = joueur
                if a_gagne(plateau, joueur):
                    plateau[indice_ligne][indice_colonne] = " "
                    return (indice_ligne, indice_colonne)
                plateau[indice_ligne][indice_colonne] = " "
    return None


# --- IA niveau 3 : un peu "intelligente" (gagner, bloquer, centre, coins, sinon hasard) ---
def coup_ia_niveau3(plateau, signe_ia, signe_adversaire):
    # 1) Cherche un coup gagnant pour l'IA
    coup = trouver_coup_gagnant(plateau, signe_ia)
    if coup:
        return coup

    # 2) Sinon bloque l'adversaire
    coup = trouver_coup_gagnant(plateau, signe_adversaire)
    if coup:
        return coup

    # 3) Sinon prend le centre si possible
    if plateau[1][1] == " ":
        return (1, 1)

    # 4) Sinon prend un coin si possible
    coins = [(0, 0), (0, 2), (2, 0), (2, 2)]
    coins_libres = [coin for coin in coins if plateau[coin[0]][coin[1]] == " "]
    if coins_libres:
        return random.choice(coins_libres)

    # 5) Sinon joue au hasard
    return coup_ia_niveau1(plateau)


# =========================================================
#               VERSION CONSOLE (TEXTE)
# =========================================================

print("=== MORPION VERSION PYGAME + CONSOLE ===")
print("Tape 1 pour jouer en Pygame")
print("Tape 2 pour jouer en Console")

choix_mode_general = input("Ton choix : ")

if choix_mode_general == "2":
    # Choix du type de partie en console
    choix_mode_console = ""
    while choix_mode_console not in ["1", "2", "3", "4"]:
        print("Choisis le mode de jeu :")
        print("1 - Joueur vs Joueur (1v1)")
        print("2 - IA niveau 1")
        print("3 - IA niveau 2")
        print("4 - IA niveau 3")
        choix_mode_console = input("Choix : ")

    # Si ce n'est pas 1, on joue contre l'ordinateur
    contre_ordinateur = (choix_mode_console != "1")
    niveau_ia_console = int(choix_mode_console) - 1 if contre_ordinateur else 0

    plateau_console = creer_plateau()
    joueur_actuel_console = "X"

    # Boucle principale du jeu en console
    while True:
        afficher_plateau(plateau_console)
        print("Tour :", joueur_actuel_console)

        # Tour de l'IA si on joue contre elle et que c'est O
        if contre_ordinateur and joueur_actuel_console == "O":
            if niveau_ia_console == 1:
                ligne_console, colonne_console = coup_ia_niveau1(plateau_console)
            if niveau_ia_console == 2:
                ligne_console, colonne_console = coup_ia_niveau2(plateau_console, "O", "X")
            if niveau_ia_console == 3:
                ligne_console, colonne_console = coup_ia_niveau3(plateau_console, "O", "X")
        else:
            # Tour d'un joueur humain
            ligne_console, colonne_console = demander_coup(plateau_console)

        plateau_console[ligne_console][colonne_console] = joueur_actuel_console

        # Vérification de la victoire
        if a_gagne(plateau_console, joueur_actuel_console):
            afficher_plateau(plateau_console)
            print(joueur_actuel_console, "a gagné !")
            break

        # Vérification du match nul
        if plateau_plein(plateau_console):
            afficher_plateau(plateau_console)
            print("Match nul !")
            break

        # Changement de joueur
        joueur_actuel_console = "O" if joueur_actuel_console == "X" else "X"

    quit()


# =========================================================
#     FONCTION POUR TROUVER LA LIGNE GAGNANTE (PYGAME)
# =========================================================

def trouver_ligne_gagnante(plateau, joueur):
    """
    Retourne les deux cases extrêmes de l'alignement gagnant
    sous forme de deux coordonnées ((ligne1, col1), (ligne2, col2)).
    Sert pour tracer le trait sur l'interface graphique.
    """
    # Lignes
    for indice_ligne in range(3):
        if plateau[indice_ligne][0] == joueur and plateau[indice_ligne][1] == joueur and plateau[indice_ligne][2] == joueur:
            return (indice_ligne, 0), (indice_ligne, 2)
    # Colonnes
    for indice_colonne in range(3):
        if plateau[0][indice_colonne] == joueur and plateau[1][indice_colonne] == joueur and plateau[2][indice_colonne] == joueur:
            return (0, indice_colonne), (2, indice_colonne)
    # Diagonale principale
    if plateau[0][0] == joueur and plateau[1][1] == joueur and plateau[2][2] == joueur:
        return (0, 0), (2, 2)
    # Diagonale secondaire
    if plateau[0][2] == joueur and plateau[1][1] == joueur and plateau[2][0] == joueur:
        return (0, 2), (2, 0)
    return None


# =========================================================
#                     VERSION PYGAME (GRAPHIQUE)
# =========================================================

# --- Initialisation de Pygame et paramètres de la fenêtre ---
pygame.init()
LARGEUR_FENETRE = 600
HAUTEUR_FENETRE = 600
TAILLE_CASE = LARGEUR_FENETRE // 3  # chaque case du morpion

# Couleurs en RGB
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
ROUGE = (255, 0, 0)

# Création de la fenêtre et des polices de texte
ecran = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Morpion Pygame")
police_jeu = pygame.font.SysFont(None, 120)     # pour les X et O
police_menu = pygame.font.SysFont(None, 40)     # pour le menu
police_info = pygame.font.SysFont(None, 32)     # pour les messages en bas

# Horloge pour limiter les FPS
horloge = pygame.time.Clock()

# --------------------
# MENU GRAPHIQUE DE DÉPART
# --------------------

# Boutons (rectangles) pour choisir le mode de jeu
bouton_joueur_vs_joueur = pygame.Rect(150, 150, 300, 60)   # 1v1
bouton_ia_niveau1 = pygame.Rect(150, 250, 300, 60)         # IA 1
bouton_ia_niveau2 = pygame.Rect(150, 350, 300, 60)         # IA 2
bouton_ia_niveau3 = pygame.Rect(150, 450, 300, 60)         # IA 3

niveau_ia_pygame = 1
dans_menu = True
contre_ia = True  # True = contre IA, False = 1v1 local

# Boucle d'affichage du menu
while dans_menu:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            quit()
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            position_souris_x, position_souris_y = evenement.pos

            # Choix du mode 1v1
            if bouton_joueur_vs_joueur.collidepoint(position_souris_x, position_souris_y):
                contre_ia = False
                dans_menu = False

            # Choix IA niveau 1
            if bouton_ia_niveau1.collidepoint(position_souris_x, position_souris_y):
                niveau_ia_pygame = 1
                contre_ia = True
                dans_menu = False

            # Choix IA niveau 2
            if bouton_ia_niveau2.collidepoint(position_souris_x, position_souris_y):
                niveau_ia_pygame = 2
                contre_ia = True
                dans_menu = False

            # Choix IA niveau 3
            if bouton_ia_niveau3.collidepoint(position_souris_x, position_souris_y):
                niveau_ia_pygame = 3
                contre_ia = True
                dans_menu = False

    # Fond blanc
    ecran.fill(BLANC)

    # Dessin des boutons du menu
    pygame.draw.rect(ecran, GRIS, bouton_joueur_vs_joueur)
    pygame.draw.rect(ecran, GRIS, bouton_ia_niveau1)
    pygame.draw.rect(ecran, GRIS, bouton_ia_niveau2)
    pygame.draw.rect(ecran, GRIS, bouton_ia_niveau3)

    # Texte sur les boutons
    ecran.blit(police_menu.render("1v1 Joueur vs Joueur", True, NOIR), bouton_joueur_vs_joueur.move(20, 10))
    ecran.blit(police_menu.render("IA niveau 1", True, NOIR), bouton_ia_niveau1.move(70, 10))
    ecran.blit(police_menu.render("IA niveau 2", True, NOIR), bouton_ia_niveau2.move(70, 10))
    ecran.blit(police_menu.render("IA niveau 3", True, NOIR), bouton_ia_niveau3.move(70, 10))

    # Mise à jour de l'affichage
    pygame.display.update()


# --------------------
# BOUCLE PRINCIPALE DU JEU EN PYGAME
# --------------------

plateau_pygame = creer_plateau()      # plateau graphique
joueur_actuel_pygame = "X"            # X commence
partie_terminee = False               # True si victoire ou match nul
message_fin = ""                      # message à afficher en bas ("Tu as gagné !", etc.)
ligne_gagnante = None                 # coordonnées pour tracer le trait de victoire

while True:
    horloge.tick(30)  # limite à ~30 FPS

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Clic de souris pendant la partie (si elle n'est pas finie)
        if evenement.type == pygame.MOUSEBUTTONDOWN and not partie_terminee:
            position_souris_x, position_souris_y = evenement.pos

            # Conversion coordonnées pixel -> indices de case
            colonne_case = position_souris_x // TAILLE_CASE
            ligne_case = position_souris_y // TAILLE_CASE

            # On ne joue que si la case est vide
            if plateau_pygame[ligne_case][colonne_case] == " ":
                if contre_ia:
                    # Mode contre IA : le joueur humain joue X
                    if joueur_actuel_pygame == "X":
                        plateau_pygame[ligne_case][colonne_case] = "X"

                        # Vérifier si le joueur X gagne
                        if a_gagne(plateau_pygame, "X"):
                            partie_terminee = True
                            ligne_gagnante = trouver_ligne_gagnante(plateau_pygame, "X")
                            message_fin = "Tu as gagné !"  # message quand le joueur humain gagne
                        elif plateau_plein(plateau_pygame):
                            partie_terminee = True
                            message_fin = "Match nul."
                        else:
                            # Passage au tour de l'IA
                            joueur_actuel_pygame = "O"
                else:
                    # Mode 1v1 : les deux joueurs jouent à la souris
                    plateau_pygame[ligne_case][colonne_case] = joueur_actuel_pygame

                    if a_gagne(plateau_pygame, joueur_actuel_pygame):
                        partie_terminee = True
                        ligne_gagnante = trouver_ligne_gagnante(plateau_pygame, joueur_actuel_pygame)
                        message_fin = f"Le joueur {joueur_actuel_pygame} a gagné !"
                    elif plateau_plein(plateau_pygame):
                        partie_terminee = True
                        message_fin = "Match nul."
                    else:
                        # On alterne X → O → X ...
                        joueur_actuel_pygame = "O" if joueur_actuel_pygame == "X" else "X"

    # Tour de l'IA si on est en mode IA et que c'est à elle de jouer
    if contre_ia and joueur_actuel_pygame == "O" and not partie_terminee:
        pygame.time.delay(300)  # petite pause pour voir le coup

        # Choix du coup en fonction du niveau
        if niveau_ia_pygame == 1:
            ligne_ia, colonne_ia = coup_ia_niveau1(plateau_pygame)
        if niveau_ia_pygame == 2:
            ligne_ia, colonne_ia = coup_ia_niveau2(plateau_pygame, "O", "X")
        if niveau_ia_pygame == 3:
            ligne_ia, colonne_ia = coup_ia_niveau3(plateau_pygame, "O", "X")

        plateau_pygame[ligne_ia][colonne_ia] = "O"

        # Vérification si l'IA gagne
        if a_gagne(plateau_pygame, "O"):
            partie_terminee = True
            ligne_gagnante = trouver_ligne_gagnante(plateau_pygame, "O")
            message_fin = "L'IA a gagné."
        elif plateau_plein(plateau_pygame):
            partie_terminee = True
            message_fin = "Match nul."
        else:
            joueur_actuel_pygame = "X"  # retour au joueur humain

    # --------------------
    # DESSIN GRAPHIQUE
    # --------------------

    # Fond blanc
    ecran.fill(BLANC)

    # Dessin de la grille (2 lignes verticales, 2 horizontales)
    pygame.draw.line(ecran, NOIR, (TAILLE_CASE, 0), (TAILLE_CASE, HAUTEUR_FENETRE), 3)
    pygame.draw.line(ecran, NOIR, (TAILLE_CASE * 2, 0), (TAILLE_CASE * 2, HAUTEUR_FENETRE), 3)
    pygame.draw.line(ecran, NOIR, (0, TAILLE_CASE), (LARGEUR_FENETRE, TAILLE_CASE), 3)
    pygame.draw.line(ecran, NOIR, (0, TAILLE_CASE * 2), (LARGEUR_FENETRE, TAILLE_CASE * 2), 3)

    # Dessin des X et O sur le plateau
    for indice_ligne in range(3):
        for indice_colonne in range(3):
            symbole = plateau_pygame[indice_ligne][indice_colonne]
            if symbole != " ":
                image_symbole = police_jeu.render(symbole, True, NOIR)
                # Positionner le symbole au milieu de la case
                position_x = indice_colonne * TAILLE_CASE + 60
                position_y = indice_ligne * TAILLE_CASE + 20
                ecran.blit(image_symbole, (position_x, position_y))

    # Si quelqu'un a gagné, on trace un trait rouge sur l'alignement
    if ligne_gagnante is not None:
        (ligne1, colonne1), (ligne2, colonne2) = ligne_gagnante
        x1 = colonne1 * TAILLE_CASE + TAILLE_CASE // 2
        y1 = ligne1 * TAILLE_CASE + TAILLE_CASE // 2
        x2 = colonne2 * TAILLE_CASE + TAILLE_CASE // 2
        y2 = ligne2 * TAILLE_CASE + TAILLE_CASE // 2
        pygame.draw.line(ecran, ROUGE, (x1, y1), (x2, y2), 8)

    # Affichage du message de fin s'il existe
    if message_fin != "":
        texte_info = police_info.render(message_fin, True, NOIR)
        ecran.blit(texte_info, (20, HAUTEUR_FENETRE - 30))

    # Mise à jour de l'écran
    pygame.display.update()
