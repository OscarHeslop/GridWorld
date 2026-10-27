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
#ADDING BLOCK BUTTONS
#-----------------------------
button = pygame.Rect(600, 100, 150, 50)

# ! CREATING VARS 
start_col, start_row = None, None


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
#DRAWING GRID
#-----------------------------

def draw_grid(colour):
    for r in range(ROWS):
        for c in range(COLS):
            
                
            # Calculate position dynamically based on grid index
            x = c * square_size

            y = r * square_size
            
            # Draw the square onto the screen
            pygame.draw.rect(screen, pygame.Color(colour), (x, y, square_size, square_size), width=2)




    #add end
num_start = 0 
num_end = 0
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
        



agent_colour = (0,255,0) # green
def draw_agent(col, row): # x, y 
    
    #a circle
    center_x = col * square_size + square_size // 2
    center_y = row * square_size + square_size // 2
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

#------------------------------
#FOR LOOP
#-----------------------------
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
        #2)DECTECTING MOUSE PRESSES (ADDING BLOCK)
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
        #3)DECTECTING MOUSE PRESSES (REMOVING BLOCK)
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
                 
                run_RL = True 









    #---------------------
    # ! DISPLAY
    #---------------------
    #background - black 
    
    grid_colour = "#32a87d"
    bg_colour = (255, 255, 144)


    screen.fill(bg_colour)  #WHITE (RGB
    draw_grid(grid_colour)




    draw_blocks()

    if run_RL == True:
        if (start_col != None) and (start_row != None):
            draw_agent(start_col, start_row)

    









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
'''