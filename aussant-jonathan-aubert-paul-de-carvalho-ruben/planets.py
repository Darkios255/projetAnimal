
from grid import *
import random
from config import *
from elements import *


class PlanetAlpha(Grid):

    def __init__(self, name, longitude_cells_count, latitude_cells_count, ground):
        grid_init = []
        for i in range(longitude_cells_count):
            grid_ligne = []
            for i in range(latitude_cells_count):
                grid_ligne.append(ground)
            grid_init.append(grid_ligne)
        Grid.__init__(self, grid_init)
        self.longitude = longitude_cells_count
        self.lattitude = latitude_cells_count
        self.__name = name
        self.__ground = ground

    def get_ground(self):
        return self.__ground

    def get_name(self):
        return self.__name

    def is_free_place(self, cell_number):
        return self.get_cell(cell_number) == self.__ground

    def get_random_free_place(self, liste_collision):
        size = ( len(self.get_line(0)) * len(self.get_column(0)) ) -1
        collision = []
        for u in liste_collision:
            collision.append(self.get_cell_number_from_coordinates(u.x/32, u.y/32))
        for i in range(size):
            n = random.randint(0, size)
            if self.is_free_place(n) and n not in collision:
                return n
        return -1

    def place_resources_random(self, ressource, liste_collision):
        for i in ressource:
            self.set_cell(self.get_random_free_place(liste_collision), i)

    def place_resource(self, ressource, place): #place in cell_number
        self.set_cell(place, ressource)

    def get_autour_4(self, place): # place in coordonnee
        autour = []
        """ #REALISER POUR COORDONNEE
        if place[0] == 0:
            autour.append((None, None))
        else:
            autour.append((place[0]-self.lalitude, place[1]))
        if place[1]%self.lattitude == self.lattitude-1:
            autour.append((None, None))
        else:
            autour.append((place[0], place[1]+1))
        if place[0] == self.longitude-1:
            autour.append((None, None))
        else:
            autour.append((place[0]+self.lalitude, place[1]))
        if place[1] == 0:
            autour.append((None, None))
        else:
            autour.append((place[0], place[1]-1))
        """ #REALISER POUR CELL NUMBER
        if place < self.lattitude:
            pass #autour.append(None)
        else:
            autour.append(place-self.lattitude)
        if place%self.lattitude == self.lattitude-1:
            pass #autour.append(None)
        else:
            autour.append(place+1)
        if place >= (self.lattitude*(self.longitude-1)):
            pass #autour.append(None)
        else:
            autour.append(place+self.lattitude)
        if place%self.lattitude == 0:
            pass #autour.append(None)
        else:
            autour.append(place-1)        
        #"""
        return autour # au-dessus / a droite / en bas / a gauche
        







    
