from config import *
import pygame
import random


class Element:

    __ids_count = 1

    @classmethod
    def get_ids_count(cls):
        """
        Renvoie le nombre d'id presente
        """
        return cls.__ids_count

    @classmethod
    def incr_ids_count(cls):
        """
        Augmente le nombre d'id de 1
        """
        cls.__ids_count += 1

    def __init__(self, name):
        self.__name = name
        self.__id = Element.__ids_count
        Element.__ids_count += 1

    def __eq__(self, other):
        return self.__name == other.__name

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

####################################

class Ressource(Element):
    """
    Represente les ressources du jeu
    """

    def __init__(self, name, value):
        Element.__init__(self, name)
        self.__value = value

    def get_value(self):
        return self.__value

class Ground(Element):
    """
    Represente le sol du jeu
    """

    def __init__(self):
        Element.__init__(self, 'Ground')

####################################

class Herb(Ressource):
    """
    Represente la nourriture des herbivores du jeu
    """
    def __init__(self):
        Ressource.__init__(self, 'Herb', 0)

class Water(Ressource):
    """
    Represente un obstacle dans le jeu
    """
    def __init__(self):
        Ressource.__init__(self, 'water', 1)

class Stone(Ressource):
    """
    Represente un decor pour le jeu
    """
    def __init__(self):
        Ressource.__init__(self, 'stone', 2)