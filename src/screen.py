import pygame
import threading


class Screen:
    def __init__(self,config_screen):
        self.title_caption = config_screen['title_caption']
        self.width = config_screen['width']
        self.height = config_screen['height']
        self.fullscreen = config_screen['fullscreen']
        self.color_background = (config_screen['color_background_r'],config_screen['color_background_g'],config_screen['color_background_b'])
        
        self.eye_padding=config_screen['eye_padding']
        self.eye_speed=config_screen['eye_speed']
        self.eye_color=(config_screen['eye_color_r'],config_screen['eye_color_g'],config_screen['eye_color_b'])
        
        self.iris_eye_pos=[self.width//2,self.height//2]
        self.window = None
        self.active_window = 'screen_loading_init'
        self.thread_screen=threading.Thread(target=self.screen_manager)
        
        self.list_wifi=[]
        self.selected_wifi_name=""
        self.selected_wifi_password=""
    
    def set_active_window(self,value):
        self.active_window=value
        
    def set_list_wifi(self,value):
        self.list_wifi=value
    
    def get_selected_wifi_name(self)->str:
        return(self.selected_wifi_name)
    
    def set_selected_wifi_name(self,value):
        self.selected_wifi_name=value
    
    def get_selected_wifi_password(self)->str:
        return(self.selected_wifi_password)
    
    def set_selected_wifi_password(self,value):
        self.selected_wifi_password=value
        
    def set_iris_eye_pos(self,value):
        self.iris_eye_pos=value
    
    
    def thread_screen_start(self):
        self.thread_screen.start()
        
    def thread_screen_stop(self):
        self.active_window = None
        self.thread_screen.join()
            
    def screen_manager(self):
        pygame.init()
        
        if self.fullscreen:
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title_caption)
        
        while self.active_window != None:
            match self.active_window:
                case 'screen_loading_init':  
                    self.screen_loading_init()
                case 'screen_loading_wifi':  
                    self.screen_loading_wifi()
                case 'screen_loading_no_wifi':
                    self.screen_loading_no_wifi()
                case 'screen_loading_wifi_valid':
                    self.screen_loading_wifi_valid()
                case 'screen_wifi_connection_select':
                    self.screen_wifi_connection_select()
                case 'screen_wifi_connection_password':
                    self.screen_wifi_connection_password()
                case 'screen_eye_watching':
                    self.screen_eye_watching()
        pygame.quit()
        
    
    def screen_loading_init(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/Logo.png")
        coord_largeur_center_img = (self.width//2) - (img.get_width()//2)
        coord_hauteur_center_img = (self.height//2) - (img.get_height()//2)
        
        while  self.active_window == 'screen_loading_init':
        
            self.window.fill(self.color_background)
            self.window.blit(img, (coord_largeur_center_img,coord_hauteur_center_img))
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def screen_loading_wifi(self):  
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/wifi.png")
        coord_largeur_center_img = (self.width//2) - (img.get_width()//2)
        coord_hauteur_center_img = (self.height//2) - (img.get_height()//2)
        ball_x = self.width//2
        ball_x2 = ball_x
        ball_y =self.height//2 +300
        
        ball_speed = 20
        
        while  self.active_window == 'screen_loading_wifi':
            
            ball_x+=ball_speed
            ball_x2-=ball_speed
            
            if ball_x>int(self.width*(4/7)) or ball_x<int(self.width*(3/7)):
                ball_speed= -ball_speed

            self.window.fill(self.color_background)
            self.window.blit(img, (coord_largeur_center_img,coord_hauteur_center_img))
            
            pygame.draw.circle(self.window, (4,10,170), (ball_x,ball_y),30)
            pygame.draw.circle(self.window, (4,10,170), (ball_x2,ball_y),30)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def screen_loading_no_wifi(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/no_wifi.png")
        coord_largeur_center_img = (self.width//2) - (img.get_width()//2)
        coord_hauteur_center_img = (self.height//2) - (img.get_height()//2)
        
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = font.render('Pas de connexion internet', False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width/2, (self.height/2)-300))

        while  self.active_window == 'screen_loading_no_wifi':

            self.window.fill(self.color_background)
            self.window.blit(img, (coord_largeur_center_img,coord_hauteur_center_img))
            self.window.blit(text_surface, text_rect)

            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def screen_loading_wifi_valid(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/wifi_valid.png")
        coord_largeur_center_img = (self.width//2) - (img.get_width()//2)
        coord_hauteur_center_img = (self.height//2) - (img.get_height()//2)
        
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = font.render('Connexion  internet : OK', False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width/2, (self.height/2)-300))

        while  self.active_window == 'screen_loading_wifi_valid':

            self.window.fill(self.color_background)
            self.window.blit(img, (coord_largeur_center_img,coord_hauteur_center_img))
            self.window.blit(text_surface, text_rect)

            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def screen_wifi_connection_select(self):

        button_width = 300
        button_height = 75
        button_padding = 20
        
        num_buttons = len(self.list_wifi)
        
        font = pygame.font.SysFont('Comic Sans MS', 40, True)
        text_surface = font.render('Selectionne un reseau Wifi pour connecter Vikki', False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width//2, 250))
        

        while  self.active_window == 'screen_wifi_connection_select':

            self.window.fill(self.color_background)
            self.window.blit(text_surface, text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    for i in range(num_buttons):
                        button_x = (self.width - button_width) // 2
                        button_y = (self.height - num_buttons * (button_height + button_padding)) // 2 + i * (button_height + button_padding)

                        if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                            self.selected_wifi_name = self.list_wifi[i]
                            self.active_window = 'screen_wifi_connection_password'
            
            for i in range(num_buttons):
                button_x = (self.width - button_width) // 2
                button_y = (self.height - num_buttons * (button_height + button_padding)) // 2 + i * (button_height + button_padding)
                pygame.draw.rect(self.window, (4,10,170), (button_x, button_y,  button_width, button_height))
    
                font = pygame.font.Font(None, 36)
                text_surface1 = font.render(self.list_wifi[i], True, (255, 255, 255))
                text_rect1 = text_surface1.get_rect(center=(button_x +  button_width // 2, button_y + button_height // 2))
                self.window.blit(text_surface1, text_rect1)
                

            
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def screen_wifi_connection_password(self):
        
        # Couleurs
        white = (255, 255, 255)
        black = (0, 0, 0)
        green = (0,255,0)

        # Police de caractères
        font = pygame.font.Font(None, 40)

        # Texte d'en-tête
        header_text = "Saisie de Mot de Passe de : "+self.selected_wifi_name
        header_surface = font.render(header_text, True, white)
        header_rect = header_surface.get_rect(center=(self.width // 2, self.height // 6))

        # Champ de texte
        text_input_rect = pygame.Rect(self.width // 4, self.height // 2 - 100, self.width // 2, 60)
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
            x = (button_size + button_padding) * col + (self.width - (button_size + button_padding) * 10) // 2
            y = (button_size + button_padding) * row + self.height // 2 
            rect = pygame.Rect(x, y, button_size, button_size)
            keyboard_buttons.append((rect, letter))

        # Bouton "Caps"
        caps_lock_button_rect = pygame.Rect((self.width - (button_size + button_padding) * 10) // 2 - (button_size + button_padding) - 25,
                                            self.height // 2 + 60, button_size+25, button_size)
        keyboard_buttons.append((caps_lock_button_rect, "Caps"))

        # Bouton de validation
        validate_button_rect = pygame.Rect(text_input_rect.right + button_padding, text_input_rect.top, 100, text_input_rect.height)

        # Position initiale du bouton "Supp"
        delete_button_rect = pygame.Rect(
            (self.width + (button_size + button_padding) * 10) // 2 ,
            self.height // 2 + 60,
            button_size+25,
            button_size
        )
        keyboard_buttons.append((delete_button_rect, "Supp"))


        # Variable pour suivre l'état du clavier (majuscules ou minuscules)
        caps_lock = False

        # Boucle principale
        while self.active_window == 'screen_wifi_connection_password':
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
                            self.selected_wifi_password = text_input
                            text_input = ""

            # Affichage
            self.window.fill(black)
            self.window.blit(header_surface, header_rect)
            pygame.draw.rect(self.window, white, text_input_rect, 2)

            # Affichage du texte dans le champ de texte
            input_surface = font.render(text_input, True, white)
            input_rect = input_surface.get_rect(midleft=(text_input_rect.left + 5, text_input_rect.centery))
            
            gap = 0
            while input_rect.width+gap > text_input_rect.width:
                gap+=5
                input_surface = font.render(text_input[gap:], True, white)
                input_rect = input_surface.get_rect(midleft=(text_input_rect.left + 5, text_input_rect.centery))
            self.window.blit(input_surface, input_rect)


            # Affichage des boutons du clavier
            for rect, letter in keyboard_buttons:
                if letter == "Caps" and caps_lock:
                    pygame.draw.rect(self.window, (0, 0, 255), rect, 2)  # Mettre en bleu si les majuscules sont activées
                else:
                    pygame.draw.rect(self.window, white, rect, 2)
                letter_surface = font.render(letter, True, white)
                letter_rect = letter_surface.get_rect(center=rect.center)
                self.window.blit(letter_surface, letter_rect)

            # Affichage du bouton de validation
            pygame.draw.rect(self.window, white, validate_button_rect, 2)
            validate_text_surface = font.render("Valider", True, green)
            validate_text_rect = validate_text_surface.get_rect(center=validate_button_rect.center)
            self.window.blit(validate_text_surface, validate_text_rect)

            pygame.display.flip()
    
    def screen_eye_watching(self):
        
        center_screen_x = int(self.width*(1/2))
        center_screen_y = int(self.height*(1/2))
        
        largeur_eye = int(self.width*(1/8))
        hauteur_eye = int(self.height*(2/3))
        
        largeur_eye_iris = int(largeur_eye*(2/3))
        hauteur_eye_iris = int(hauteur_eye*(2/3))
        
        x_eye,y_eye = center_screen_x-int(largeur_eye*(1/2)),center_screen_y-int(hauteur_eye*(1/2))
        x_eye_iris,y_eye_iris = center_screen_x-int(largeur_eye_iris*(1/2)),center_screen_y-int(hauteur_eye_iris*(1/2))
        
        while self.active_window == 'screen_eye_watching':
            
            if any(self.iris_eye_pos):
                if (x_eye_iris+largeur_eye_iris < x_eye+largeur_eye and self.iris_eye_pos[0]>x_eye_iris+largeur_eye_iris):
                    x_eye_iris+=self.eye_speed
                    
                if (y_eye_iris+hauteur_eye_iris < y_eye+hauteur_eye and self.iris_eye_pos[1]>y_eye_iris+hauteur_eye):
                    y_eye_iris+=self.eye_speed
                
                if (x_eye_iris>x_eye and self.iris_eye_pos[0]<x_eye_iris):
                    x_eye_iris-=self.eye_speed
                
                if (y_eye_iris>y_eye and self.iris_eye_pos[1]<y_eye_iris):
                    y_eye_iris-=self.eye_speed
            

            # Effacer l'écran
            self.window.fill(self.color_background)

            # Dessiner l'objet animé (ici, un simple carré)
            pygame.draw.ellipse(self.window, self.eye_color, (x_eye-int(self.eye_padding/2), y_eye,largeur_eye, hauteur_eye))
            pygame.draw.ellipse(self.window, self.eye_color, (x_eye+int(self.eye_padding/2), y_eye,largeur_eye, hauteur_eye))
            
            pygame.draw.ellipse(self.window, self.color_background, (x_eye_iris-int(self.eye_padding/2), y_eye_iris,largeur_eye_iris, hauteur_eye_iris))
            pygame.draw.ellipse(self.window, self.color_background, (x_eye_iris+int(self.eye_padding/2), y_eye_iris,largeur_eye_iris, hauteur_eye_iris))

            
            # Mettre à jour l'affichage
            pygame.display.flip()

            # Contrôler la fréquence de rafraîchissement
            pygame.time.Clock().tick(60)
