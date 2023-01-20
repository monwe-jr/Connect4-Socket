from Client import Client
from GUI import GUI
import time as time

player_one = 1
player_two = 2
client_handler = Client()
grid = GUI(client_handler, player_one, player_two)   
turn = 0

while True:
    if(turn == 0):
        grid.disable_buttons(player_two)
    else:   
        grid.disable_buttons(player_one)

    over = grid.get_state()
    print(over)
    if not over:
        grid.enable_buttons(player_one)
        grid.enable_buttons(player_two)
        turn += 1
        turn = turn % 2
    else:
        print("over")
        client_handler.end()
        grid.destroy_grid()
        exit()
    
       



