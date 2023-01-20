import tkinter 
import numpy as np

class GUI:
    global row_count
    global column_count 
    row_count = 6
    column_count = 7

    def __init__(self, client_side, state, pOne, pTwo):
        self.game_over = state
        self.piece_one = pOne
        self.piece_two = pTwo
        self.board = self.create_board()
        self.top_one = self.gen_window("Player One", pOne)
        self.top_two = self.gen_window("Player Two", pTwo) 
        self.clients = client_side
        self.disable_buttons(self.piece_two)
        while not self.game_over:
            self.top_one.mainloop()
            self.top_two.mainloop()
            

    # disables buttons
    def disable_buttons(self, piece):
        if piece == self.piece_one:
            for i in range(7):
                id = chr(ord('A') + i)
                button = self.top_one.children['b_' + id]
                button['state'] = tkinter.DISABLED
        else:
            for i in range(7):
                id = chr(ord('A') + i)
                button = self.top_two.children['b_' + id]
                button['state'] = tkinter.DISABLED


    # enables buttons
    def enable_buttons(self, piece):
        if piece == self.piece_one:
            for i in range(7):
                id = chr(ord('A') + i)
                button = self.top_one.children['b_' + id]
                button['state'] = tkinter.NORMAL
        else:
            for i in range(7):
                id = chr(ord('A') + i)
                button = self.top_two.children['b_' + id]
                button['state'] = tkinter.NORMAL


    # closure function
    def shooper(self, i, piece):
        def shoop():
            self.insert(i, piece)
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
        for c in range(column_count):
            for r in range(row_count - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

            # Check positive diagonal locations for win
            for c in range(column_count - 3):
                for r in range(row_count - 3):
                    if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                        return True

            # Check negative diagonal locations for win
            for c in range(column_count - 3):
                for r in range(3, row_count):
                    if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                        return True


    def build_grid(self, board):
        gridStr = ""
        for c in range(column_count):
            s = ""
            if c == 0:
                s += "|  " + chr(ord('A') + c) + "  |"
            else: 
                s += "  " + chr(ord('A') + c) + "  |"
            gridStr += s  

        for r in range(row_count):
            s = "\n" + "------------------------------------------" + "\n"
            for c in range(column_count):
                if board[r][c] ==  self.piece_one:
                    if c == 0:
                        s += "|  " + "x" + "  |"
                    else:
                        s += "  " + "x" + "  |"
                elif board[r][c] ==  self.piece_two:
                    if c == 0:
                        s += "|  " + "o" + "  |"
                    else:
                        s += "  " + "o" + "  |"  
                else:
                    if c == 0:
                        s += "|  " + " " + "  |"
                    else:
                        s += "  " + " " + "  |"                        
            gridStr += s
            if r == row_count-1:
                gridStr += "\n" + "------------------------------------------"

        return gridStr


    def safety(self):
        self.state = True
        self.top_one.destroy()
        self.top_two.destroy()


    def destroy_grid(self):
        self.top_one.destroy()
        self.top_two.destroy()

    # generates the tkinter window with all the buttons
    def gen_window(self, title, piece):
        win = tkinter.Tk()
        s = tkinter.StringVar(win, name="grid")
        t = tkinter.StringVar(win,name="extra")
        lbl = tkinter.Label(win, width=42, height=15, font=("courier",13), bg="white", textvariable=s)
        lbl.grid(column=0, row=0, columnspan=7)
        text = tkinter.Label(win, width=42, height=7, font="courier", bg="white", textvariable=t)
        text.grid(column=0,row = 2, columnspan = 7)
        for i in range(7):
            id = chr(ord('A') + i)
            b = tkinter.Button(win, text=id, name="b_" + id, fg="blue", width=4, command=self.shooper(i, piece))
            b.grid(column=i, row=1)
        win.setvar("grid", self.build_grid(self.board))
        win.resizable(False,False)
        win.title(title)
        win.protocol("WM_DELETE_WINDOW",self.safety)

        return win

               

    def insert(self, selection, piece):
        if piece == self.piece_one:
            if self.is_valid_location(self.board, selection):
                id = chr(ord('A') + selection)
                self.top_one.setvar("extra","you selected column:" + id)
                self.top_two.setvar("extra","X selected column:" + id)
                row = self.get_next_open_row(self.board, selection)
                self.drop_piece(self.board, row, selection, piece)
                rec_data = self.flip_board(self.board)
                self.clients.send(self.build_grid(rec_data))
                response = self.clients.recieve_from_one()
                self.top_one.setvar('grid', response)
                self.top_two.setvar("grid", response)
                if self.winning_move(self.board, piece):
                    self.disable_buttons(self.piece_one)
                    self.disable_buttons(self.piece_two)
                    self.top_one.setvar("extra",  "You win!")
                    self.top_two.setvar("extra",  "X wins!")
                    self.state= True
            else:
                self.top_one.setvar("extra", "You picked an invalid column!")
                self.top_two.setvar("extra", "X picked an invalid column. Your turn.")
                pass

            if not self.game_over:
                self.disable_buttons(self.piece_one)
                self.enable_buttons(self.piece_two)

        else:
            if self.is_valid_location(self.board, selection):
                id = chr(ord('A') + selection)
                self.top_two.setvar("extra","you selected column:" + id)
                self.top_one.setvar("extra","O selected column:" + id)
                row = self.get_next_open_row(self.board, selection)
                self.drop_piece(self.board, row, selection, piece)
                rec_data = self.flip_board(self.board)
                self.clients.send(self.build_grid(rec_data))
                response = self.clients.recieve_from_two()
                self.top_two.setvar('grid', response)
                self.top_one.setvar('grid', response)
                if self.winning_move(self.board, piece):
                    self.disable_buttons(self.piece_one)
                    self.disable_buttons(self.piece_two)
                    self.top_two.setvar("extra",  "You win!")
                    self.top_one.setvar("extra",  "O wins!")
                    self.state = True
            else:    
                self.top_two.setvar("extra", "You picked an invalid column!")
                self.top_one.setvar("extra", "O picked an invalid column. Your turn.")
                pass

            if not self.game_over:
                self.disable_buttons(self.piece_two)
                self.enable_buttons(self.piece_one)
            
        