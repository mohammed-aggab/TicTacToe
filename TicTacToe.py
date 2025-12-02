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


