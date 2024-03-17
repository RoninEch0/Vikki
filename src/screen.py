import pygame
import threading
import random
import time

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
        
        self.score_analyse=0
        
        self.spo2=-1
        self.bpm=-1
    
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
        
    def get_score_analyse(self):
        value=self.score_analyse
        self.score_analyse=0
        return(value)
    
    def set_bpm_spo2(self,new_value_bpm,new_value_spo2):
        self.spo2=new_value_spo2
        self.bpm=new_value_bpm
        
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
                case 'analyse_score_question':
                    self.analyse_score_question()
                case 'analyse_vital':
                    self.analyse_vital()
                case 'analyse_vital_value':
                    self.analyse_vital_value()
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
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/Logo.png")
        coord_largeur_center_img = (self.width//2) - (img.get_width()//2)
        coord_hauteur_center_img = (self.height//2) - (img.get_height()//2)
        
        img_loading = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/loading.png")
        rotation_speed = 10
        angle = 0

        while  self.active_window == 'screen_loading_wifi':
            
            rotated_image = pygame.transform.rotate(img_loading, angle)
            new_rect = rotated_image.get_rect(center = img_loading.get_rect(center = (960, 810)).center)
            
            if angle<=0:
                angle=360
            angle -= rotation_speed
        
            self.window.fill(self.color_background)
            self.window.blit(img, (coord_largeur_center_img,coord_hauteur_center_img))
            
            self.window.blit(rotated_image, new_rect)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def screen_loading_no_wifi(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/no_wifi.png")
        img = pygame.transform.scale(img,(1920,1080))
        while  self.active_window == 'screen_loading_no_wifi':

            self.window.fill(self.color_background)
            self.window.blit(img, (0,0))
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def screen_loading_wifi_valid(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/wifi_valid.png")
        resized_image = pygame.transform.scale(img, (1920, 1080))
        
        while  self.active_window == 'screen_loading_wifi_valid':

            self.window.fill(self.color_background)
            self.window.blit(resized_image, (0,0))
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def screen_wifi_connection_select(self):

        button_width = 300
        button_height = 75
        button_padding = 20
                
        num_buttons = len(self.list_wifi)
        
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/wifi_select.png")
        resized_image = pygame.transform.scale(img, (1920, 1080))
        font = pygame.font.SysFont('Roobert-Regular', 40, True)
        
        
        while  self.active_window == 'screen_wifi_connection_select':

            self.window.fill(self.color_background)
            self.window.blit(resized_image, (0,0))
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    for i in range(num_buttons):
                        button_x = (self.width - button_width) // 2
                        button_y = (self.height - num_buttons * (button_height + button_padding)) // 2 + i * (button_height + button_padding) + 150

                        if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                            self.selected_wifi_name = self.list_wifi[i]
                            self.active_window = 'screen_wifi_connection_password'
            
            for i in range(num_buttons):
                button_x = (self.width - button_width) // 2 
                button_y = (self.height - num_buttons * (button_height + button_padding)) // 2 + i * (button_height + button_padding) + 150
                pygame.draw.rect(self.window, (62,62,62), (button_x, button_y,  button_width, button_height))
    
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
        
        img_bg = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/wifi_password.png")
        resized_image = pygame.transform.scale(img_bg, (1920, 1080))
        img_button=pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/button.png")
        img_button = pygame.transform.scale(img_button, (110,80))
        img_validate=pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/validate_button.png")
        img_validate = pygame.transform.scale(img_validate, (250, 100))
        img_little=pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/little_button.png")
        img_little = pygame.transform.scale(img_little, (80,80))


        # Police de caractères
        font_header = pygame.font.SysFont('Roobert-Regular', 80, True)
        font = pygame.font.SysFont('Roobert-Regular', 40, True)
        
        # Texte d'en-tête
        header_text = self.selected_wifi_name
        header_surface = font_header.render(header_text, True, white)
        header_rect = header_surface.get_rect(center=(1200, 165))

        # Champ de texte
        text_input_rect = pygame.Rect(610,425,600, 60)
        text_input = ""

        # Liste des lettres du clavier
        keyboard_letters = "AZERTYUIOPQSDFGHJKLMWXCVBN"

        # Liste des caractères spéciaux
        special_characters = "!@#$%^&*()_-+=<>?"

        # Liste des chiffres
        numbers = "0123456789"

        # Position initiale des boutons du clavier
        button_size = 80
        button_padding = 5
        keyboard_buttons = []

        for i, letter in enumerate(numbers + keyboard_letters + special_characters):
            col = i % 10
            row = i // 10
            x = (button_size + button_padding) * col + (self.width - (button_size + button_padding) * 10) // 2
            y = (button_size + button_padding) * row + self.height // 2 + 25
            rect = pygame.Rect(x, y, button_size, button_size)
            keyboard_buttons.append((rect, letter))

        # Bouton "Caps"
        caps_lock_button_rect = pygame.Rect((self.width - (button_size + button_padding) * 10) // 2 - (button_size + button_padding) - 25,
                                            self.height // 2 + 60, button_size+25, button_size)
        keyboard_buttons.append((caps_lock_button_rect, "Caps"))

        # Bouton de validation
        validate_button_rect = pygame.Rect(text_input_rect.right + button_padding +25, text_input_rect.top-20, 250, text_input_rect.height+40)
        validate_button_rect2 = pygame.Rect(text_input_rect.right + button_padding +100, text_input_rect.top, 100, text_input_rect.height)

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
                            print("validate")
                            text_input = ""

            # Affichage
            self.window.fill(self.color_background)
            self.window.blit(resized_image, (0,0))

            self.window.blit(header_surface, header_rect)

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
                letter_surface = font.render(letter, True, self.color_background)
                if letter == "Caps" and caps_lock:
                    letter_surface = font.render(letter, True, (2, 171, 171))
                    self.window.blit(img_button, rect)
                elif letter == "Caps" or letter == "Supp":
                    self.window.blit(img_button, rect)
                else :
                    self.window.blit(img_little, rect)

                

                letter_rect = letter_surface.get_rect(center=rect.center)
                self.window.blit(letter_surface, letter_rect)
                

            # Affichage du bouton de validation
            self.window.blit(img_validate, validate_button_rect)
            validate_text_surface = font.render("Valider", True, (255, 255, 255))
            validate_text_rect = validate_text_surface.get_rect(center=validate_button_rect2.center)
            self.window.blit(validate_text_surface, validate_text_rect)

            pygame.display.flip()
    
    
    def screen_eye_watching(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/eye.png")
        img2 = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/eye2.png")
        
        
        center_screen_x = int(self.width*(1/2))
        center_screen_y = int(self.height*(1/2))
        
        refresh = 0
        is_eye_close = False
        
        current_x_pos=center_screen_x
        current_y_pos=center_screen_y
        
        img_eye=img
        
        while self.active_window == 'screen_eye_watching':
            
            refresh +=1
            if is_eye_close and refresh>5:
                is_eye_close=False
                img_eye=img
                refresh=0
            if is_eye_close == False and refresh>40:
                is_eye_close=True
                img_eye=img2
                refresh=0

                
            largeur_eye = img_eye.get_width()
            hauteur_eye = img_eye.get_height()
            
            if any(self.iris_eye_pos):
                if current_x_pos<self.iris_eye_pos[0] and current_x_pos+largeur_eye//2 <= 1770:
                    current_x_pos+=self.eye_speed
                if current_x_pos>self.iris_eye_pos[0] and current_x_pos-largeur_eye//2 >= 150:
                    current_x_pos-=self.eye_speed
                if current_y_pos<self.iris_eye_pos[1] and current_y_pos+hauteur_eye//2 <= 1080:
                    current_y_pos+=self.eye_speed
                if current_y_pos>self.iris_eye_pos[1] and current_y_pos-hauteur_eye//2 >= 0:
                    current_y_pos-=self.eye_speed

            self.window.fill(self.color_background)
            self.window.blit(img_eye, (current_x_pos-largeur_eye//2, current_y_pos-hauteur_eye//2))
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def analyse_score_question(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/score_analyse.png")
        resized_image = pygame.transform.scale(img, (1920, 1080))
        
        number_buttons=[]
        
        y = 578
        
        for i in range(10):
            x = i * 150 +230
            rect = pygame.Rect(x, y, 100, 100)
            number_buttons.append((rect,i+1))
        
        font = pygame.font.Font(None, 36)

        while  self.active_window == 'analyse_score_question':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for rect, num in number_buttons:
                            if rect.collidepoint(event.pos):
                                self.score_analyse=num

            self.window.fill(self.color_background)
            self.window.blit(resized_image, (0,0))
            for rect, num in number_buttons:
                pygame.draw.circle(self.window, (255,255,255), (rect[0]+50, rect[1]+50), 50)
                text = font.render(str(num), True, (30,30,30))
                text_rect = text.get_rect(center=(rect[0]+50,rect[1]+50))
                self.window.blit(text, text_rect)
            
            pygame.display.flip()
            
    def analyse_vital(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/analyse_vital.png")
        resized_image = pygame.transform.scale(img, (1920, 1080))

        
        while  self.active_window == 'analyse_vital':
        
            self.window.fill(self.color_background)
            self.window.blit(resized_image, (0,0))
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def analyse_vital_value(self):
        img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/analyse_vital_value.png")
        resized_image = pygame.transform.scale(img, (1920, 1080))
        
        heart_img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/heart.png")
        resized_heart_img = pygame.transform.scale(heart_img, (221, 195))
        lung_img = pygame.image.load("/home/raspberry/Desktop/Projet_Vikki/assets/lung.png")
        resized_lung_img = pygame.transform.scale(lung_img, (236, 216))

        
        self.spo2 = 100
        self.bpm = 100
        
        font = pygame.font.Font(None, 120)
        var_heart=1
        var_lung=1
        lung_bool=-1
        
        while  self.active_window == 'analyse_vital_value':
             

            
            if self.bpm == -1:
                text_bpm="???"
            else :
                text_bpm=self.bpm
                var_heart = var_heart-(0.05*(self.bpm/100))
                if var_heart<0.7:
                    var_heart=1
                resized_heart_img = pygame.transform.scale(heart_img, (int(221*var_heart), int(195*var_heart)))
            
            if self.spo2 == -1:
                text_spo2="???"
            else:
                text_spo2=self.spo2
                var_lung = var_lung+lung_bool*(0.05*(self.spo2/100))
                if var_lung<0.7 or var_lung>1:
                    lung_bool= -(lung_bool)
                resized_lung_img = pygame.transform.scale(lung_img, (int(236*var_lung), int(216*var_lung)))

            
            self.window.fill(self.color_background)
            self.window.blit(resized_image, (0,0))
            
            text = font.render(str(text_bpm), True, (255,255,255))
            self.window.blit(text, (640,520))
            
            text = font.render(str(text_spo2), True, (255,255,255))
            self.window.blit(text, (1140,520))
            
            self.window.blit(resized_heart_img, (264+((1-var_heart)*221)//2,442+((1-var_heart)*195)//2))
            self.window.blit(resized_lung_img, (1433+((1-var_lung)*236)//2,442+((1-var_lung)*216)//2))

            
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    