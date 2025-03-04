import random

class GameState:
    def __init__(self):
        self.board = [] # Holds the game board with mines and numbers
        self.revealed = [] # Tracks which cells have been revealed (True or False)
        self.game_over = False # Flag to track if the game is over
        self.won = False # Flag to track if the player has won
    
    # Function to create the game board
    def create_board(self, cols, rows, num_mines):
        # Initialize the board with all cells set to 0
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)] # Initialize all cells as unrevealed
        
        mines_placed = 0 # Counter for placed mines
        
        # Place mines randomly on the board
        while mines_placed < num_mines:
            col = random.randint(0, cols - 1) # Random column index
            row = random.randint(0, rows - 1) # Random row index
            
            if self.board[row][col] != -1: # Don't place a mine where one already exists
                self.board[row][col] = -1
                mines_placed += 1 # Increment mines counter
        
        # Calculate the number of neighboring mines for each cell
        for row in range(rows):
            for col in range(cols):  
                if self.board[row][col] == -1: # Skip cells that are mines
                    continue
                
                mine_count = 0
                # Check all neighboring cells (in 3x3 grid)
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= row + i < rows and 0 <= col + j < cols: # Ensure within bounds
                            if self.board[row + i][col + j] == -1: # If the neighbor is a mine
                                mine_count += 1 # Increment the mine count
                self.board[row][col] = mine_count # Set the mine count for the current cell
    
    # Function to reveal a cell
    def reveal(self, row, col):
        # If the cell is a mine, reveal it and set game over
        if self.board[row][col] == -1:
            self.revealed[row][col] # Mark the mine cell as revealed
            self.game_over = True # End the game
        
        # If the cell is empty (0), recursively reveal neighboring cells
        elif self.board[row][col] == 0:
            for i in range(row - 1, row + 2): # Check the 3x3 grid surrounding the cell
                for j in range(col - 1, col + 2):
                    # Ensure we're within the bounds and the cell isn't already revealed
                    if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and not self.revealed[i][j]:
                        self.revealed[i][j] = True # Mark the cell as revealed
                        if self.board[i][j] == 0: # If the neighboring cell is also empty
                            self.reveal(i, j) # Recursively reveal further neighbors
        else:
            # If the cell contains a number, reveal it
            self.revealed[row][col] = True
    
    # Function to check if the player has won the game
    def check_won(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                # If any non-mine cell is not revealed, the game is not won yet
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return
                
        # If all non-mine cells are revealed, the player has won
        self.won = True

    
                
                
            