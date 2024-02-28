from Game import Game


print("---Wellcome to TAC---")
toDo = input("Start new game?")
while toDo == "yes" or toDo == "y":
    playerNames = []

    game = Game()
    game.start()

    toDo = input("Start new game?")