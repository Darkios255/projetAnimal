
import random
from config import *
from elements import *
from faune import *
from planets import PlanetAlpha
from game import *

def get_map(text):
        """
        Cette méthode permet de genrer la carte à partir d'un fichier texte
        """
        liste_collision = []
        f = open('lands/' + text + '.txt', 'r') # on ouvre le fichier texte
        data = f.read()
        f.close()
        data = data.split('\n') # on passe le fichier en liste de liste
        liste = []
        for row in data:
            liste.append(list(row))
        return liste

map__ = get_map(map_)                           # Creer la carte
planet = PlanetAlpha('Terre', 30, 54, Ground()) # definir la planet quii correspond au jeu
game = Game(planet, map__)                      # charger le jeu
game.start()                                    # demarrer le jeu

for coordonne_colision in game.liste_colision:
    planet.place_resource(Water(), planet.get_cell_number_from_coordinates(coordonne_colision.x//TAILLE_CASE, coordonne_colision.y//TAILLE_CASE))
#planet.place_resources_random([Herb() for _ in range(2)], game.liste_colision) # commencer le jeu avec 2 herbes
planet.place_resources_random([Stone() for _ in range(5)], game.liste_colision) # commencer le jeu avec 5 pierre

pygame.init()   # Lancer le jeu
running = True  # lancer le while

def can_spawn(faune, type_):
    """
    Verifie si l'objet donner a le droit d'apparaitre ( si il n'est pas dans l'eau ) et regarde si c'est un humain ou un animal
    """
    spawn = True
    for case in game.liste_colision:
        if faune.rect.colliderect(case):
            spawn = False
    if spawn == True:
        if type_ == 0:
            game.spawn_faune(faune)
        else:
            game.spawn_humain(faune)

while running:

    # Dectecion des evenements
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:   # Regarde si il faut quitter le jeu
            running = False
        if game.current_mode[0] != 0:   # Regarde si on n'est pas en mode debug
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:   # Passer en mode construction/Placement
                    if game.current_mode[0] == 1:
                        game.current_mode[0] = 2
                        game.current_mode[1] = 0
                    else:
                        game.current_mode[0] = 1
                        game.current_mode[1] = 0
                if event.button == 4:   # Regarde si on change de choix d'element par la mollette vers le bas
                    game.current_mode[1] -= 1
                    if game.current_mode[1] < 0:
                        game.current_mode[1] = len(selection[game.current_mode[0]])-1   # si on depasse du nombre d'element prevu, repartir à 0
                if event.button == 5:   # Regarde si on change de choix d'element par la mollette vers le haut
                    game.current_mode[1] += 1
                    if game.current_mode[1] > len(selection[game.current_mode[0]])-1:   # si on depasse du nombre d'element prevu, repartir à 0
                        game.current_mode[1] = 0
                if event.button == 1:    # Regarde si le clic gauche est declanché
                    if game.current_mode[0] == 1:
                        pos = (pygame.mouse.get_pos()[0] - 24, pygame.mouse.get_pos()[1] - 24 ) # recupere la position de la souris
                        if game.current_mode[1] == 0:
                            can_spawn(Cow(pos), 0)
                        if game.current_mode[1] == 1:
                            can_spawn(Wolf(pos), 0)
                        if game.current_mode[1] == 2:
                            can_spawn(Pig(pos), 0)
                        if game.current_mode[1] == 3:
                            can_spawn(Sheep(pos), 0)
                        if game.current_mode[1] == 4:
                            can_spawn((Human(human_image, pos)), 1)
                    if game.current_mode[0] == 2:
                        game.change_terrain(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN: # si le joueur n'a pas de molette, ici on regarde si il change grace au touche 1,2,3,4,5
                if event.key == pygame.K_1:
                    game.current_mode[1] = 0
                if event.key == pygame.K_2:
                    game.current_mode[1] = 1
                if event.key == pygame.K_3:
                    game.current_mode[1] = 2
                if event.key == pygame.K_4:
                    game.current_mode[1] = 3
                if event.key == pygame.K_5:
                    game.current_mode[1] = 4
            if game.current_mode[1] > len(selection[game.current_mode[0]])-1: # si on depasse du nombre d'element prevu, repartir à 0
                game.current_mode[1] = 0

                    
    game.update(screen)     
    pygame.display.flip()   # Actualiser la page
    clock.tick(30)          # Maintenir à n fps

pygame.quit()

