#displaying the board - make it pure python 

#is 8x8 grid 

#each is given points 

import pygame
import sys
import numpy as np
import pygame_gui



pygame.init()
screen_width, screen_height = 800,800
ROWS, COLS = 4,4
square_size = int(screen_width / ROWS)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Oscars RL Chess")


#------------------------------
# ! IMPORTANT VARIABLE INITIALISATION

#------------------------------
start_col, start_row = None, None
num_start, num_end = 0,0

moves_list = {
    "left": [-1, 0],   # Decrease horizontal (x)
    "right": [1, 0],   # Increase horizontal (x)
    "up": [0, -1],     # Decrease vertical (y) - moves upward
    "down": [0, 1]     # Increase vertical (y) - moves downward
}
end_reward = 10
hole_reward = -0.1
total_reward = 0


#------------------------------
# ! BLOCK CLASS
#------------------------------
class Block():
    #GLOBAL VARIABLES
    block_arr = [] 
    
    def add(clicked_col, clicked_row,type): #x, y
        if type=="s":
            Block.block_arr.append((clicked_col, clicked_row, "s")) #start
        elif type=="e":
            Block.block_arr.append((clicked_col, clicked_row, "e")) #end
        else:
            Block.block_arr.append((clicked_col, clicked_row, "h")) #hole


        print(clicked_col, clicked_row)
        print(Block.block_arr)
    def remove(clicked_col, clicked_row): #x, y
        for block in Block.block_arr:
            if block[0] == clicked_col and block[1] == clicked_row:
                Block.block_arr.remove(block)
                break



#------------------------------
# ! DRAWING GRID
#-----------------------------

def draw_grid(colour):
    for r in range(ROWS):
        for c in range(COLS):
            
                
            # Calculate position dynamically based on grid index
            x = c * square_size

            y = r * square_size
            
            # Draw the square onto the screen
            pygame.draw.rect(screen, pygame.Color(colour), (x, y, square_size, square_size), width=2)


#------------------------------
# ! DRAWING BLOCKS ON GRID
#-----------------------------
def draw_blocks():
    global num_start, num_end
    red = (255, 0, 0)#pygame.color
    blue = (0,0,255)
    black = (0,0,0 )
    for block in Block.block_arr:
        col, row, block_type = block

        block_x = (col) * square_size
        block_y = (row) * square_size

        if block_type == "s":#ONE START MAX
            pygame.draw.rect(screen, pygame.Color(blue), (block_x, block_y, square_size, square_size))
            block_type = "b"


        elif block_type == "e" and int(num_end) == 0:
            pygame.draw.rect(screen, pygame.Color(red), (block_x, block_y, square_size, square_size))
            block_type = "b"
        else:

            pygame.draw.rect(screen, pygame.Color(black), (block_x, block_y, square_size, square_size))
        

# ! -------------------------
# ! AGENT CLASS 
# ! -------------------------
agent_col, agent_row = None, None


