import tkinter 
import socket
import time
import numpy as np

class Client:
    global game_over
    global row_count
    global column_count 
    global board
    global client
    global Symbol
    global OppSymbol
    global top
    global Name
    row_count = 6
    column_count = 7

    def __init__(self, state, symbol, oppSymbol):
        self.game_over = state
        self.Symbol = symbol
        self.OppSymbol = oppSymbol
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use IPV4
        self.client.connect(("localhost", 2046))
        self.board = self.create_board()
        self.top = self.gen_window()
        while not self.game_over:
            self.top.mainloop()


    # disables buttons
    def disable_buttons(self):
        for i in range(7):
            id = chr(ord('A') + i)
            button = self.top.children['b_' + id]
            button['state'] = tkinter.DISABLED


    # enables buttons
    def enable_buttons(self):
        for i in range(7):
            id = chr(ord('A') + i)
            button = self.top.children['b_' + id]
            button['state'] = tkinter.NORMAL


    # closure function
    def shooper(self, i):
        def shoop():
            self.send(i)
        return shoop


    # creates the grid represented by a matrix
    def create_board(self):
        self.board = np.zeros((6, 7))
        return self.board


    # drops the piece in the specified location
    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece


    # checks if the column is full
    def is_valid_location(self, board, col):
        if board[5][col]==0:
            return True


    def get_next_open_row(self, board, col):
        for r in range(row_count):
            if board[r][col] == 0:
                return r


    # flips the board to it's correct orientation
    def flip_board(self, board):
        return np.flip(board, 0)


    # checks for a win with recent drop
    def winning_move(self, board, piece):
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


    # generates the tkinter window with all the buttons
    def gen_window(self):
        win = tkinter.Tk()
        s = tkinter.StringVar(win, name="grid")
        t = tkinter.StringVar(win,name="extra")
        text = tkinter.Label(win, width=34, height=17, font="courier", bg="white", textvariable=t)
        text.grid(column=0,row = 3, columnspan = 7)
        lbl = tkinter.Label(win, width=34, height=17, font="courier", bg="white", textvariable=s)
        lbl.grid(column=0, row=0, columnspan=7)

        for i in range(7):
            id = chr(ord('A') + i)
            b = tkinter.Button(win, text=id, name="b_" + id, fg="blue", width="7", command=self.shooper(i))
            b.grid(column=i, row=1)
        win.setvar("grid", self.board)

        return win


    def send(self,selection):
        if self.is_valid_location(self.board, selection):
            id = chr(ord('A') + selection)
            self.top.setvar("extra","you selected column:" + id)
            row = self.get_next_open_row(self.board, selection)
            self.drop_piece(self.board, row, selection, self.Symbol)
            rec_data = self.flip_board(self.board)
            self.top.setvar('grid', rec_data)
            self.disable_buttons()
            s = str(selection)  # input the board
            self.client.sendall(s.encode())
            time.sleep(0.5)
            if self.winning_move(self.board, self.Symbol):
                self.disable_buttons()
                self.top.setvar("extra", self.Symbol + " wins!")
                time.sleep(3)
                self.game_over = True
        else:
            self.top.setvar("extra", self.Symbol + " picked an invalid column.")
            pass
        
        
    def recieve(self):
        time.sleep(0.5)
        r = int(self.client.recv(1024).decode())
        if self.is_valid_location(self.board, r):
            id = chr(ord('A') + r)
            self.top.setvar("extra", "Player two selected column:" + id)
            row = self.get_next_open_row(self.board, r)
            self.drop_piece(self.board, row, r, self.OppSymbol)
            rec_data = self.flip_board(self.board)
            self.top.setvar('grid', rec_data)
            self.enable_buttons()
            if self.winning_move(self.board, self.OppSymbol):
                self.disable_buttons()
                self.top.setvar("extra", self.OppSymbol + " wins!")
                time.sleep(3)
                self.game_over = True
        else:
            self.top.setvar("extra", self.OppSymbol + " picked an invalid column.")
            pass

































