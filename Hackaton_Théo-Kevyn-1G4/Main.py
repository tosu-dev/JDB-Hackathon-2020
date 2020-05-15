from tkinter import *
from random import *
from rsrc.Class.Card import Card

# _____VAR_____
listQstAns = [] # liste qui va contenir toutes les listes

# listes correspondant aux difficultés (1=trop facile, 2=je savais, 3=je ne savais pas)
dif1 = []
dif2 = []
dif3 = []

# _____LIST QUESTION/REPONSE_____
with open("rsrc/question_reponse.txt", "r+", encoding="utf8") as file:
    listTotal = file.readlines() # liste [question, réponse, question, ...]
    i = 0
    while i < len(listTotal):
        l = [listTotal[i], listTotal[i+1], 0] # liste [question, réponse, difficulté]
        listQstAns.append(l) # on ajoute cette liste dans la liste principal
        i += 2 # on avance de deux lignes (question/réponse)
    file.close()
    # listQstAns contient chaques liste contenant la question, sa réponse et sa difficulté (0 par défaut)

shuffle(listQstAns) # on mélange cette liste
# on instancie un  première fois notre carte avec la premiere question et sa réponse
card = Card(listQstAns[0][0], listQstAns[0][1])

# _____VAR_____
numQuestion = 0 # numéro de la question
maxQuestion = len(listQstAns) # question maxi
numSerie = 1 # numéro de la série

# _____FUNCTIONS_____
def enableButtons():
    # Désactive le bouton "retourner le carte" et active les 3 autres boutons
    turnCardButton.configure(state=DISABLED, cursor="X_cursor")
    button1.configure(state=NORMAL, cursor="hand2")
    button2.configure(state=NORMAL, cursor="hand2")
    button3.configure(state=NORMAL, cursor="hand2")

def disabledButtons():
    # Active le bouton "retourner le carte" et déscative les 3 autres boutons
    turnCardButton.configure(state=NORMAL, cursor="hand2")
    button1.configure(state=DISABLED, cursor="X_cursor")
    button2.configure(state=DISABLED, cursor="X_cursor")
    button3.configure(state=DISABLED, cursor="X_cursor")

def shuffleLists():
    # Mélange les listes de difficultés
    shuffle(dif1)
    shuffle(dif2)
    shuffle(dif3)

def reset():
    # quand c'est la derniere question et qu'on passe à la série suivante

    global numSerie
    global numQuestion

    numQuestion = 0  # on réinitialise le numéro de la question
    numSerie += 1 # on passe à la prochaine série
    numQuestionLabel.configure(text="{}/{}".format(numQuestion + 1, maxQuestion))
    numSerieLabel.configure(text="Série n°{}".format(numSerie))
    disabledButtons()

def proba():
    # 60% pour une question "je ne savais pas" (3)
    # 30% pour une question "je savais" (2)
    # 10% pour une question "trop facile" (1)
    r =  randint(1, 10)
    if r >= 1 and r <= 6:
        return 3
    elif r >=7 and r <= 9:
        return 2
    elif r == 10:
        return 1

def chance():
    # selon ce que proba() va retourner, on va piocher une liste dans la bonne difficulté
    # si elle est vide, on recommence jusqu'à qu'on pioche une question

    global card

    del card # on suppr la carte courante pour la redéfinir
    pickedQuestion = False # bool pour savoir si une question a bien été piocher

    while pickedQuestion == False: # tant qu'aucune question n'est prise

        chance = proba()

        if chance == 3 and len(dif3) != 0: # si la chance tombe sur 3 et que la liste correspondante n'est pas vide
            pickedQuestion = True # on peut bien prendre une question
            card = Card(dif3[0][0], dif3[0][1], dif3[0][-1]) # on créer un nouvelle carte avec la prochaine question, sa réponse et sa difficulté
            cardLabel.configure(text="Question :\n\n{}".format(card.getQuestion()), fg="red") # on affiche la question en rouge
            del dif3[0] # et on peut supprimer cette liste de sa difficulté (elle est stocké avec sa nouvelle difficulté dans listQstAns)

        elif chance == 2 and len(dif2) != 0: # pareil pour 2
            pickedQuestion = True
            card = Card(dif2[0][0], dif2[0][1], dif2[0][-1])
            cardLabel.configure(text="Question :\n\n{}".format(card.getQuestion()), fg="orange")
            del dif2[0]

        elif chance == 1 and len(dif1) != 0: # pareil pour 3
            pickedQuestion = True
            card = Card(dif1[0][0], dif1[0][1], dif1[0][-1])
            cardLabel.configure(text="Question :\n\n{}".format(card.getQuestion()), fg="green")
            del dif1[0]

        else: # si la liste est vide, on recommence
            continue

def verifKnowledge():
    # vérifie si toutes les questoins sont "trop facile"
    # on vérifie à la fin d'une série

    # si oui
    if len(dif2) + len(dif3) == 0:
        cardLabel.configure(text="VOUS SAVEZ TOUT !", fg="green")
        numQuestionLabel.configure(text="")
        numSerieLabel.configure(text="")
        turnCardButton.configure(state=DISABLED, cursor="X_cursor")
    # si non, on continue (on fait la première carte de la nouvelle série)
    else:
        chance()

