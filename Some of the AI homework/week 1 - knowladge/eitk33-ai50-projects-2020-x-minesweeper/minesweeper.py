import itertools
import random
import copy
import sys

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
        # EK

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
        # EK
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
        # EK
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if 0 < self.count == len(self.cells):
            return self.cells
        return None

    def known_safes(self):
        # EK
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        # EK
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        try:
            self.cells.remove(cell)
            self.count -= 1
        except KeyError:
            return

    def mark_safe(self, cell):
        # EK
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        try:
            self.cells.remove(cell)
        except KeyError:
            return

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
        # EK
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # EK
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # EK
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

        self.moves_made.add(cell)
        self.mark_safe(cell)

        new_set = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            if not 0 <= i < 8:
                continue
            for j in range(cell[1] - 1, cell[1] + 2):
                if not 0 <= j < 8:
                    continue
                new_set.add((i, j))
        sentence = Sentence(new_set, count)
        self.knowledge.append(sentence)
        checked = None
        while True:
            comp_list = [x for x in self.knowledge]
            self.mines_n_safes()
            self.itere()
            if comp_list == self.knowledge and checked:
                break
            elif comp_list == self.knowledge:
                checked = 1

        return

    def mines_n_safes(self):
        # EK
        while True:
            checker = 0
            for sentence in self.knowledge:
                sentence.cells.difference_update(self.safes)

                if sentence.known_mines():
                    tmp_list = [x for x in sentence.known_mines()]
                    for item in tmp_list:
                        self.mark_mine(item)
                    checker = 1
                else:
                    a = sentence.cells.intersection(self.mines)
                    if a:

                        count = sentence.count
                        sentence.cells.difference_update(self.mines)
                        sentence.count = count - len(a)

                if sentence.known_safes():
                    tmp_list = [x for x in sentence.known_safes()]
                    for item in tmp_list:
                        self.mark_safe(item)
                    checker = 1
            if checker == 1:
                self.knowledge = [x for x in self.knowledge if x.cells]
                continue
            else:
                break

    def iter(self):
        # EK
        while True:
            check = 0
            self.knowledge = [x for x in self.knowledge if x.cells]
            for a, b in itertools.combinations_with_replacement(self.knowledge, 2):
                if a == b:

                    continue
                new_sen = self.subsets(a, b)
                if new_sen:
                    check = 1
                    if len(new_sen.cells) == len(b.cells - a.cells):
                        self.knowledge.remove(b)
                        self.knowledge.append(new_sen)
                    elif len(new_sen.cells) == len(a.cells - b.cells):
                        self.knowledge.remove(a)
                        self.knowledge.append(new_sen)
            if check == 0:
                return

    def subsets(self, a, b):
        # EK
        if a.cells.issubset(b.cells):
            #print('subs if\n', a, 'a\n', b, 'b\n')
            diff = b.cells.difference(a.cells)
            count = b.count - a.count
            new_sen = Sentence(diff, count)

        elif b.cells.issubset(a.cells):
            #print('subs elif\n', a, 'a\n', b, 'b\n')
            diff = a.cells.difference(b.cells)
            count = a.count - b.count
            new_sen = Sentence(diff, count)

        else:
            return None
        return new_sen

    def make_safe_move(self):
        # EK
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        if self.safes > self.moves_made:
            av_moves = [i for i in self.safes.difference(self.moves_made)]
            a = random.choice(av_moves)

            return a
        return None

    def make_random_move(self):
        # EK
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        ints = [x for x in range(8)]
        pos = []
        for i in itertools.product(ints, repeat=2):
            if i not in self.moves_made and i not in self.mines:
                pos.append(i)
            else:
                pass

        if pos:
            move = random.choice(pos)
            return move
        else:
            return None
