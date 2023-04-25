
import random
from config import *
from elements import *
from faune import *
from planets import PlanetAlpha
from math import sqrt
import pygame

class Game:

    def __init__(self, planet, map__):
        self.all_animals = pygame.sprite.Group()    # represente le groupe qui possede tous les animaux
        self.all_humans = pygame.sprite.Group()     # represente le groupe qui possede tous les humains
        self.planet = planet    # represente la planete qui correspond au jeu                   
        self.vitesse = 0        # represente la vitesse de jeu, la valeur peux etre soir -1 / 0 / 1
        self.tick = 0           # permet de regler les differantes importance de chaque action, il augmente à chaque passage de boucle
        self.liste_colision = [] # cette liste possede la liste en pygame.rect de tous les bloc qui on une collision
        self.current_mode = [1, 0]  # permet de definir le mode 0 pour debug, 1 pour faune, 2 pour build puis quel truc dans le mode
        self.map = map__

    def start(self):
        """
        Cette méthode se lance au début du programme pour démarrer le jeu. Elle appelle toute les fonction nécessaire au lancement
        """
        self.generer_map()

    def update(self, screen):
        """
        Cette méthode va être lancer à chaque passage de la boucle. C'est ici que le jeu se réalise et que les action sont réalisé.
        Les Actions sont réaliser en fonction de leur importance grâce au tick
        """
        #### Ici on verifie le jeu est en quel vitesse pour adapter combien on ajoute de tick par tour ####
        if self.current_mode[0] == 0: #on regarde si le jeu est en debug-mode, si c'esy le cas on arrete de faire progresser le jeu
            self.tick = 0
        elif self.vitesse == -1:
            self.tick += 0.5
        elif self.vitesse == 0:
            self.tick += 1
        elif self.vitesse == 1:
            self.tick += 2
        
        #### Ici on place toute les méthodes indispensable au jeu, qui n'on pas de lien avec la vitesse de jeu ####
        self.generer_map()
        self.afficher_element() # afficher les element de la carte

        #### Ici on effectue toute les actions qui sont tres importante, et qui doivent etre effectuer presque tout le temps ####
        if self.tick%1 == 0:

            cursor_img_rect.center = pygame.mouse.get_pos()  # on recupere la position du cursor
            cursor_img = pygame.image.load("elements/mouse/cursor_" + selection[self.current_mode[0]][self.current_mode[1]] + '.png')
            screen.blit(cursor_img, cursor_img_rect)       # on modifie le cursor de la souris en une image

            ## ici on parcours tous la faune pour verifier qu'il sont tous vivant ##
            for animal in self.all_animals:
                if animal.bar_life[0] <= 0:
                    self.all_animals.remove(animal)
            for human in self.all_humans:
                if human.vie <= 0:
                    self.all_humans.remove(human)

            ## ici on parcours la liste de tous les animaux et on les affiches par rapport a leur position ##
            for animal in self.all_animals:
                animation = self.load_animation(animal.name, animal.image)
                animal_flip = False
                if animal.direction[0] < 0:
                    animal_flip = True
                screen.blit((pygame.transform.flip(animation[self.tick%len(animation)], animal_flip, False)), animal.rect)
            for human in self.all_humans:
                screen.blit(human.image, human.rect)
            #self.all_animals.draw(screen)
            #self.all_humans.draw(screen)
            
            ## ici on parcours la liste de tous les animaux pour effectuer tous leur deplacement ##
            for animal in self.all_animals:
                    if animal.alimentation == 0:
                        predateur = animal.get_plus_proche_animal(self.get_predateur())
                        if predateur != None:
                            if sqrt((animal.rect.x - predateur.rect.x)**2 + (animal.rect.y - predateur.rect.y)**2) < 65:
                                if animal.rect.x < predateur.rect.x:
                                    if animal.rect.y < predateur.rect.y:
                                        animal.go_to_coordonne((animal.rect.x-predateur.rect.x, animal.rect.y-predateur.rect.y), self.liste_colision)
                                    else:
                                        animal.go_to_coordonne((animal.rect.x-predateur.rect.x, animal.rect.y+predateur.rect.y), self.liste_colision)
                                else:
                                    if animal.rect.y < predateur.rect.y:
                                        animal.go_to_coordonne((animal.rect.x+predateur.rect.x, animal.rect.y-predateur.rect.y), self.liste_colision)
                                    else:
                                        animal.go_to_coordonne((animal.rect.x+predateur.rect.x, animal.rect.y+predateur.rect.y), self.liste_colision)
                    if animal.food < 5:
                        if animal.alimentation == 0:
                            coordonne_herbe = animal.get_plus_proche_element(self.get_herbe()) # on recupere le rect de l'herbe la plus proche
                            if animal.go_to_coordonne(coordonne_herbe, self.liste_colision):
                                self.planet.set_cell(self.planet.get_cell_number_from_coordinates(coordonne_herbe.x//TAILLE_CASE, coordonne_herbe.y//TAILLE_CASE), Ground())
                        elif animal.alimentation == 1:
                            proie = animal.get_plus_proche_animal(self.get_proie())
                            if proie != None:
                                proie_coordonne = (proie.rect.x, proie.rect.y)
                                if animal.go_to_coordonne(proie_coordonne, self.liste_colision):
                                    proie.bar_life[0] = 0
                    else:
                        if random.randint(0, 15) == 0: # change de direction 1 fois sur 15
                            animal.change_direction()
                        animal.avancer(self.liste_colision)
            
            for human in self.all_humans:
                human.se_deplacer(self.liste_colision)
        
        #### Ici on effectue toute les actions qui sont a realiser moins souvent ####
        if self.tick%70 == 0:
            ## ici on regarde pour chaque herbe et on les repend au alentour ##
            for herbes in self.get_herbe():
                other = self.planet.get_autour_4(self.planet.get_cell_number_from_coordinates(herbes.x//TAILLE_CASE, herbes.y//TAILLE_CASE))
                ran = random.randint(0, len(other)-1)
                if self.planet.get_cell(other[ran]) == Ground(): # ici on reagarde si UN SEUL des coter est dispo, pour plus d'aleatoire
                    self.planet.place_resource(Herb(), other[ran])
        
        #### Ici on effectue toute les actions qui ne doivent pas etre réalisé pas souvent ####
        if self.tick%150 == 0:
            for animal in self.all_animals:
                animal.food -= 1            # on baisse la nourriture de tous les animaux
                if animal.food <= 0:
                    animal.bar_life[0] = 0  # si ils n'ont plus de nourriture, ils meurent
                animal.ageing()
                if animal.get_age() > 15:   # si ils ont trop vieux, ils meurent
                    animal.bar_life[0] = 0

    def spawn_faune(self, element):
        """
        Cette méthode sert à ajouter un animal à la partie
        """
        self.all_animals.add(element)
    
    def spawn_humain(self, element):
        """
        Cette méthode sert à ajouter un humain à la partie
        """
        self.all_humans.add(element)

    def afficher_element(self):
        """
        Cette méthode sert à afficher tous les elements de la partie
        """
        y = 0
        for ligne in self.planet.grid:
            x = 0
            for element in ligne:
                if element == Herb():
                    screen.blit(herbe_image, (x * TAILLE_CASE , y * TAILLE_CASE))
                if element == Stone():
                    screen.blit(pierre_image, (x * TAILLE_CASE , y * TAILLE_CASE))
                x += 1
            y += 1

    def get_herbe(self):
        """
        Cette méthode va renvoyer la liste de toutes les herbes de la partie sous forme de rect
        """
        liste_position_herbe =[]
        y = 0
        for ligne in self.planet.grid:
            x = 0
            for element in ligne:
                if element == Herb():
                    liste_position_herbe.append(pygame.Rect(x * TAILLE_CASE , y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
                x += 1
            y += 1
        return liste_position_herbe

    def get_proie(self):
        """
        Cette méthode renvoie la liste des animaux herbivore du jeu
        """
        liste_proie = []
        for animal in self.all_animals:
            if animal.name != "loup":
                liste_proie.append(animal)
        return liste_proie

    def get_predateur(self):
        """
        Cette méthode renvoie la liste des animaux carnivor du jeu
        """
        liste_predateur = []
        for animal in self.all_animals:
            if animal.name == "loup":
                liste_predateur.append(animal)
        return liste_predateur

    def generer_map(self):
        """
        Cette méthode permet de genrer la carte à partir d'une liste
        """
        liste_collision = []
        y = 0               
        for ligne in self.map: # on va parcourir la map par ligne puis par cellule
            x = 0            
            for case in ligne:
                if case == '0':
                    choose_img = random.randint(0, 2) # on ajoute de l'aleatoire, ici on a 2 eau possible, une sera choisi au hasard 
                    if choose_img == 0:
                        screen.blit(vague_image1, (x * TAILLE_CASE, y * TAILLE_CASE))
                    else:
                        screen.blit(vague_image2, (x * TAILLE_CASE, y * TAILLE_CASE))
                elif case == '1':
                    screen.blit(plaine_image, (x * TAILLE_CASE , y * TAILLE_CASE))
                elif case == '2':
                    screen.blit(pierre_image, (x * TAILLE_CASE, y * TAILLE_CASE))
                if case != '1': # On recupere tous les case qui ne sont pas de la terre et on les met dans la liste de collision
                    liste_collision.append(pygame.Rect(x * TAILLE_CASE , y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)) # la liste est consituer de rect
                x += 1
            y += 1
        self.liste_colision = liste_collision # on actualise la liste de collision
        ## Ici si le debug_mode est ON on afficher les collisions ##
        if self.current_mode[0] == 0: 
            for i in self.liste_colision:
                screen.blit(collide_image, (i.x, i.y))

    def load_animation(self, img, frame_durations):
        """
        permet de mettre dans une liste, les image nessessaire a l'animation
        """
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            n += 1
            for _ in range(frame):                                      
                animation_frame_data.append(pygame.image.load("elements/" + img + '/' + img + '_' + str(n) + '.png'))
        return animation_frame_data

    def change_terrain(self, pos):
        """
        Cette méthode prend la position de la souris, regarde sur quel choix l'utilisateur est placé et change le terrain à cette endroit
        """
        ligne_number = pos[0]//TAILLE_CASE
        colum_number = pos[1]//TAILLE_CASE
        if self.current_mode[1] == 0:
            self.map[pos[1]//TAILLE_CASE][pos[0]//TAILLE_CASE] = '1'
            self.planet.set_cell(self.planet.get_cell_number_from_coordinates(ligne_number, colum_number), Ground())
        elif self.current_mode[1] == 1:
            self.map[pos[1]//TAILLE_CASE][pos[0]//TAILLE_CASE] = '0'
            self.planet.set_cell(self.planet.get_cell_number_from_coordinates(ligne_number, colum_number), Water())
        elif self.current_mode[1] == 2:
            self.planet.set_cell(self.planet.get_cell_number_from_coordinates(ligne_number, colum_number), Herb())
        