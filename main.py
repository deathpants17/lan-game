import random
import tkinter
import socket
from tkinter import *
from tkinter import Tk
from PIL import ImageTk, Image

screen_width = None
screen_height = None

import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
playerTurn = None
player1Name = 'joining'
player2Name = 'joining'
player1Label = None
player2Label = None

player1Score = 0
player2Score = 0
player2ScoreLabel = None
player2ScoreLabel = None

dice = None

rollButton = None
resetButton = None

winingMessage = None

winingFunctionCall = 0


def check(boxes,color):
    for i in boxes:
        box_color = i.cget('bg')
        if box_color == color: 
            return boxes.index(i)
    return False


def movePlayer1(steps):
    global leftBoxes

    boxPosition = check(leftBoxes[1:],"red")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(steps == remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            global finishingBox

            finishingBox.configure(bg='red')

            global SERVER
            global playerName

            greetMessage = f'Red wins the game.'
            SERVER.send(greetMessage.encode())

        elif(steps < remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            leftBoxes[nextStep].configure(bg='red')
        else:
            print("Move False")
    else:
        # first step
        leftBoxes[steps].configure(bg='red')    

def movePlayer2(steps):
    global rightBoxes

    # Moving to reverse order
    tempBoxes = rightBoxes[-2::-1]

    boxPosition = check(tempBoxes,"yellow")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(diceValue == remainingSteps):
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')

            global finishingBox

            finishingBox.configure(bg='yellow', fg="black")

            global SERVER
            global playerName

            greetMessage = f'Yellow wins the game.'
            SERVER.send(greetMessage.encode())

        elif(diceValue < remainingSteps):
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            rightBoxes[::-1][nextStep].configure(bg='yellow')
        else:
            print("Move False")
    else:
        # first step
        rightBoxes[len(rightBoxes) - (steps+1)].configure(bg='yellow')


def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xPos = 30
    for box in range(0, 11):
        if (box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica", 10), width=2, height=1, relief='ridge', borderwidth=0,
                             bg="red")
            boxLabel.place(x=xPos, y=screen_height / 2 - 88)
            leftBoxes.append(boxLabel)
            xPos += 50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica", 15), width=2, height=1, relief='ridge', borderwidth=0,
                             bg="white")
            boxLabel.place(x=xPos, y=screen_height / 2 - 100)
            leftBoxes.append(boxLabel)
            xPos += 80


def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xPos = 988
    for box in range(0, 11):
        if (box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica", 10), width=2, height=1, relief='ridge', borderwidth=0,
                             bg="yellow")
            boxLabel.place(x=xPos, y=screen_height / 2 - 88)
            rightBoxes.append(boxLabel)
            xPos += 50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica", 15), width=2, height=1, relief='ridge', borderwidth=0,
                             bg="white")
            boxLabel.place(x=xPos, y=screen_height / 2 - 100)
            rightBoxes.append(boxLabel)
            xPos += 80


def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0,
                         bg="green", fg="white")
    finishingBox.place(x=screen_width / 2 - 68, y=screen_height / 2 - 160)


def gameWindow():
        global gameWindow
        global canvas2
        global screen_width
        global screen_height
        global dice
        global rollButton
        global face
        global playerTurn
        global playerType
        global playerName
        # Additional Activity
        global player1Name
        global player2Name
        global player1Label
        global player2Label
        global player1Score
        global player2Score
        global player1ScoreLabel
        global player2ScoreLabel

        gameWindow = Toplevel()
        gameWindow.title("Ludo Ladder")
        gameWindow.attributes('-fullscreen', True)

        screen_width = gameWindow.winfo_screenwidth()
        screen_height = gameWindow.winfo_screenheight()
        gameWindow= Toplevel()

        bg= ImageTk.PhotoImage(file="background.png")

        canvas2 = Canvas(gameWindow, width=500, height=500)
        canvas2.pack(fill="both", expand=True)

        canvas2.create_image(0, 0, image=bg, anchor="nw")
        canvas2.create_text(screen_width / 2, screen_height / 5, text="Ludo Ladder", font=("Chalkboard SE", 100),
                            fill="white")



        rollButton = Button(gameWindow, text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey", width=10,
                            height=2,command=diceRoll)
        rollButton.place(x=screen_width / 2 - 60, y=screen_height / 3 + 250)

        if (playerType == 'player1' and playerTurn):
            rollButton.place(x=screen_width / 2 - 60, y=screen_height / 3 + 250)
        else:
            rollButton.pack_forget()

        # Creating Dice with value 1
        dice = canvas2.create_text(screen_width / 2 - 180, screen_height / 3 + 250, text=face,
                                   font=("Chalkboard SE", 100), fill="white")

        player1Label = canvas2.create_text(400, screen_height / 2 + 100, text=player1Name, font=("Chalkboard SE", 80),
                                           fill='#fff176')
        player2Label = canvas2.create_text(screen_width - 300, screen_height / 2 + 100, text=player2Name,
                                           font=("Chalkboard SE", 80), fill='#fff176')

        # Creating Score Board
        player1ScoreLabel = canvas2.create_text(400, screen_height / 2 - 160, text=player1Score,
                                                font=("Chalkboard SE", 80), fill='#fff176')
        player2ScoreLabel = canvas2.create_text(screen_width - 300, screen_height / 2 - 160, text=player2Score,
                                                font=("Chalkboard SE", 80), fill='#fff176')

        leftBoard()
        rightBoard()
        finishingBox()
        gameWindow.resizable(True, True)
        gameWindow.mainloop()


