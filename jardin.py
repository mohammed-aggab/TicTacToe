def creer_jardin():
    jardin = [
        [".", ".", "."],[".", ".", "."],[".", ".", "."]
    ]
    return jardin

def afficher_jardin(jardin):
    print("---------")
    for element in jardin:
        print("|", element[0], element[1], element[2], "|")
    print("---------")

def position_jardin(jardin):
    for i in range(5):

        ligne = input("Choisis une ligne (0, 1 ou 2) : ")
        colonne = input("Choisis une colonne (0, 1 ou 2) : ")


        ligne = int(ligne)
        colonne = int(colonne)

        choix = input("Écris G : ")

        if jardin[ligne][colonne] == ".":
            jardin[ligne][colonne] = choix
        else:
            print("La case est déjà remplie, choisis une case vide")



        afficher_jardin(jardin)

    return jardin

j_ardin = creer_jardin()
afficher_jardin(j_ardin)
print(position_jardin(j_ardin))
