import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)  # Utilisation du drapeau FULLSCREEN
pygame.display.set_caption("Animation Pygame")

# Couleur de fond
couleur_fond = (0, 0, 0)
print(type(couleur_fond))

# Vitesse de déplacement

vx_eyelid_1,vx_eyelid_2 = 0,0
vy_eyelid_1,vy_eyelid_2 = 10,10

x_eye_1, y_eye_1 = (largeur//2)-200, (hauteur//2)-100
x_eye_2, y_eye_2 = (largeur//2)+100, (hauteur//2)-100
x_eyelid_1, y_eyelid_1 = x_eye_1, y_eye_1-200
x_eyelid_2, y_eyelid_2 = x_eye_2, y_eye_2-200

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Mise à jour de la position de l'objet animé
    x_eyelid_1+=vx_eyelid_1
    x_eyelid_2+=vx_eyelid_2
    y_eyelid_1+=vy_eyelid_1
    y_eyelid_2+=vy_eyelid_2


    # Rebondir sur les bords de la fenêtre
    
    if y_eyelid_1<=y_eye_1-1000 or y_eyelid_1>=y_eye_1-10:
        vx_eyelid_1=-vx_eyelid_1
        vx_eyelid_2=-vx_eyelid_2
        vy_eyelid_1=-vy_eyelid_1
        vy_eyelid_2=-vy_eyelid_2
    


    # Effacer l'écran
    fenetre.fill(couleur_fond)

    # Dessiner l'objet animé (ici, un simple carré)

    pygame.draw.ellipse(fenetre, (5, 4, 170), ((largeur//2)-200, (hauteur//2)-100, 100, 200))
    pygame.draw.ellipse(fenetre, (5, 4, 170), ((largeur//2)+100, (hauteur//2)-100, 100, 200))

    pygame.draw.ellipse(fenetre, (0, 0, 0), (x_eyelid_1, y_eyelid_1, 100, 200))
    pygame.draw.ellipse(fenetre, (0, 0, 0), (x_eyelid_2, y_eyelid_2, 100, 200))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence de rafraîchissement
    pygame.time.Clock().tick(60)

# Quitter Pygame et terminer le programme
pygame.quit()
sys.exit()
