import robot
import pygame

def screen_manager(instance_robot):
    
    pygame.init()
    
    if instance_robot.fullscreen:
        instance_robot.window = pygame.display.set_mode((instance_robot.largeur, instance_robot.hauteur), pygame.FULLSCREEN)  # Utilisation du drapeau FULLSCREEN
    else:
        instance_robot.window = pygame.display.set_mode((instance_robot.largeur, instance_robot.hauteur))
    pygame.display.set_caption(instance_robot.title_caption)
    
    while instance_robot.active_window != '':
        match instance_robot.active_window:
            case 'screen_loading_init':  
                screen_loading_init(instance_robot)
            case 'screen_eye_watching':  
                screen_eye_watching(instance_robot)
            case 'screen_loading_wifi_connection':
                screen_loading_wifi_connection(instance_robot)
            case 'screen_loading_no_wifi':
                screen_loading_no_wifi(instance_robot)
            case 'screen_wifi_connection_select':
                screen_wifi_connection_select(instance_robot)
            case 'screen_wifi_connection_password':
                screen_wifi_connection_password(instance_robot)
            
    
    pygame.quit()

def screen_loading_init(instance_robot):
        
    screen = instance_robot.window
    color_background = instance_robot.color_background
    largeur_screen = instance_robot.largeur
    hauteur_screen = instance_robot.hauteur
    
    image = pygame.image.load("/home/raspberry/Desktop/Projet Vikki/img/Logo.png")
    coord_largeur_center_img = (largeur_screen//2) - (image.get_width()//2)
    coord_hauteur_center_img = (hauteur_screen//2) - (image.get_height()//2)
    
    while  instance_robot.active_window == 'screen_loading_init':
        #MATH animation
        
        screen.fill(color_background)
        screen.blit(image, (coord_largeur_center_img,coord_hauteur_center_img))
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def screen_eye_watching(instance_robot):
    
    screen = instance_robot.window
    color_background = instance_robot.color_background
    largeur_screen = instance_robot.largeur
    hauteur_screen = instance_robot.hauteur
    
    equart_eye = instance_robot.equart_eye
    eye_color = instance_robot.eye_color
    v_eye = instance_robot.vitesse_eye
    
    center_screen_x = int(largeur_screen*(1/2))
    center_screen_y = int(hauteur_screen*(1/2))
    
    largeur_eye = int(largeur_screen*(1/8))
    hauteur_eye = int(hauteur_screen*(2/3))
    
    largeur_eye_iris = int(largeur_eye*(2/3))
    hauteur_eye_iris = int(hauteur_eye*(2/3))
    
    x_eye,y_eye = center_screen_x-int(largeur_eye*(1/2)),center_screen_y-int(hauteur_eye*(1/2))
    x_eye_iris,y_eye_iris = center_screen_x-int(largeur_eye_iris*(1/2)),center_screen_y-int(hauteur_eye_iris*(1/2))
    
    while instance_robot.active_window == 'screen_eye_watching':
        

        if (x_eye_iris+largeur_eye_iris < x_eye+largeur_eye and int(instance_robot.camera_face_pos_x*3)>x_eye_iris+largeur_eye_iris):
            x_eye_iris+=v_eye
            
        if (y_eye_iris+hauteur_eye_iris < y_eye+hauteur_eye and int(instance_robot.camera_face_pos_y*2.25)>y_eye_iris+hauteur_eye):
            y_eye_iris+=v_eye
        
        if (x_eye_iris>x_eye and int(instance_robot.camera_face_pos_x*3)<x_eye_iris):
            x_eye_iris-=v_eye
        
        if (y_eye_iris>y_eye and int(instance_robot.camera_face_pos_y*2.25)<y_eye_iris):
            y_eye_iris-=v_eye


        # Effacer l'écran
        screen.fill(color_background)

        # Dessiner l'objet animé (ici, un simple carré)
        pygame.draw.ellipse(screen, eye_color, (x_eye-int(equart_eye/2), y_eye,largeur_eye, hauteur_eye))
        pygame.draw.ellipse(screen, eye_color, (x_eye+int(equart_eye/2), y_eye,largeur_eye, hauteur_eye))
        
        pygame.draw.ellipse(screen, color_background, (x_eye_iris-int(equart_eye/2), y_eye_iris,largeur_eye_iris, hauteur_eye_iris))
        pygame.draw.ellipse(screen, color_background, (x_eye_iris+int(equart_eye/2), y_eye_iris,largeur_eye_iris, hauteur_eye_iris))

        
        # Mettre à jour l'affichage
        pygame.display.flip()

        # Contrôler la fréquence de rafraîchissement
        pygame.time.Clock().tick(60)


def screen_loading_wifi_connection(instance_robot):
        
    screen = instance_robot.window
    color_background = instance_robot.color_background
    largeur_screen = instance_robot.largeur
    hauteur_screen = instance_robot.hauteur
    
    image = pygame.image.load("/home/raspberry/Desktop/Projet Vikki/img/wifi.png")
    
    coord_largeur_center_img = (largeur_screen//2) - (image.get_width()//2)
    coord_hauteur_center_img = (hauteur_screen//2) - (image.get_height()//2)
    
    ball_x = largeur_screen//2
    ball_x2 = ball_x
    ball_y = hauteur_screen//2 +300
    
    vitesse_ball = 20
    
    while  instance_robot.active_window == 'screen_loading_wifi_connection':
        
        ball_x+=vitesse_ball
        ball_x2-=vitesse_ball
        
        if ball_x>int(largeur_screen*(4/7)) or ball_x<int(largeur_screen*(3/7)):
            vitesse_ball= -vitesse_ball

        
        screen.fill(color_background)
        screen.blit(image, (coord_largeur_center_img,coord_hauteur_center_img))
        
        
        pygame.draw.circle(screen, (4,10,170), (ball_x,ball_y),30)
        pygame.draw.circle(screen, (4,10,170), (ball_x2,ball_y),30)


        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
def screen_loading_no_wifi(instance_robot):
        
    screen = instance_robot.window
    color_background = instance_robot.color_background
    largeur_screen = instance_robot.largeur
    hauteur_screen = instance_robot.hauteur
    
    image = pygame.image.load("/home/raspberry/Desktop/Projet Vikki/img/no_wifi.png")
    
    coord_largeur_center_img = (largeur_screen//2) - (image.get_width()//2)
    coord_hauteur_center_img = (hauteur_screen//2) - (image.get_height()//2)
    
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = font.render('Pas de connexion internet', False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(largeur_screen/2, (hauteur_screen/2)-300))


    
    while  instance_robot.active_window == 'screen_loading_no_wifi':

        screen.fill(color_background)
        screen.blit(image, (coord_largeur_center_img,coord_hauteur_center_img))
        screen.blit(text_surface, text_rect)

        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
        
        
# Fonction pour créer un bouton
def draw_wifi_button(instance_robot,x, y, width, height, color, text, text_color):
    screen = instance_robot.window
    pygame.draw.rect(screen, color, (x, y, width, height))
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def screen_wifi_connection_select(instance_robot):
        
    screen = instance_robot.window
    color_background = instance_robot.color_background
    largeur_screen = instance_robot.largeur
    hauteur_screen = instance_robot.hauteur
    
    # Position et dimensions des boutons
    button_width = 300
    button_height = 75
    button_padding = 20
    
    list_wifi = instance_robot.list_wifi 

    # Calcul du nombre de boutons en fonction de la liste
    num_buttons = len(list_wifi)
        
    
    
    font = pygame.font.SysFont('Comic Sans MS', 40, True)
    text_surface = font.render('Selectionné un réseau Wifi pour connecter Vikki', False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(largeur_screen/2, 250))
    
    
    #TEST
    
    while  instance_robot.active_window == 'screen_wifi_connection_select':

        screen.fill(color_background)
        screen.blit(text_surface, text_rect)
        

        
        for event in pygame.event.get():
            # Vérifiez si un bouton est cliqué
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                for i in range(num_buttons):
                    button_x = (largeur_screen - button_width) // 2
                    button_y = (hauteur_screen - num_buttons * (button_height + button_padding)) // 2 + i * (button_height + button_padding)

                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        instance_robot.active_wifi = list_wifi[i]
                        instance_robot.active_window = 'screen_wifi_connection_password'
                        #print(f"Bouton {i + 1} cliqué: {list_wifi[i]}")
        
        # Dessinez les boutons
        for i in range(num_buttons):
            button_x = (screen.get_width() - button_width) // 2
            button_y = (screen.get_height() - num_buttons * (button_height + button_padding)) // 2 + i * (button_height + button_padding)
            draw_wifi_button(instance_robot,button_x, button_y, button_width, button_height, (4,10,170), list_wifi[i], (255,255,255))
            

        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def screen_wifi_connection_password(instance_robot):
        
    screen = instance_robot.window
    wifi = instance_robot.active_wifi
    color_background = instance_robot.color_background
    largeur_screen = instance_robot.largeur
    hauteur_screen = instance_robot.hauteur
    
    # Couleurs
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0,255,0)

    # Police de caractères
    font = pygame.font.Font(None, 40)

    # Texte d'en-tête
    header_text = "Saisie de Mot de Passe de : "+instance_robot.active_wifi
    header_surface = font.render(header_text, True, white)
    header_rect = header_surface.get_rect(center=(largeur_screen // 2, hauteur_screen // 6))

    # Champ de texte
    text_input_rect = pygame.Rect(largeur_screen // 4, hauteur_screen // 2 - 100, largeur_screen // 2, 60)
    text_input = ""

    # Liste des lettres du clavier
    keyboard_letters = "AZERTYUIOPQSDFGHJKLMWXCVBN"

    # Liste des caractères spéciaux
    special_characters = "!@#$%^&*()_-+=<>?"

    # Liste des chiffres
    numbers = "0123456789"

    # Position initiale des boutons du clavier
    button_size = 100
    button_padding = 10
    keyboard_buttons = []

    for i, letter in enumerate(numbers + keyboard_letters + special_characters):
        col = i % 10
        row = i // 10
        x = (button_size + button_padding) * col + (largeur_screen - (button_size + button_padding) * 10) // 2
        y = (button_size + button_padding) * row + hauteur_screen // 2 
        rect = pygame.Rect(x, y, button_size, button_size)
        keyboard_buttons.append((rect, letter))

    # Bouton "Caps"
    caps_lock_button_rect = pygame.Rect((largeur_screen - (button_size + button_padding) * 10) // 2 - (button_size + button_padding) - 25,
                                        hauteur_screen // 2 + 60, button_size+25, button_size)
    keyboard_buttons.append((caps_lock_button_rect, "Caps"))

    # Bouton de validation
    validate_button_rect = pygame.Rect(text_input_rect.right + button_padding, text_input_rect.top, 100, text_input_rect.height)

    # Position initiale du bouton "Supp"
    delete_button_rect = pygame.Rect(
        (largeur_screen + (button_size + button_padding) * 10) // 2 ,
        hauteur_screen // 2 + 60,
        button_size+25,
        button_size
    )
    keyboard_buttons.append((delete_button_rect, "Supp"))


    # Variable pour suivre l'état du clavier (majuscules ou minuscules)
    caps_lock = False

    # Boucle principale
    while instance_robot.active_window == 'screen_wifi_connection_password':
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Vérifiez si le clic est dans un bouton du clavier
                    for rect, letter in keyboard_buttons:
                        if rect.collidepoint(event.pos):
                            if letter == "Caps":
                                # Basculez l'état des majuscules
                                caps_lock = not caps_lock
                            elif letter == "Supp":
                                # Supprimez le dernier caractère
                                text_input = text_input[:-1]
                            else:
                                # Mettez à jour le texte en fonction de l'état des majuscules
                                if caps_lock:
                                    text_input += letter.upper()
                                else:
                                    text_input += letter.lower()

                    # Vérifiez si le clic est dans le bouton de validation
                    if validate_button_rect.collidepoint(event.pos):
                        print("Mot de passe saisi :", text_input)
                        instance_robot.active_wifi_password = text_input
                        text_input = ""

        # Affichage
        screen.fill(black)
        screen.blit(header_surface, header_rect)
        pygame.draw.rect(screen, white, text_input_rect, 2)

        # Affichage du texte dans le champ de texte
        input_surface = font.render(text_input, True, white)
        input_rect = input_surface.get_rect(midleft=(text_input_rect.left + 5, text_input_rect.centery))
        
        gap = 0
        while input_rect.width+gap > text_input_rect.width:
            gap+=5
            input_surface = font.render(text_input[gap:], True, white)
            input_rect = input_surface.get_rect(midleft=(text_input_rect.left + 5, text_input_rect.centery))
        screen.blit(input_surface, input_rect)


        # Affichage des boutons du clavier
        for rect, letter in keyboard_buttons:
            if letter == "Caps" and caps_lock:
                pygame.draw.rect(screen, (0, 0, 255), rect, 2)  # Mettre en bleu si les majuscules sont activées
            else:
                pygame.draw.rect(screen, white, rect, 2)
            letter_surface = font.render(letter, True, white)
            letter_rect = letter_surface.get_rect(center=rect.center)
            screen.blit(letter_surface, letter_rect)

        # Affichage du bouton de validation
        pygame.draw.rect(screen, white, validate_button_rect, 2)
        validate_text_surface = font.render("Valider", True, green)
        validate_text_rect = validate_text_surface.get_rect(center=validate_button_rect.center)
        screen.blit(validate_text_surface, validate_text_rect)

        pygame.display.flip()
