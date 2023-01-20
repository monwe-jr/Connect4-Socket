from Client import Client
from GUI import GUI
import time as time

game_over = False
player_one = 1
player_two = 2
client_handler = Client()
grid = GUI(client_handler, game_over, player_one, player_two)   
turn = 0

while not game_over:
    if(turn == 0):
        grid.disable_buttons(player_two)
    else:   
        grid.disable_buttons(player_one)

    grid.enable_buttons(player_one)
    grid.enable_buttons(player_two)
    turn += 1
    turn = turn % 2

if game_over:
    time.sleep(5)
    client_handler.end()
    grid.destroy_grid()
    exit()