agent_colour = (0,255,0) # green
class Agent:
    def __init__(self):
        self.col = None 
        self.row = None

        
    def random_move(self): 
        col, row = self.col, self.row # dont want to rewrite a million times

        global moves_list
        move_name = random.choice(list(moves_list.keys())) 
        move_change_pos = (moves_list[move_name])
        #UPDATING CLASS
        self.cur_move = move_name 
        
        #check if the move is valid 
        if (ROWS-1) >= col + int(move_change_pos[0])>=0 and (COLS - 1)>=(row + int(move_change_pos[1]))>= 0:
            print(f'New move to :{col + move_change_pos[0]}, {row + move_change_pos[1]}')
            new_col, new_row =col + move_change_pos[0], row + move_change_pos[1]

            self.col, self.row = new_col, new_row

            #getting index of cur move 
            cur_action =  list(moves_list.keys()).index(self.cur_move)#gives index
            #----------------------------
            # ! UPDATING Q TABLE
            Q_learning_inst.update_table(self.col, self.row, cur_action) #uses the instansiation
            #----------------------------
            return new_col, new_row
        else:
            return Agent_smith.random_move() #instansitated ver
    def get_reward(self):
        # get that specific block 
        reward = 0 
        for block in Block.block_arr:
            
            col, row, block_type= block #x, y
            if col == self.col and row == self.row:
                #found the block type
                if block_type == "h":
                    reward = -0.2
                elif block_type == "e":
                    reward = 10
        return reward
        



    def greedy_move(self):
        global moves_list
        #from current pos look at all possible moves, look for optimal one thats it 
        
        #create arr of all moves 
        temp_q_arr = [] 
        for i, move in enumerate(moves_list.values()): 
            col, row = agent_col + int(move[0]), agent_row + int(move[1]) #index to look in for q val
            #getting move_type 

            if not (0 <= col < COLS and 0 <= row < ROWS): #skips over whole loop not check in q table if outside range
                continue

            
            move_name = list(moves_list.keys())[i]
            #get the q val 
            Q_val = Q_learning.Q_table[col][row][i] 
            temp_q_arr.append(Q_val)
        #find getting best move - the q val index same as move name index same pos 
        best_move_index = temp_q_arr.index(max(temp_q_arr))
        move_name = moves_list.keys()[best_move_index]
        move_change_pos = moves_list.values()[best_move_index]
        #updating agent pos
        self.agent_col += move_change_pos[0]
        self.agent_row += move_change_pos[1]

        return self.agent_col, self.agent_row
        
    def draw_agent(self): # x, y 
        
        #a circle
        center_x = self.col * square_size + square_size // 2
        center_y = self.row * square_size + square_size // 2
        radius = square_size // 3
        pygame.draw.circle(screen, agent_colour, (center_x, center_y), radius)



def binary_grid():
    grid = np.zeros((COLS, ROWS), dtype="object") # numpy normally not built for strings, makes slower 


    for block in Block.block_arr:
        
        col, row, block_type= block #x, y
        if block_type == "s":
            grid[col, row] = "s"

        elif block_type == "e":
            grid[col, row] = "e"
            

        else: #black
            grid[col, row] = "1"
    print(grid)
    return grid




#-----------------------------------------------------------------
def reset_agent():
    
    global showed_end, start_row, start_col, epoch
    print(f"Epoch {epoch}")
    Agent_smith.col, Agent_smith.row = start_col, start_row


# ! -------------------------
# ! Q LEARNING CLASS 
# ! -------------------------
import random
class Q_learning():
    global moves_list
    def __init__(self):
        self.cur_move = None #current_move
        self.Q_table = np.ones((COLS,ROWS,len(moves_list)),dtype=float)*1.0/len(moves_list) #from Microsoft github
    
    def update_table(self, agent_col, agent_row, cur_action): # Qtable
        alpha = 0.1
        gamma = 0.95 
        #GETTING Q MAX FOR ALL POSSIBLE MOVES 
        #get the coords of the left, right, up down, storing in array
        temp_q_arr = [] 
        for i, move in enumerate(moves_list.values()): 

            col, row = agent_col + int(move[0]), agent_row + int(move[1]) #index to look in for q val
            if not (0 <= col < COLS and 0 <= row < ROWS):
                continue #skips over loop doesnt append it so not check in q table out of range 
            #getting move_type 
            move_name = list(moves_list.keys())[i]
            #get the q val 
            Q_val = self.Q_table[col][row][i] 
            temp_q_arr.append(Q_val)
        #getting maxQ 
        max_Q = max(temp_q_arr)
        #finding max_q for all the moves beside it 
        cur_reward = Agent_smith.get_reward()
        #TEMPORAL DIFFERENCE EQUATION
        old_q = self.Q_table[agent_col][agent_row][cur_action] 
        new_q= old_q + alpha * ((cur_reward + gamma * max_Q)- old_q)
        #WRITING BACK TO TABLE
        self.Q_table[agent_col][agent_row][cur_action] = new_q
        print(f"updated_table {old_q}->{new_q}")


#------------------------------
# ! MAIN LOOP
#-----------------------------
epoch = 0 
num_epochs = 10
thresh = int(0.1 * num_epochs)

# ! Class intansiation
Q_learning_inst = Q_learning()
Agent_smith = Agent()
time_delay = 100 # millisec
showed_end = False



