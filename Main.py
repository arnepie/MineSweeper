import pygame
import math
import GameState

pygame.init()

# Initialize the GameState object and the pygame screen
game_state = GameState.GameState()
screen = pygame.display.set_mode((600, 600)) 

# Game Settings
rows = 9
columns = 9
number_of_mines = 10

# Function to draw the board on the screen
def draw_board(rows, cols, screen):
    black = (0, 0, 0)
    white = (255,255,255)
    
    pygame.display.set_caption('MineSweeper') 
    screen.fill(black)
    
    x_pos = y_pos = 30
    # Loop through rows and columns to draw grid squares
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, white, pygame.Rect(x_pos, y_pos, 60, 60))
            pygame.draw.rect(screen, black, pygame.Rect(x_pos, y_pos, 60, 60), 5)
            x_pos += 60 # Move to next column
        y_pos += 60 # Move to next row
        x_pos = 30 # Reset to the x position to the left of the board
    
    pygame.display.flip() # Update the display

# Function to update the board with revealed cells
def update_board(rows, cols):
    font = pygame.font.Font('freesansbold.ttf', 32)
    black = (0, 0, 0)
    red = (255, 0, 0)
    
    # Loop through all rows and columns to render the revealed cells
    for row in range(rows):
        for col in range(cols):
            if game_state.revealed[row][col] == True: # Check if cell is revealed
                pygame.draw.rect(screen, black, pygame.Rect((col * 60) + 30,(row * 60) + 30, 60, 60))
                
                # Render the revealed cell
                text = font.render(str(game_state.board[row][col]), True, red)
                textRect = text.get_rect(center=((col * 60 + 60), (row * 60 + 60)))
                screen.blit(text, textRect)
                
                pygame.display.flip() # Update display

# Function to handle left-click and right-click events
def clicked(mouse_x, mouse_y, button):
    row = math.ceil((mouse_y - 30) / 60) # Calculate the row from the mouse position
    col = math.ceil((mouse_x - 30) / 60) # Calculate the column from the mouse position
    
    if button == 1: # Left click
        game_state.reveal(row - 1, col - 1) # Reveal the clicked cell
        
        if game_state.board[row - 1][col - 1] == -1: # If it's a bomb
            reveal_bomb(row - 1, col - 1) # Show the bomb image
    
    elif button == 3: # Right click (to place flag)
        flag_image = pygame.image.load("flag.png") # Load flag image
        flag_image = pygame.transform.scale(flag_image, (60, 60)) # Scale to fit the square
        screen.blit(flag_image, (col * 60 - 30, row * 60 - 30)) # Place the flag in the clicked position
        pygame.display.flip() # Update display
                                            
# Function to reveal the bomb when it's clicked
def reveal_bomb(row, col):
    bomb_image = pygame.image.load("bomb.png") # Load bomb image
    bomb_image = pygame.transform.scale(bomb_image, (60, 60)) # Scale image to fit the square
    screen.blit(bomb_image, (col * 60 + 30, row * 60 + 30)) # Place bomb in the clicked position
    pygame.display.flip() # Update display

# Function to display the end message
def end_message(message):
    font = pygame.font.Font('freesansbold.ttf', 64)
    black = (0, 0, 0)
    red = (255, 0, 0)

    text = font.render(message, True, red) # Render the end message
    textRect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)) # Center the message on screen
    
    # Draw a background for the text
    pygame.draw.rect(screen, black, textRect.inflate(20, 20))
    screen.blit(text, textRect) # Draw the text on screen

    pygame.display.flip() # Update the display
        
# Main function to run the game
def main():
    game_state.create_board(rows, columns, number_of_mines) # Create the game board
    draw_board(rows, columns, screen) # Draw the initial empty board
        
    running = True
    while running: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # Close the window
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN: # When mouse is clicked
                mouse_x, mouse_y = event.pos # Get the mouse position
                
                if 30 <= mouse_x <= 570 and 30 <= mouse_y <= 570:
                    clicked(mouse_x, mouse_y, event.button) # Call the clicked function when a cell is clicked
                    update_board(rows, columns) # Update the board after a click
            
            game_state.check_won() # Check if the player has won
            
            if game_state.game_over: # If game over, show the message
                end_message("Game Over!")
            elif game_state.won: # If won, show the message
                end_message("You Won!")
        
    
main()