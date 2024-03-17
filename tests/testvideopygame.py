import pygame
import sys

# Initialisation de Pygame
pygame.init()

# D�finition de la r�solution de l'�cran
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)


# Chargement de la vid�o
video_path = "/home/raspberry/Desktop/Projet_Vikki/tests/video_test.mp4"  # Remplacez par le chemin de votre vid�o

# D�marrez la lecture de la vid�o (peut �galement fonctionner avec des fichiers vid�o)
pygame.mixer.init()
pygame.mixer.music.load(video_path)
pygame.mixer.music.play(-1)  # -1 pour la lecture en boucle

# Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

# Arr�tez la musique et fermez Pygame
pygame.mixer.music.stop()
pygame.quit()
sys.exit()