# ! Variable setting
# used for time delay
grid_colour = "#32a87d"
bg_colour = (255, 255, 144)
last_move = 0
num_steps = 0 

selected_type = "black"
run_RL = False




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # ! --------------------------------
        # ! KEYBOARD PRESS DETECTION
        # ! --------------------------------
        #--------------------------------
        #1)DETECTING KEYBOARD PRESSES
        #--------------------------------



        if event.type == pygame.KEYDOWN:

            #check if start and end already exist 
            if event.key == pygame.K_s :
                selected_type= "s"
            elif event.key == pygame.K_e:
                selected_type = "e"
            else:
                selected_type= "h"



        #--------------------------------
        # ! 2)DECTECTING MOUSE PRESSES (ADDING BLOCK)
        #--------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(selected_type)


            start_exists = any(b[2] == "s" for b in Block.block_arr)#True means exists
            end_exists   = any(i[2] == "e" for i in Block.block_arr)

            mouse_x, mouse_y = event.pos

            clicked_col = mouse_x // square_size
            clicked_row = mouse_y // square_size

            if selected_type==  "s" and not start_exists:
                Block.add(clicked_col, clicked_row, "s")
                start_col, start_row = clicked_col, clicked_row
            elif selected_type==  "e" and not end_exists:
                Block.add(clicked_col, clicked_row, "e")
            
            #START NOT EXIST
            else:
                Block.add(clicked_col, clicked_row, "black")
                

        #--------------------------------
        # ! 3)DECTECTING MOUSE PRESSES (REMOVING BLOCK)
        #--------------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: 

                mouse_x, mouse_y = event.pos
                clicked_col = mouse_x // square_size
                clicked_row = mouse_y // square_size



                for i, block in enumerate(Block.block_arr):
                    if block[0] == clicked_col and block[1] == clicked_row:
                                
                        Block.block_arr.remove(Block.block_arr[i])

                        print(Block.block_arr)
        
        #--------------------------------
        # ! RUNNING GAME - ENTER PRESSED
        #--------------------------------
        
        if event.type == pygame.KEYDOWN: 

            if event.key == pygame.K_RETURN: # ! ENTER KEY PRESSED
                grid = binary_grid() #creates binary grid of all obstacles

                
                # ! getting end col pos 
                end_col, end_row = np.where(grid == "e")
                end_col, end_row = int(end_col[0]), int(end_row[0])
                
                run_RL = True 

                if (start_col != None) and (start_row != None):
                    Agent_smith.col, Agent_smith.row = start_col, start_row









    #---------------------
    # ! DISPLAY
    #---------------------


    screen.fill(bg_colour)  #WHITE (RGB
    draw_grid(grid_colour)




    draw_blocks()

    if run_RL == True:
        if (Agent_smith.col != None) and (Agent_smith.row != None):
            Agent_smith.draw_agent()

            # ! ----------------------------
            # ! REACHES END / GOAL 
            # ! ----------------------------
            if Agent_smith.col == end_col and Agent_smith.row == end_row:
                if showed_end == False:
                    #show new Qtable
                    print("reached goal")
                    print(Q_learning_inst.Q_table)
                    reset_agent()
            # ! ----------------------------
            # ! NUM EPOCHS FINISHED
            # ! ----------------------------
            if epoch >= num_epochs:
                running = False
                print("Agent smith training complete")
            




            elif  Agent_smith.col != end_col or Agent_smith.row != end_row:
                #only do after 3secondss
                time_since_last_move = pygame.time.get_ticks() - last_move
                if time_since_last_move >= time_delay:
                    # ! RANDOM OR GREEDY 
                    if epoch < thresh:
                        agent_col, agent_row = Agent_smith.random_move()
                        num_steps += 1
                    elif epoch >= thresh:
                        agent_col, agent_row = Agent_smith.greedy_move()
                        num_steps +=1 


                    last_move = pygame.time.get_ticks() #reset timer
                


    









    pygame.display.flip()


# Clean exit
pygame.quit()
sys.exit()

'''
For me

SEE Repo currently linked
git remote -v

Ovverrides current git with new
git remote set-url origin https://github.com/OscarHeslop/GridWorld.git

git restore --staged .
'''