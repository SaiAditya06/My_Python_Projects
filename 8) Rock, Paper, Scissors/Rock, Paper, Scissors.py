import random

com_points = 0
play_points = 0

while play_points < 10 and com_points < 10:
    com = random.choice(["Rock", "Paper", "Scissors"])
    play = input("Choose between Rock, Paper, Scissors: ")

    if play.upper().strip()[0] == com.upper().strip()[0]:
        print("Tie - Both of you choose", play)
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points >= 10:
            print("Computer Won :( Try Again!!")
        elif play_points >= 10:
            print("You Won :) Congratulations!!")

    elif play.upper()[0] == "P" and com.upper() == "ROCK":
        play_points += 1
        print("Computer choose", com)
        print("You Won :) +1 point")
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points >= 10:
            print("Computer Won :( Try Again!!")
        elif play_points >= 10:
            print("You Won :) Congratulations!!")

    elif play.upper()[0] == "R" and com.upper() == "SCISSORS":
        play_points += 1
        print("Computer choose", com)
        print("You Won :) +1 point")
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points >= 10:
            print("Computer Won :( Try Again!!")
        elif play_points >= 10:
            print("You Won :) Congratulations!!")

    elif play.upper()[0] == "S" and com.upper() == "PAPER":
        play_points += 1
        print("Computer choose", com)
        print("You Won :) +1 point")
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points >= 10:
            print("Computer Won :( Try Again!!")
        elif play_points >= 10:
            print("You Won :) Congratulations!!")
#
    elif com.upper() == "PAPER" and play.upper()[0] == "R":
        com_points += 1
        print("Computer choose", com)
        print("You Lost :( +1 to computer")
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points >= 10:
            print("Computer Won :( Try Again!!")
        elif play_points >= 10:
            print("You Won :) Congratulations!!")

    elif com.upper() == "ROCK" and play.upper()[0] == "S":
        com_points += 1
        print("Computer choose", com)
        print("You Lost :( +1 to computer")
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points >= 10:
            print("Computer Won :( Try Again!!")
        elif play_points >= 10:
            print("You Won :) Congratulations!!")

    elif com.upper() == "SCISSORS" and play.upper()[0] == "P":
        com_points += 1
        print("Computer choose",com)
        print("You Lost :( +1 to computer")
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points >= 10:
            print("Computer Won :( Try Again!!")
        elif play_points >= 10:
            print("You Won :) Congratulations!!")

    else:
        print("The value is incorrect")
        print("Computer points:", com_points, "You're points:", play_points)
        if com_points == 10:
            print("Computer Won :( Try Again!!")
        elif play_points == 10:
            print("You Won :) Congratulations!!")