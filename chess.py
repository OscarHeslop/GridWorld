#displaying the board - make it pure python 

#is 8x8 grid 

#each is given points 

import pygame
import sys
import numpy as np





# 1. Initialize Pygame
pygame.init()

#IS 8 by 8
screen_width, screen_height = 800,800
ROWS, COLS = 8, 8
square_size = int(screen_width / ROWS)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Oscars RL Chess")

#----------------------------
#ALL SQUARE COLOURS
#----------------------------




colour_1 = pygame.Color("#32a852") #green 
colour_2 = pygame.Color("#3244a8") #blue
move_square_colour = pygame.Color("#f5427e") #pink


def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            if (r + c) % 2 == 0:
                square_colour = colour_1
            else:
                square_colour = colour_2
                
            # Calculate position dynamically based on grid index
            x = c * square_size

            y = r * square_size
            
            # Draw the square onto the screen
            pygame.draw.rect(screen, square_colour, (x, y, square_size, square_size))




#1 point to a pawn, 3 points to a knight or bishop, 5 points to a rook, and 9 points to the queen,

def straight_check(start, end):

    #check one variable changed 
    if (start[0] != end[0]) and (start[1] == end[1]):
        print("allowed st")
        return True
    elif (start[0] == end[0]) and (start[1] != end[1]): 
        print("not allowed st")
        return True
    else:
        return False
        
def diagonal_check(start, end):
    #GRADIENT 
    y = start[1] - end[1]
    x = start[0] - end[0]

    
    #MAKING SURE IS DIAGONAL - GRADIENT 1 
    if x != 0:
        if (float(y / x ))**2 == float(1.0): #check the modulus, POS OR NEG
            print("allowed di")
            return True 
        else:
            print("not allowed di")
            return False



from pathlib import Path
class Pieces():
    #all global vars 
    pieces_list = [] # shared between all the classes
    def __init__(self, name, file_path, possible_moves):
        self.file_path = file_path
        self.name = name
        self.row = 0 
        self.col = 0
        self.possible_moves = possible_moves
# between 1 and 8 

    def move(self, new_col, new_row): #x, y
        self.row = new_row 
        self.col = new_col #is col



    def add_to_board(self, row, col):
        self.row = row 
        self.col = col
        Pieces.pieces_list.append(self) #x, y
    def display(self):
        pieces = Pieces.pieces_list

        for i in range(len(pieces)):
            row = self.row
            col = self.col
        
            x = float(((col) * square_size)) #should be in the middle
            y = float(((row) * square_size) )

            path = Path(r"C:\Users/Oscar/Downloads/ALL ML PROJECTS/chess_img") #needs to be raw
            img = pygame.image.load(str(path / f'{self.file_path}')).convert_alpha() #makes transparent background
            #RATIO 
            if img.get_height() != 0 :
                ratio = square_size / (img.get_height())
                new_width = int(img.get_width() * float(ratio))
                new_height = int(img.get_height() * float(ratio)) #cannot have half a pixel 

                img = pygame.transform.smoothscale(img, (new_width, new_height))#smooth scale diff to scale, makes look cleaner
                screen.blit(img, (x, y))
            else:
                print("Image folder not found")


#--------------------------------
#CREATING THE PIECES 
#--------------------------------
knight1 = Pieces("knight", "wN.svg",("L"))
knight1.add_to_board(2, 3) #each one is a new instance 

knight2 = Pieces("knight", "wN.svg",("L"))
knight2.add_to_board(3, 4)


queen = Pieces("queen", "wQ.svg",("D","S")) #diagonal, straight
queen.add_to_board(4, 5)

bishop = Pieces("bishop", "wB.svg",("D"))
bishop.add_to_board(5, 6)

#adding to the board




#req 
#focus on the knight 
#when the knight moves goes to the correct spot
#when knight creates add to existing pieces and go through all the x, y coordinates 


        

#seperates sliding pieces to normal piece 
#add to list of possible moves 

#looks at all possible moves 


#sliding pieces 
'''' sebastian lague
https://www.youtube.com/watch?v=U4ogK0MIzqk
'''
#--------------------------
# ! MAIN GAME LOOP
#--------------------------


#--------------------------
# ! SETTING THE VARS
#--------------------------

x = None
y = None


counter = 0
selected_piece = None
running = True
start = None
end = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #-------------------------------
        # ! ALL INPUTS CHECKED HERE
        #-------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 means LEFT PRESSED / CLICKED
                # Get the raw pixel coordinates (e.g., x=450, y=120)
                mouse_x, mouse_y = event.pos
                
                # (between 1 and 8)
                clicked_col = int(mouse_x // square_size) 
                clicked_row = int(mouse_y // square_size)   


                x = (clicked_col) * square_size
                y = (clicked_row) * square_size





                

                if selected_piece == None: #if a piece selected 
                    #search for piece
                            
                    #PRINT THE CHESS PIECE CLICKED
                    for i, piece in enumerate(Pieces.pieces_list):
                        if (piece.col == (clicked_col)) and (piece.row == (clicked_row)): #a piece is clicked
                            selected_piece = i
                            counter += 1 

                    #picked a piece
                    start = (clicked_col, clicked_row)

                    print(clicked_col, clicked_row)
                    print(selected_piece)

                            
                #------------------------
                # ! MOVING THE PIECE
                #------------------------
                elif selected_piece != None and counter ==1:
                    #not search for piece
                    piece_obj = Pieces.pieces_list[selected_piece]

                    end = (clicked_col, clicked_row)

                    move_allow = False

                    for sub in list(piece_obj.possible_moves):
                             #look at the tuples in each sub
                            print(sub)
                            #S, D, L
                            if sub == "S":
                                if straight_check(start, end):
                                    piece_obj.col, piece_obj.row = end
                                else:
                                    print("not up")
                                    
                                    
                            elif sub == "D":
                                if diagonal_check(start, end):
                                    piece_obj.col, piece_obj.row = end 
                                else:
                                    print("not up")
                                
                            
                    counter = 0 
                    selected_piece = None 
                    start = None


                    #check if it follows move


                    


                    


                        
                        


                #detect when a piece is clicked 
                #count num clicks the one after that run the func 

                #update the display_array 

    
                






    #SCREEN DISPLAY 
    draw_board()    
    if (x != None) and (y != None):
        pygame.draw.rect(screen, move_square_colour, (x, y, square_size, square_size))

    #SHOWING PIECES 
    for piece in Pieces.pieces_list:
        piece.display()
    
    





    pygame.display.flip()


# Clean exit
pygame.quit()
sys.exit()
