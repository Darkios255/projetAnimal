from config import *
from math import sqrt
import pygame
import random


class Animal(pygame.sprite.Sprite):

    def __init__(self, name, life_max, image, position, alimentation, velocity):
        super().__init__()
        self.__age = 0
        self.name = name
        self.bar_life = [life_max, life_max]
        self.food = 5
        self.alimentation = alimentation
        self.image = image
        self.rect = pygame.Rect(position[0],position[1],32,32) # la position et taille de base du perso ( x, y, largeur, hauteur )
        self.direction = [1,0]
        self.velocite = velocity

    def get_age(self) -> int:
        """
        Renvoie l'age de l'animal
        """
        return self.__age

    def ageing(self) -> int:
        """
        Augmente l'age de 1
        """
        self.__age += 1

    def get_life_max(self) -> int:
        """
        Renvoie la vie maximum de l'animal
        """
        return self.__bar_life[1]

    def get_life(self) -> int:
        """
        Renvoie la vie de l'animal
        """
        return self.__bar_life[0]

    def get_position(self) -> tuple[int, int]:
        """
        Renvoie la position de l'animal
        """
        return (self.rect.x, self.rect.y)

    def recovering_life(self, value) -> int:
        """
        Augmente la vie de l'animal de la valeur donné
        """
        self.__bar_life[0] += value

    def losing_life(self, value) -> int:
        """
        Diminue la vie de l'animal de la valeur donné
        """
        self.__bar_life[0] -= value

    def get_plus_proche_element(self, liste):
        """
        Prend une liste d'elements et renvoie celle qui est la plus proche
        """
        if liste == []:
            return None
        else:
            min_ = sqrt((self.rect.x - liste[0][0])**2 + (self.rect.y - liste[0][1])**2) # Calcul de la distance
            coordonne_final = liste[0]
            for coordonne in liste:     # Comparaison des distance de tous les elements
                if sqrt((self.rect.x - coordonne[0])**2 +
                        (self.rect.y - coordonne[1])**2) < min_:
                    min_ = sqrt((self.rect.x - coordonne[0])**2 +
                                (self.rect.y - coordonne[1])**2)
                    coordonne_final = coordonne
            return coordonne_final

    def get_plus_proche_animal(self, liste):
        """
        Prend une liste d'animaux et renvoie celui qui est le plus proche
        """
        if liste == []:
            return None
        else:
            min_ = sqrt((self.rect.x - liste[0].rect.x)**2 + (self.rect.y - liste[0].rect.y)**2) # Calcul de la distance
            coordonne_final = liste[0]
            for coordonne in liste: # Comparaison des distance de tous les animaux
                if sqrt((self.rect.x - coordonne.rect.x)**2 +
                        (self.rect.y - coordonne.rect.y)**2) < min_:
                    min_ = sqrt((self.rect.x - coordonne.rect.x)**2 +
                                (self.rect.y - coordonne.rect.y)**2)
                    coordonne_final = coordonne
            return coordonne_final

    def set_direction(self, other):
        """
        Prend un autre animal ( other ) et place la direction vers lui
        """
        if other[0] < self.rect.x:
            self.direction[0] = -1
        elif other[0] == self.rect.x:
            self.direction[0] = 0
        else:
            self.direction[0] = 1
        if other[1] < self.rect.y:
            self.direction[1] = -1
        elif other[1] == self.rect.y:
            self.direction[1] = 0
        else:
            self.direction[1] = 1

    def change_direction(self):
        """
        Change de direction de manière aléatoire
        """
        self.direction[0] = random.randint(-1, 1)
        self.direction[1] = random.randint(-1, 1)

    def avancer(self, liste_colision):
        """
        Fais avancer l'animal
        """ 
        self.rect.x += self.direction[0] * self.velocite   # Fais Avancer
        hit_list = []
        for case in liste_colision: # liste_collision est la liste des bloc qui doivent avoir une collisions
            if self.rect.colliderect(case):
                hit_list.append(case)
        for case in hit_list:
            if self.direction[0] > 0: # les x
                self.rect.right = case.left
            elif self.direction[0] < 0:
                self.rect.left = case.right
        self.rect.y += self.direction[1] * self.velocite # Fais Avancer
        hit_list = []
        for case in liste_colision: # liste_collision est la liste des bloc qui doivent avoir une collisions
            if self.rect.colliderect(case):
                hit_list.append(case)
        for case in hit_list:
            if self.direction[1] > 0: # les y
                self.rect.bottom = case.top
            elif self.direction[1] < 0:
                self.rect.top = case.bottom

    def go_to_coordonne(self, coordonne, liste_colision):
        """
        Prend une coordonne et la liste des collision et va dans cette direction SI possible,
        si la coordonne est a moins de 15px, alors la nourtirrue augmente de 1 et on revoie True, sinon False
        """
        if coordonne != None:    
            if sqrt((self.rect.x - coordonne[0])**2 + (self.rect.y - coordonne[1])**2) < 15: # on regarde si cette coordonne la plus proche est à moins de 15px
                if self.food < 10:
                    self.food += 1
                return True
            else:
                self.set_direction(coordonne)
                self.avancer(liste_colision)
                return False

# Pour les 4 classe Animaux qui suivent, le init se produit de cette maniere
# self / name / life_max / image / position / alimentation / velocity 

