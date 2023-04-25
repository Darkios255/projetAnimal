# -*- coding: utf-8 -*-

import random
import turtle


class Grid:

    def __init__(self, grid_init):
        self.grid = grid_init
        self.lines_count = len(grid_init)
        self.columns_count = len(grid_init[0]) if len(grid_init) else 0


    def fill_random(self, values):
        res=[]
        for ligne in range(self.lines_count):
           l = []
           for element in range(self.columns_count):
               l.append(random.randint(values[0], values[len(values)-1]))
           res.append(l)
        self.grid=res



    def get_line(self, line_number):
        return self.grid[line_number]

    
    def get_column(self, column_number):
        c = []
        for ligne in range(self.lines_count):
            for element in range(self.columns_count):
                if element == column_number:
                    c.append(self.grid[ligne][element])
        return c


    def get_line_str(self, line_number, separator='\t'):
        chaine = ''
        for value in range(self.columns_count-1):
            chaine += str(self.grid[line_number][value])
            chaine += str(separator)
        chaine += str(self.grid[line_number][self.columns_count-1])
        return chaine


    def get_grid_str(self, separator='\t'):
        chaine = ''
        for ligne in range(self.lines_count-1):
            chaine += self.get_line_str(ligne, separator)
            chaine += '\n'
        chaine += self.get_line_str(self.lines_count-1, separator)
        return chaine


    def get_diagonal(self):
        min_ = self.lines_count
        if min_ > self.columns_count:
            min_ = self.columns_count
        li = []
        for i in range(min_):
            li.append(self.grid[i][i])
        return li


    def get_anti_diagonal(self):
        min_ = self.lines_count
        if min_ > self.columns_count:
            min_ = self.columns_count
        li = []
        for i in range(min_):
            li.append(self.grid[i][self.columns_count-1-i])
        return li


    def has_equal_values(self, value):
        for ligne in self.grid:
            for element in ligne:
                if element != value:
                    return False
        return True

      
    def is_square(self):
        if self.lines_count == self.columns_count:
            return True
        else:
            return False

      
    def get_count(self, value):
        occurence = 0
        for ligne in self.grid:
            for element in ligne:
                if element == value:
                    occurence += 1
        return occurence
        

       
    def get_sum(self):
        somme = 0
        for ligne in self.grid:
            for element in ligne:
                somme += element
        return somme



    def get_coordinates_from_cell_number(self, cell_number):
        somme = 0
        for ligne in range(len(self.grid)):
            for element in range(self.columns_count):
                if somme == cell_number:
                    return (ligne, element)
                somme += 1
        return False 


    def get_cell_number_from_coordinates(self, column_number, line_number):
        somme = 0
        for ligne in range(len(self.grid)):
            for element in range(self.columns_count):
                if ligne == line_number and element == column_number:
                    return somme
                somme += 1
        return False


    def get_cell(self, cell_number):
        num_ligne , num_colonne = self.get_coordinates_from_cell_number(cell_number)
        return self.grid[num_ligne][num_colonne]


    def set_cell(self, cell_number, value):
        num_ligne , num_colonne = self.get_coordinates_from_cell_number(cell_number)
        self.grid[num_ligne][num_colonne] = value
      
        
    def get_same_value_cell_numbers(self, value):
        l = []
        for ligne in range(len(self.grid)):
            for element in range(self.columns_count):
                if self.grid[ligne][element] == value:
                    l.append(self.get_cell_number_from_coordinates(ligne, element))
        return l
   

    def get_neighbour(self, line_number, column_number, delta, is_tore=True):
        line_v = line_number + delta[0]
        colum_v = column_number + delta[1]
        if ( colum_v >= self.columns_count or line_v >= self.lines_count ) and is_tore == False:
            return None
        elif colum_v >= self.columns_count:
            colum_v -= self.columns_count
        elif line_v >= self.lines_count:
            line_v -= self.lines_count
        voisin = self.grid[line_v][colum_v]
        return voisin
      

    def get_neighborhood(self, line_number, column_number, deltas, is_tore=True):
        return [self.get_neighbour(line_number, column_number, delta, is_tore)
                for delta in deltas]

    def draw_with_turtle(self, cell_size=50, margin=50, show_values=True):
        grid_width, grid_height = cell_size * self.columns_count, cell_size * self.lines_count
        turtle.setup(grid_width + 2 * margin, grid_height + 2 * margin)
        turtle.title(f"grille de {self.lines_count} lignes et {self.columns_count} colonnes")
        turtle.speed(0)
        for cell_number in range(self.lines_count * self.columns_count):
            line_number, column_number = self.get_coordinates_from_cell_number(cell_number)
            cell_center_x = -grid_width // 2 + cell_size // 2 + column_number * cell_size
            cell_center_y = grid_height // 2 - cell_size // 2 - line_number * cell_size
            if show_values:
                turtle.up()
                turtle.goto(cell_center_x, cell_center_y)
                turtle.down()
                turtle.write(self.get_cell(cell_number))
            if line_number == 0:
                cell_top_left_x = cell_center_x - cell_size // 2
                cell_top_left_y = cell_center_y + cell_size // 2
                turtle.up()
                turtle.goto(cell_top_left_x, cell_top_left_y)
                turtle.down()
                turtle.goto(cell_top_left_x, cell_top_left_y - grid_height)
            if column_number == 0:
                cell_top_left_x = cell_center_x - cell_size // 2
                cell_top_left_y = cell_center_y + cell_size // 2
                turtle.up()
                turtle.goto(cell_top_left_x, cell_top_left_y)
                turtle.down()
                turtle.goto(cell_top_left_x + grid_width, cell_top_left_y)
        turtle.up()
        turtle.goto(grid_width // 2, grid_height // 2)
        turtle.down()
        turtle.goto(grid_width // 2, grid_height // 2 - grid_height)
        turtle.up()
        turtle.goto(-grid_width // 2, -grid_height // 2)
        turtle.down()
        turtle.goto(-grid_width // 2 + grid_width, -grid_height // 2)
        turtle.exitonclick()
      


if __name__ == '__main__':
    random.seed(1000)  # Permet de générer toujours le 'même' hasard pour les tests

    # Constantes de directions
    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
    NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST = (-1, 1), (1, 1), (1, -1), (-1, -1)
    CARDINAL_POINTS = (NORTH, EAST, SOUTH, WEST)
    WIND_ROSE = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)

    # Constantes de test
    LINES_COUNT_TEST, COLUMNS_COUNT_TEST = 5, 7
    LINE_NUMBER_TEST, COLUMN_NUMBER_TEST = 1, 6
    VALUE_TEST = 0
    VALUES_TEST = list(range(2))
    IS_TORE_TEST = True
    DIRECTION_TEST = EAST
    GRID_INIT_TEST = [[VALUE_TEST] * COLUMNS_COUNT_TEST
                      for _ in range(LINES_COUNT_TEST)]

    CELL_SIZE_TEST = 100
    MARGIN_TEST = 20
    SHOW_VALUES_TEST = True

    # Tests
    grid_const = Grid(GRID_INIT_TEST)
    grid_random = Grid(GRID_INIT_TEST)
    grid_random.fill_random(VALUES_TEST)
    print(grid_const.grid)
    assert grid_random.grid == [[1, 0, 1, 1, 0, 1, 0], [1, 0, 0, 0, 1, 1, 0], [1, 0, 1, 0, 0, 1, 0], [1, 1, 0, 0, 1, 0, 0], [0, 1, 0, 1, 0, 0, 1]]
    assert (grid_random.lines_count, grid_random.columns_count) == (5, 7)
    assert grid_random.get_line(LINE_NUMBER_TEST) == [1, 0, 0, 0, 1, 1, 0]
    assert grid_random.get_column(COLUMN_NUMBER_TEST) == [0, 0, 0, 0, 1]
    assert grid_random.get_line_str(2) == '1\t0\t1\t0\t0\t1\t0'
    assert grid_random.get_grid_str('') == '1011010\n1000110\n1010010\n1100100\n0101001'
    assert grid_random.get_diagonal() == [1, 0, 1, 0, 0]
    assert grid_random.get_anti_diagonal() == [0, 1, 0, 0, 0]
    assert not grid_random.has_equal_values(GRID_INIT_TEST[0][0])
    assert grid_const.has_equal_values(GRID_INIT_TEST[0][0])
    assert not grid_random.is_square()
    assert grid_random.get_count(1) == grid_random.get_sum() == 16
    assert grid_random.get_coordinates_from_cell_number(13) == (1, 6)
    assert grid_random.get_cell_number_from_coordinates(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST) == 13
    assert grid_random.get_cell(9) == 0
    grid_random.set_cell(9, 1)
    assert grid_random.get_cell(9) == 1
    assert grid_random.get_same_value_cell_numbers(1) == [0, 2, 3, 5, 7, 9, 11, 12, 14, 16, 19, 21, 22, 25, 29, 31, 34]
    assert grid_random.get_neighbour(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, DIRECTION_TEST, IS_TORE_TEST) == 1
    assert not grid_random.get_neighbour(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, DIRECTION_TEST, not IS_TORE_TEST)
    assert grid_random.get_neighborhood(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, WIND_ROSE, IS_TORE_TEST) == [0, 1, 1, 1, 0, 1, 1, 1]
    assert grid_random.get_neighborhood(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, WIND_ROSE, not IS_TORE_TEST) == [0, None, None, None, 0, 1, 1, 1]
    grid_random.draw_with_turtle(CELL_SIZE_TEST, MARGIN_TEST, SHOW_VALUES_TEST)
    print("Tests all OK")

