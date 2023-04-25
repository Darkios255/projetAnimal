import pygame 

#-----------------#
### GAME CONFIG ###
#-----------------#

map_ = "map1"                                               # Charger la carte
TAILLE_CASE = 32                                            # Definir la Taille d'une case dans le jeu
pygame.display.set_caption('Islande Evolution')             # Definir le nom de la fenetre ( du jeu )
TAILLE_FENETRE = (1732, 972)                                # Definir la taille de taille de la fenetre
screen = pygame.display.set_mode(TAILLE_FENETRE, 0, 32)     # Appliquer la taille de la fenetre
clock = pygame.time.Clock() 

selection = [ ["debug"], ["vache", "loup", "cochon", "mouton", "humain"], ["terre", "eau", "herb"]    ]     # la liste que l'utilisateur va parcourir pour choisir l'action a faire

################### -- CHARGER LES IMAGES -- #####################

plaine_image = pygame.image.load("lands/" + 'sol/' +'plaine1.png')
vague_image1 =  pygame.image.load("lands/" + 'eau/' +'eau1.png')  
vague_image2 =  pygame.image.load("lands/" + 'eau/' +'eau2.png')  
pierre_image =  pygame.image.load("lands/" + 'pierre/' +'pierre.png')   
herbe_image = pygame.image.load("elements/" + 'herbe.png')


collide_image = pygame.image.load("lands/" + "testing/" + "COLLIDE.png")
error_image = pygame.image.load("lands/" + "testing/" + "ERROR.png")

cursor_base = pygame.image.load("elements/" + "mouse/" + "cursor_base.png")
human_image = pygame.image.load("elements/" + "humain/" + "humain_1.png")

pygame.mouse.set_visible(False)                 # Enlever le curseur de base
cursor_img_rect = cursor_base.get_rect()        # recuperer le rect du curseur