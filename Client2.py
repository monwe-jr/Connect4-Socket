import tkinter
import time
import socket
import numpy as np

client_two = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use IPV4, and stream (think TCP)
client_two.connect(("localhost", 2046))
print("Accepted client:" + str(client_two))



# disables buttons
def disable_buttons():
    for i in range(7):
        id = chr(ord('A') + i)
        button = top.children['b_' + id]
        button['state'] = tkinter.DISABLED


# enables buttons
def enable_buttons():
    for i in range(7):
        id = chr(ord('A') + i)
        button = top.children['b_' + id]
        button['state'] = tkinter.NORMAL





# gets the response of the other player******
def send(selection):
    global game_over
    global client_two

    if is_valid_location(board, selection):
        id = chr(ord('A') + selection)
        top.setvar("extra","you selected column:" + id)
        row = get_next_open_row(board, selection)
        drop_piece(board, row, selection, player_two)
        rec_data = flip_board(board)
        top.setvar('msg', rec_data)
        disable_buttons()
        if winning_move(board, player_two):
            disable_buttons()
            top.setvar("extra","Player two wins!")
            time.sleep(3)
            game_over = True

    else:
        top.setvar("extra", "You picked an invalid column.")
        pass

    s = str(selection)  # input the board
    client_two.sendall(s.encode())
    r = int(client_two.recv(1024).decode())

    if is_valid_location(board, r):
        id = chr(ord('A') + r)
        top.setvar("extra", "Player one selected column:" + id)
        row = get_next_open_row(board, r)
        drop_piece(board, row, r, player_one)
        rec_data = flip_board(board)
        top.setvar('msg', rec_data)
        enable_buttons()
        if winning_move(board, player_one):
            disable_buttons()
            top.setvar("extra","Player one wins!")
            time.sleep(3)
            game_over = True

    else:
        top.setvar("extra", "Player one picked an invalid column.")
        pass




# closure function
def shooper(i):
    def shoop():
        send(i)

    return shoop


# creates the grid represented by a matrix
def create_board():
    board = np.zeros((6, 7))
    return board


# drops the piece in the specified location
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# checks if the olumn is full
def is_valid_location(board, col):
    if board[5][col] == 0:
        return True

def get_next_open_row(board, col):
    for r in range(row_count):
        if board[r][col] == 0:
            return r


# flips the board to it's correct orientation
def flip_board(board):
    return np.flip(board, 0)


# checks for a win with recent drop
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(column_count - 3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(column_count - 3):
        for r in range(row_count):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

        # Check positive diagonal locations for win
        for c in range(column_count - 3):
            for r in range(row_count - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negative diagonal locations for win
        for c in range(column_count - 3):
            for r in range(3, row_count):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True


board = create_board()
game_over = False
row_count = 6
column_count = 7
player_one = 1
player_two = 2


# generates the tkinter window with all the buttons
# crwates closer with selections using shooper
def gen_window():
    win = tkinter.Tk()
    s = tkinter.StringVar(win, name="msg")
    t = tkinter.StringVar(win,name="extra")
    text = tkinter.Label(win, width=34, height=17, font="courier", bg="white", textvariable=t)
    text.grid(column=0,row = 3, columnspan = 7)
    lbl = tkinter.Label(win, width=34, height=17, font="courier", bg="white", textvariable=s)
    lbl.grid(column=0, row=0, columnspan=7)

    for i in range(7):
        id = chr(ord('A') + i)
        b = tkinter.Button(win, text=id, name="b_" + id, fg="blue", width="7", command=shooper(i))
        b.grid(column=i, row=1)
    win.setvar("msg", board)


    return win


top = gen_window()
while game_over != True:
    top.mainloop()