def diceRoll():
    global SERVER
    global face
    diceFace = ['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    face = random.choice(diceFace)

    global playerType
    global rollButton
    global playerTurn
    print(face)

    rollButton.destroy()
    playerTurn = False

    if (playerType == 'player1'):
        SERVER.send(f'{face}playerTurn'.encode())
    if (playerType == 'player2'):
        SERVER.send(f'{face}player2Turn'.encode())



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen', True)

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="background.png")

    canvas1 = Canvas(nameWindow, width=500, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=bg, anchor="nw")
    canvas1.create_text(screen_width / 2, screen_height / 5, text="Enter Name", font=("Chalkboard SE", 100),
                        fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x=screen_width / 2 - 220, y=screen_height / 4 + 100)

    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30), width=15,  height=2,command=gameWindow,
                    bg="#80deea", bd=3)
    button.place(x=screen_width / 2 - 130, y=screen_height / 2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


def recivedMsg():
    global SERVER
    global playerType
    global playerTurn
    global rollButton
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gameWindow
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global winingFunctionCall



    while True:
        message = SERVER.recv(2048).decode()

        if('player_type' in message):
            recvMsg = eval(message)
            playerType = recvMsg['player_type']
            playerTurn = recvMsg['turn']
        elif('player_names' in message):

            players = eval(message)
            players = players["player_names"]
            for p in players:
                if(p["type"] == 'player1'):
                    player1Name = p['name']
                if(p['type'] == 'player2'):
                    player2Name = p['name']

        elif('⚀' in message):
            # Dice with value 1
            canvas2.itemconfigure(dice, text='\u2680')
        elif('⚁' in message):
            # Dice with value 2
            canvas2.itemconfigure(dice, text='\u2681')
        elif('⚂' in message):
            # Dice with value 3
            canvas2.itemconfigure(dice, text='\u2682')
        elif('⚃' in message):
            # Dice with value 4
            canvas2.itemconfigure(dice, text='\u2683')
        elif('⚄' in message):
            # Dice with value 5
            canvas2.itemconfigure(dice, text='\u2684')
        elif('⚅' in message):
            # Dice with value 6
            canvas2.itemconfigure(dice, text='\u2685')
        #--------- Boilerplate Code Start--------
        elif('wins the game.' in message and winingFunctionCall == 0):
            winingFunctionCall +=1
            handleWin(message)
            # Addition Activity
            updateScore(message)
        elif(message == 'reset game'):
            handleResetGame()
        #--------- Boilerplate Code End--------


        #creating rollbutton
        if('player1Turn' in message and playerType == 'player1'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

        elif('player2Turn' in message and playerType == 'player2'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 260)


        # Student Activity
        # Deciding player turn
        if('player1Turn' in message or 'player2Turn' in message):
            diceChoices=['⚀','⚁','⚂','⚃','⚄','⚅']
            diceValue = diceChoices.index(message[0]) + 1

            if('player2Turn' in message):
                movePlayer1(diceValue)


            if('player1Turn' in message):
                movePlayer2(diceValue)

        # Additional Activity
        # Creating Name Board
        if(player1Name != 'joining' and canvas2):
            canvas2.itemconfigure(player1Label, text=player1Name)

        if(player2Name != 'joining' and canvas2):
            canvas2.itemconfigure(player2Label, text=player2Name)






def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))


    askPlayerName()


setup()