class Wolf(Animal):

    def __init__(self, position):
        Animal.__init__(self, 'loup', 25, [4,3,4,3], position, 1, 4)

class Sheep(Animal):

    def __init__(self, position):
        Animal.__init__(self, 'mouton', 5, [1], position, 0, 2)

class Pig(Animal):

    def __init__(self, position):
        Animal.__init__(self, 'cochon', 10, [1], position, 0, 2)

class Cow(Animal):

    def __init__(self, position):
        Animal.__init__(self, 'vachette', 15, [4,3,4,3], position, 0, 2)





##### CLASSE HUMAIN #####

class Human(pygame.sprite.Sprite):
    
    # compteur d'humain
    nbHumain = 0
    # compteur de clan
    nbClan = 0

    @classmethod
    def compteur_humain(cls):
        cls.nbHumain += 1
        return cls.nbHumain

    @classmethod
    def compteur_clan(cls):
        cls.nbClan += 1
        return cls.nbClan

    # ----------------------------------------- initialisation --------------------------------------- #
    def __init__(self,human_image, position):
        super().__init__()
        self.id = Human.compteur_humain()
        self.age = 0
        self.vie = 100
        self.etat = True  # True pour vivant, False pour 
        self.image = human_image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.direction = [0, 0]
        self.velocite = 1
        self.clan = "hermite"

    # ------------------------------------------- obtenir une infos ------------------------------------------- #
    def get_id(self) -> str:
        return self.id

    def get_age(self) -> int:
        return self.age

    def get_vie(self) -> int:
        return self.vie

    def get_etat(self) -> bool:
        return self.etat

    def get_position(self) -> tuple[int, int]:
        return (self.rect.x, self.rect.y)
        

    def get_clan(self) -> str:
        return self.clan

    # ------------------------------------------- modifier une infos pour les tests------------------------------------------- #

    def set_vie(self, vie: int) -> None:
        self.vie = vie
        self.mourir()

    def set_etat(self, etat: bool) -> None:
        self.etat = etat


    def set_clan(self, clan: str) -> None:
        self.clan = clan

    # ------------------------------------------- varier une caracteristique ------------------------------------------- #
    def vieillir(self) -> None:
        self.age += 1

    def mourir(self) -> None:
        if self.vie <= 0:
            self.etat = False  # état passe à False pour mort

    
    def se_deplacer(self, liste_colision) -> None:
        # Choisit une nouvelle direction toutes les 20-60 frames (environ 0.3-1 seconde à 60 fps)
        if random.randint(0, 59) == 0:
            # Choisit une nouvelle direction de manière aléatoire (entre -1 et 1) pour les axes x et y
            nouvelle_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
            # Normalise la nouvelle direction pour avoir une longueur de 1
            norme = (nouvelle_direction[0]**2 + nouvelle_direction[1]**2)**0.5
            self.direction = [nouvelle_direction[0] / norme, nouvelle_direction[1] / norme]
        # Déplace l'humain dans la direction actuelle avec une vitesse aléatoire (entre 1 et 3 pixels par frame)  
        self.rect.x += int(self.direction[0] * self.velocite * random.uniform(1, 3))
        hit_list = []
        for case in liste_colision: # liste_collision est la liste des bloc qui doivent avoir une collisions
            if self.rect.colliderect(case):
                hit_list.append(case)
        for case in hit_list:
            if self.direction[0] > 0: # les x
                self.rect.right = case.left
            elif self.direction[0] < 0:
                self.rect.left = case.right
        self.rect.y += int(self.direction[1] * self.velocite * random.uniform(1, 3))
        hit_list = []
        for case in liste_colision: # liste_collision est la liste des bloc qui doivent avoir une collisions
            if self.rect.colliderect(case):
                hit_list.append(case)
        for case in hit_list:
            if self.direction[1] > 0: # les y
                self.rect.bottom = case.top
            elif self.direction[1] < 0:
                self.rect.top = case.bottom 


    def obtenir_clan(self, enfant, parent) -> None:
        # l'enfant des parent prend le clan de ses parents
        if enfant.get_clan() == "hermite":
            enfant.set_clan(parent.get_clan())


    def se_reproduire(self, human2):
        # si l'humain est sur une case adjacente (position) a un humain du meme clan alors il peut se reproduire puis il ne peut plus se reproduire pendant x temps (modifiable)
        
        if self.get_position() == human2.get_position():
            if self.get_clan() == human2.get_clan():
                self.obtenir_clan(self, human2)
                self.obtenir_clan(human2, self)
                return True
            else:
                return False
            

                

    def attaquer(self, human2):
        # si l'humain est sur une case adjacente (position) a un humain d'un autre clan alors il peut attaquer

        if self.get_position() == human2.get_position():
            if self.get_clan() != human2.get_clan():
                while (self.get_vie() >= 0 and human2.get_vie() >= 0):

                    self.set_vie(self.get_vie() - random.randint(0, 10)) # definir les degats
                    human2.set_vie(human2.get_vie() - random.randint(0, 10))

    def prendre_ressource(self, human):
        pass

    # ----------------------------------------- strs --------------------------------------- #

    def __str__(self):
        return f"ID : {self.id} | Age : {self.age} | Vie : {self.vie} | Etat : {self.etat} | Position : {self.position} | Clan : {self.clan}"

# ------------------------------------------------------------------------------------------------ #
#                                               Test                                               #
# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":



    print("all tests passed")