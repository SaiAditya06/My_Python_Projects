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
    player1_token = None
    player2_token = None

    switch = True
    while switch:
        player1_token = input("Player1) Do you want X or O: ")
        player2_token = None
        if player1_token.upper() == "X":
            player1_token = "X"
            player2_token = "O"
            print("Player1 Choose",player1_token)
            print("Player2 Choose",player2_token)
            time.sleep(2)
            switch = False
        elif player1_token.upper() == "O":
            player1_token = "O"
            player2_token = "X"
            time.sleep(2)
            print("Player1 Choose",player1_token)
            print("Player2 Choose",player2_token)
            switch = False
        else:
            print("Sorry You neither choose X or O")
            switch = True
    return {"player1": player1_token,"player2": player2_token}


tokens = token()
player1 = tokens.get("player1")
player2 = tokens.get("player2")


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
    win__check1 = win_check(data,player1)
    win__check2 = win_check(data,player2)
    if win__check1:
        print("Congrats Player1 have won the game")
        exit()
    elif win__check2:
        print("Congrats Player2 have won the game")
        exit()


def space_check(board,position):
    return board[position] == ' '


def full_board_check(board):
    for i in range(1,10):
        if space_check(board,i):
            return False
    return True


def player1_prompt():
    print("[1,2,3]")
    print("[4,5,6]")
    print("[7,8,9]")
    while True:
        try:
            ask1 = int(input("Player1) Where do you want to place " + player1 + " (above is the layout): "))
        except:
            print("sorry that not a number please enter a digit")
        else:
            if data[ask1] == ' ':
                data[ask1] = player1
                break
            else:
                print("sorry the space in occupied")


def player2_prompt():
    print("[1,2,3]")
    print("[4,5,6]")
    print("[7,8,9]")
    while True:
        try:
            ask1 = int(input("Player2) Where do you want to place " + player2 + " (above is the layout): "))
        except:
            print("sorry that not a number please enter a digit")
        else:
            if data[ask1] == ' ':
                data[ask1] = player2
                break
            else:
                print("sorry the space in occupied")


def game():
    while True:
        x = full_board_check(data)
        if not x:
            if player1 == "X":
                board_board(data)
                full_board_win_check()
                time.sleep(2)
                player1_prompt()
                board_board(data)
                full_board_win_check()
                time.sleep(2)
                player2_prompt()
                board_board(data)
                full_board_win_check()
            elif player1 == "O":
                board_board(data)
                full_board_win_check()
                time.sleep(2)
                player2_prompt()
                board_board(data)
                full_board_win_check()
                time.sleep(2)
                player1_prompt()
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
