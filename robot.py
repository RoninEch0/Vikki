import yaml

class Robot():
    def __init__(self):
        
        with open('config.yaml', 'r') as fichier_yaml:
            configuration = yaml.safe_load(fichier_yaml)
        
        #PIN MOTEUR
        self.motor_right_1 = configuration['pin']['motor_right_1']
        self.motor_right_2 = configuration['pin']['motor_right_2']
        self.motor_left_3 = configuration['pin']['motor_left_3']
        self.motor_left_4 = configuration['pin']['motor_left_4']
        
        #ECRAN
        self.title_caption = configuration['screen']['title_caption']
        self.largeur = configuration['screen']['largeur']
        self.hauteur = configuration['screen']['hauteur']
        self.fullscreen = configuration['screen']['fullscreen']
        self.color_background = (configuration['screen']['color_background_r'],configuration['screen']['color_background_g'],configuration['screen']['color_background_b'])
        self.window = None
        
        #EYE ROBOT
        self.equart_eye = configuration['eye']['equart_eye']
        self.vitesse_eye = configuration['eye']['vitesse_eye']
        self.eye_color = (configuration['eye']['eye_color_r'],configuration['eye']['eye_color_g'],configuration['eye']['eye_color_b'])
        
        #CAMERA
        self.camera_largeur = 640
        self.camera_hauteur = 480
        self.camera_face_pos_x = 640//2
        self.camera_face_pos_y = 480//2
        
        #INTERNET
        self.list_wifi = []        
        
        #RUNNING PARAMETER
        #écran :
        self.active_window = ''
        self.active_camera = False
        
        #internet :
        self.active_wifi = ''
        self.active_wifi_password = ''
        
        #microphone (STT et TTS)
        self.active_vc = False
        
        
        

        
"""             
test = Robot()
print(Robot.get_param(test,'window'))
Robot.update_param(test,'window','its working')
print(Robot.get_param(test,'window'))
"""
