#displaying the board - make it pure python 

#is 8x8 grid 

#each is given points 

import pygame
import sys
import numpy as np
import pygame_gui



pygame.init()
screen_width, screen_height = 800,800
ROWS, COLS = 8, 8
square_size = int(screen_width / ROWS)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Oscars RL Chess")


#------------------------------
#ADDING BLOCK BUTTONS
#-----------------------------
button = pygame.Rect(600, 100, 150, 50)




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



#------------------------------
#FOR LOOP
#-----------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #-------------------------------
        # INPUT CHECK=
        #-------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_x, mouse_y = event.pos
                
                clicked_col = int(mouse_x // square_size)                 # (between 1 and 8)
                clicked_row = int(mouse_y // square_size)   


                x = (clicked_col) * square_size
                y = (clicked_row) * square_size





    #---------------------
    # ! DISPLAY
    #---------------------
    #background - black 
    
    grid_colour = "#32a87d"
    bg_colour = (255, 255, 144)

    screen.fill(bg_colour)  #WHITE (RGB
    draw_grid(grid_colour)







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