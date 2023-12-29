import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        domain_copy = self.domains.copy()
        for var in self.domains:           
            values_copy = domain_copy[var].copy()
            for value in values_copy:
                if len(value) != var.length:
                    self.domains[var].remove(value)

        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        changed = False
        if self.crossword.overlaps[x,y] != None:
            overlap_x = self.crossword.overlaps[x,y][0]
            overlap_y = self.crossword.overlaps[x,y][1]
            
            nr_words_y = len(self.domains[y])

            copy_domain_x = self.domains[x].copy()
            for value_x in copy_domain_x:
                counter = 0
                for value_y in self.domains[y]:
                    if value_x[overlap_x] != value_y[overlap_y]:
                        counter += 1
                    else: # match found
                        break
                if counter == nr_words_y:
                    self.domains[x].remove(value_x)
                    changed = True                   
        
        return changed
        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs == None: # add all existing arcs.
            all_arcs = []
            for var1 in self.crossword.variables:
                for var2 in self.crossword.variables:
                    if var1 != var2:
                        if self.crossword.overlaps[var1,var2] != None:
                            all_arcs.append((var1,var2))
            queue = all_arcs
        else:
            queue = arcs

        while len(queue) != 0:
            #s = random.choice(queue)
            s = queue[0]
            queue.remove(s)
            list_s = []
            for item in s:
                list_s.append(item)
            x = list_s[0]
            y = list_s[1]
            if self.revise(x,y) == True:
                if len(self.domains[x]) == 0:
                    return False
                neighbors = self.crossword.neighbors(x)
                neighbors.remove(y)
                for z in neighbors:
                    queue.append(set((z,x)))

        return True

        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in self.domains:
            if var not in assignment.keys():
                return False
    
        return True

        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # check if values are distinct:
        list_values = []
        for var in assignment:
            list_values.append(assignment[var])
        
        if len(set(list_values)) != len(list_values):
            return False
        
        # check for correct length of values:
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
        
        # check for conflicts with neighboring variables
        for var in assignment:
            neighbors = self.crossword.neighbors(var) # set of all neighbors to var
            for neighbor in neighbors:
                i = self.crossword.overlaps[var,neighbor][0]
                j = self.crossword.overlaps[var,neighbor][1]

                if neighbor in assignment:
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
            
        return True
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        """
        # unordered:
        list_values = []

        for x in self.domains[var]:
            list_values.append(x)
               
        return list_values
        """
        # ordered:
        list_values = []

        for x in self.domains[var]:
            list_values.append(x)
               
        list_neighbors = []
        for neighbor in self.crossword.neighbors(var):
            if not neighbor in assignment:
                list_neighbors.append(neighbor)

        dict_values = {}
        for value in list_values:
            counter = 0
            for neighbor in list_neighbors:
                for value_neighbor in self.domains[neighbor]:
                    if value[self.crossword.overlaps[var,neighbor][0]] != value_neighbor[self.crossword.overlaps[var,neighbor][1]]:
                        counter += 1
            dict_values[value] = counter
        
        dict_values_sorted = dict(sorted(dict_values.items(), key=lambda item: item[1]))

        list_values_sorted = []
        for i in dict_values_sorted:
            list_values_sorted.append(i)

        return list_values_sorted
        # """
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        """
        # without heuristics:
        assigned_vars = []
        for var in assignment:
            assigned_vars.append(var) # append all the variables already assigned

        for var_assign in self.crossword.variables:
            if not var_assign in assigned_vars:
                return var_assign
        """

        # with heuristics:
        assigned_vars = []
        for var in assignment:
            assigned_vars.append(var) # append all the variables already assigned

        list_var_assign = []
        for var_assign in self.crossword.variables:
            if not var_assign in assigned_vars:
                list_var_assign.append(var_assign)

        list_var_assign_sorted = sorted(list_var_assign, key=lambda var: len(self.domains[var]), reverse=True)

        highest_number_of_values = self.domains[list_var_assign_sorted[0]]
        list_highest = []
        for v in list_var_assign_sorted:
            if self.domains[v] == highest_number_of_values:
                list_highest.append(v)

        if len(list_highest) > 1:
            list_highest_sorted = sorted(list_highest, key=lambda var: len(self.crossword.neighbors(var)))
            return list_highest_sorted[0]
        else:
            return list_highest[0]

        # """

        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print("START BACKTRACKING")

        if self.assignment_complete(assignment):
            if self.consistent(assignment):
                return assignment
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var,assignment):
            assignment[var] = value
            if self.consistent(assignment):
                # assignment[var] = value
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment.pop(var, None) # if key `var` does not exist in assignment, return None!
        return None

        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
