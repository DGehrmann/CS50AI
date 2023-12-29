import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

        #known_mines = set()
        #for cell in self.cells:
        #    if cell in MinesweeperAI.mines:
        #        known_mines.add(cell)
        #return known_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()
        #known_safes = set()
        #for cell in self.cells:
        #    if cell in MinesweeperAI.safes:
        #        known_safes.add(cell)
        #return known_safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            if self.count > 0:
                self.count -= 1
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            #if len(sentence.cells) == 0:
            #    self.knowledge.remove(sentence) # ?

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1)
        self.moves_made.add(cell)

        # 2)
        self.mark_safe(cell)

        # 3)
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if not ((i,j) in self.mines): 
                        if not ((i,j) in self.safes):
                            cells.add((i,j))
                    else: # cell is known to be a mine, cell is not added to sentence but count must be reduced by one
                        count -= 1
        if len(cells) != 0:
            new_sentence0 = Sentence(cells, count)
            if not new_sentence0 in self.knowledge:
                self.knowledge.append(new_sentence0)
        
        # print("Knowledge base:")
        # for i in range(0,len(self.knowledge)):
        #    print(self.knowledge[i])
        
        # 4)
        knowledge_changed =True
        while knowledge_changed:
            knowledge_changed = False

            safe_cells = []
            mine_cells = []

            for sentence in self.knowledge:
                if len(sentence.known_safes()) != 0:
                    safe_cells.append(sentence.known_safes())
                # print(f"Safe_Cells: {safe_cells}")
                if len(sentence.known_mines()) != 0:
                    mine_cells.append(sentence.known_mines())
                # print(f"Mine_Cells: {mine_cells}")
            
            if safe_cells: # check if safe_cells is empty
                knowledge_changed = True
                for safe_set in safe_cells:
                    safe_set_copy = safe_set.copy()
                    for safe_cell in safe_set_copy:
                        self.mark_safe(safe_cell)
                        
            if mine_cells:
                knowledge_changed = True
                for mine_set in mine_cells:
                    mine_set_copy = mine_set.copy()
                    for mine_cell in mine_set_copy:
                        self.mark_mine(mine_cell)
                        
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)

            # print(f"Known Mines: {self.mines}")
            # print(f"Safe Cells: {self.safes}")
                
            # 5)
            knowledge_copy = self.knowledge.copy()
            for sentence in knowledge_copy:
                for sentence2 in knowledge_copy:
                    if sentence != sentence2 and len(sentence2.cells) != 0:
                        if sentence2.cells.issubset(sentence.cells):
                            new_set = sentence.cells - sentence2.cells
                            new_count = sentence.count - sentence2.count
                            new_sentence = Sentence(new_set, new_count)
                            if not new_sentence in knowledge_copy :
                                self.knowledge.append(Sentence(new_set, new_count))
                                knowledge_changed = True


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for cell in self.safes:
            if not cell in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                possible_moves.append((i,j))
        
        valid_moves = []
        for move in possible_moves:
            if move not in self.moves_made:
                if move not in self.mines:
                    valid_moves.append(move)
        
        if len(valid_moves) == 0:
            return None
        
        return(random.choice(valid_moves))

