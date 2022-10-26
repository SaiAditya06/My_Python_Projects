import random
import time

print("Welcome to Tic Tac Toe\n")


def board_board(x):
    print(100 * "\n")
    print("-------------------")
    print("|  " + x[1] + "  |  " + x[2] + "  |  " + x[3] + "  |")
    print("-------------------")
    print("|  " + x[4] + "  |  " + x[5] + "  |  " + x[6] + "  |")
    print("-------------------")
    print("|  " + x[7] + "  |  " + x[8] + "  |  " + x[9] + "  |")
    print("-------------------")


data = test_board = ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ']


def token():
    player_token = None
    computer_token = None

    switch = True
    while switch:
        player_token = input("Do you want X or O: ")
        computer_token = None
        if player_token.upper() == "X":
            player_token = "X"
            computer_token = "O"
            print("You Choose",player_token)
            print("Computer Choose",computer_token)
            time.sleep(2)
            switch = False
        elif player_token.upper() == "O":
            player_token = "O"
            computer_token = "X"
            time.sleep(2)
            print("You Choose",player_token)
            print("Computer Choose",computer_token)
            switch = False
        else:
            print("Sorry You neither choose X or O")
            switch = True
    return {"player": player_token,"computer": computer_token}


tokens = token()
player = tokens.get("player")
computer = tokens.get("computer")


def win_check(board,mark):
    return ((board[1] == mark and board[2] == mark and board[3] == mark) or
            (board[4] == mark and board[5] == mark and board[6] == mark) or
            (board[7] == mark and board[8] == mark and board[9] == mark) or
            (board[1] == mark and board[4] == mark and board[7] == mark) or
            (board[2] == mark and board[5] == mark and board[8] == mark) or
            (board[3] == mark and board[6] == mark and board[9] == mark) or
            (board[1] == mark and board[5] == mark and board[9] == mark) or
            (board[3] == mark and board[5] == mark and board[7] == mark))


def full_board_win_check():
    win__check1 = win_check(data,player)
    win__check2 = win_check(data,computer)
    if win__check1:
        print("Congrats you have won the game")
        exit()
    elif win__check2:
        print("Better try next time")
        exit()


def space_check(board,position):
    return board[position] == ' '


def full_board_check(board):
    for i in range(1,10):
        if space_check(board,i):
            return False
    return True


def player_prompt():
    print("[1,2,3]")
    print("[4,5,6]")
    print("[7,8,9]")
    while True:
        try:
            ask1 = int(input("where do you want to place " + player + " (above is the layout): "))
        except:
            print("sorry that not a number please enter a digit")
        else:
            if data[ask1] == ' ':
                data[ask1] = player
                break
            else:
                print("sorry the space in occupied")


def computer_prompt():
    while True:
        choose = random.randint(1,9)
        if data[choose] == ' ':
            data[choose] = computer
            break
        else:
            pass


def game():
    while True:
        x = full_board_check(data)
        if not x:
            if player == "X":
                board_board(data)
                full_board_win_check()
                time.sleep(2)
                player_prompt()
                board_board(data)
                full_board_win_check()
                print("Computer is choosing")
                time.sleep(2)
                computer_prompt()
                board_board(data)
                full_board_win_check()
            elif player == "O":
                board_board(data)
                full_board_win_check()
                print("Computer is choosing")
                time.sleep(2)
                computer_prompt()
                board_board(data)
                full_board_win_check()
                time.sleep(2)
                player_prompt()
                board_board(data)
                full_board_win_check()
            else:
                pass
        elif x:
            print("It's a Tie")
            exit()
        else:
            pass


game()