def setNewCard():
    global card
    global numQuestion
    global maxQuestion
    global numSerie
    global chance
    global pickedQuestion
    global dif1
    global dif2
    global dif3
    global cardLabel

    numQuestion += 1 # prochaine question

    # si c'est la 1er série (difficultés pas défini donc = 0)
    # les listes sont stockées dans la liste principal (listQstAns)
    if numSerie == 1:

        del listQstAns[0] # on suppr la liste (elle est stockée dans sa liste de difficulté)

        # si ce n'est pas la dernière question...
        if numQuestion != maxQuestion:
            # ...on redifinit la nouvelle carte et on switch les boutons
            del card
            card = Card(listQstAns[0][0], listQstAns[0][1])
            cardLabel.configure(text="Question :\n\n{}".format(card.getQuestion()), fg="white")
            numQuestionLabel.configure(text="{}/{}".format(numQuestion + 1, maxQuestion))
            disabledButtons()

        # sinon si c'est la dernière question...
        else:
            reset() # on réinitialise

            shuffleLists() # on mélange les liste
            verifKnowledge() # et on vérifie s'il sait tout
            # et si il ne sait pas tout, on rédéfini la prochaine carte de la 1ere série

    # sinon si une prochaine série (les difficultés sont définis)
    # les listes sont stockées dans les difficultés
    elif numSerie > 1:

        # si ce n'est pas la derniere question
        if numQuestion != maxQuestion:
            numQuestionLabel.configure(text="{}/{}".format(numQuestion + 1, maxQuestion))
            disabledButtons()
            chance() # on tire une carte au hasard en supprimant cette liste de sa difficulté
            # elle est stockée dans la liste principale

        # sinon si c'est la derniere question
        else:
            reset() # on réinitialise

            # les listes de difficultés sont vides et la liste principal est pleine
            # on va donc redistribuer les listes dans leurs bonnes difficultés
            for elt in listQstAns:
                if elt[-1] == 1:
                    dif1.append(elt)
                elif elt[-1] == 2:
                    dif2.append(elt)
                elif elt[-1] == 3:
                    dif3.append(elt)

            listQstAns.clear() # on suppr tous les éléments de la liste principal
            # car les listes de difficultés les possèdent déhç
            shuffleLists() # on mélange
            verifKnowledge()  # et on vérifie s'il sait tout
            # et si il ne sait pas tout, on rédéfini la prochaine carte de la 1ere série

def turnCard():
    # tourne la carte en affichant la réponse et change le mode des boutons
    cardLabel.configure(text="Réponse :\n\n{}".format(card.getAnswer()))
    enableButtons()

def diff1():
    # Change la difficulté
    card.setDifficulty(1)
    # on enregistre dans une liste, la question, sa réponse et sa nouvelle difficulté et...
    l = [card.getQuestion(), card.getAnswer(), card.getDifficulty()]

    # ...si c'est la 1er série, on l'a met directement dans sa liste de difficulté
    if numSerie == 1:
        dif1.append(l)
    # ...sinon, on le met dans la liste principal
    elif numSerie > 1:
        listQstAns.append(l)

    # puis on fait une nouvelle carte
    setNewCard()

def diff2():
    # Pareil avec la difficulté 2
    card.setDifficulty(2)
    l = [card.getQuestion(), card.getAnswer(), card.getDifficulty()]

    if numSerie == 1:
        dif2.append(l)
    elif numSerie > 1:
        listQstAns.append(l)

    setNewCard()

def diff3():
    # Pareil avec la difficulté 3
    card.setDifficulty(3)
    l = [card.getQuestion(), card.getAnswer(), card.getDifficulty()]

    if numSerie == 1:
        dif3.append(l)
    elif numSerie > 1:
        listQstAns.append(l)

    setNewCard()



# _____MAIN WINDOW_____
# Backgrounds colors
bg = "#b192eb"
bg2 = "#a684e7"

window = Tk()
window.title("Hackaton")
window.geometry("1080x720")
window.minsize(1080, 720)
window.maxsize(1080, 720)
window.config(background=bg)
window.iconbitmap("rsrc/logo.ico")

# _____MAIN FRAMES_____
leftFrame = Frame(window, bg=bg)
rightFrame = Frame(window, bg=bg)

# _____IN LEFT FRAME_____
cardLabel = Label(leftFrame, text="Question :\n\n{}".format(card.getQuestion()), font=("Courrier", 26), bg=bg, fg="white",
                  bd=4, relief=SOLID, height=12, width=25, wraplength=450)
cardLabel.pack()

turnCardButton = Button(leftFrame, text="Retourner la carte", font=("Courrier", 26), bg=bg2,
                        fg="white", command=turnCard, cursor="hand2")
turnCardButton.pack(pady=55)

# _____IN RIGHT FRAME_____
numQuestionLabel = Label(rightFrame, text="1/{}".format(maxQuestion), font=("Courrier", 20), bg=bg, fg="white")
numQuestionLabel.pack(pady=0, padx=60)

numSerieLabel = Label(rightFrame, text="Série n°1", font=("Courrier", 20), bg=bg, fg="white")
numSerieLabel.pack(pady=0, padx=60)

button1 = Button(rightFrame, text="Trop facile", font=("Courrier", 20), bg=bg2, fg="green", width=20,
                 state=DISABLED, command=diff1, cursor="X_cursor")
button1.pack(pady=20, padx=60)

button2 = Button(rightFrame, text="Je savais", font=("Courrier", 20), bg=bg2, fg="orange", width=20,
                 state=DISABLED, command=diff2, cursor="X_cursor")
button2.pack(pady=20, padx=60)

button3 = Button(rightFrame, text="Je ne savais pas", font=("Courrier", 20), bg=bg2, fg="red", width=20,
                 state=DISABLED, command=diff3, cursor="X_cursor")
button3.pack(pady=20, padx=60)

# _____DISPLAY_____
leftFrame.grid(row=0, column=0, padx=50, pady=50)
rightFrame.grid(row=0, column=1)
window.mainloop()
