from Client import Client

game_over = False
clientOne = Client(game_over, 1, 0)
clientTwo = Client(game_over, 0, 1)
turn = 0

while not game_over:
    if turn == 0:
        clientTwo.recieve
    else:
        clientOne.recieve 
    turn += 1
    turn = turn % 2 