import yaml
import pygame
import threading


class Screen:
    def __init__(self,config_file):
        with open(config_file, 'r') as fichier_yaml:
            configuration = yaml.safe_load(fichier_yaml)
            self.title_caption = configuration['screen']['title_caption']
            self.width = configuration['screen']['largeur']
            self.height = configuration['screen']['hauteur']
            self.fullscreen = configuration['screen']['fullscreen']
            self.color_background = (configuration['screen']['color_background_r'],configuration['screen']['color_background_g'],configuration['screen']['color_background_b'])
        
        self.window = None
        self.active_window = 'screen_loading_init'
        self.thread_screen=threading.Thread(target=self.screen_manager)
    
    def set_active_window(self,value):
        self.active_window=value
    
    def thread_screen_start(self):
        self.thread_screen.start()
        
    def thread_screen_stop(self):
        self.set_active_window(None)
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
        pygame.quit()
        
    
    def screen_loading_init(self):
        
        img = pygame.image.load("/home/raspberry/Desktop/Projet Vikki/assets/Logo.png")
        coord_largeur_center_img = (self.width//2) - (img.get_width()//2)
        coord_hauteur_center_img = (self.height//2) - (img.get_height()//2)
        
        while  self.active_window == 'screen_loading_init':
        
            self.window.fill(self.color_background)
            self.window.blit(img, (coord_largeur_center_img,coord_hauteur_center_img))
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
