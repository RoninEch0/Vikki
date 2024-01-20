import cv2
import threading


class Camera:
    def __init__(self):
        self.capture=cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        
        self.width_cam=int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height_cam=int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.face_detection_file=cv2.CascadeClassifier('/home/raspberry/Desktop/Projet_Vikki/assets/haarcascade_frontalface_default.xml')
        self.thread_camera=threading.Thread(target=self.camera_run)
        self.active_camera=False
        self.active_detection_face=True
        self.face_detected=[]
        
    def get_face_detected(self):
        return self.face_detected

    
    def thread_camera_start(self):
        self.active_camera=True
        self.thread_camera.start()
        
    def thread_camera_stop(self):
        self.active_camera=False
        self.thread_camera.join()
    
    def camera_run(self):
        while self.active_camera:
            ret, frame = self.capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.active_detection_face:
                faces = self.face_detection_file.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))            
                if len(faces)>0:
                    self.face_detected=[self.width_cam-faces[0][0]-(faces[0][2]//2),faces[0][1]+(faces[0][3]//2)]
                    print(self.face_detected)
        self.capture.release()
        cv2.destroyAllWindows()
    

def camera_face_detection(instance_robot):
    # Charger le classifieur de visage pré-entraîné
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Utiliser la webcam (index 0 par défaut, changez-le si vous avez plusieurs caméras)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    instance_robot.camera_largeur = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    instance_robot.camera_hauteur = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    while instance_robot.active_camera:
        # Lire la frame depuis la webcam
        ret, frame = cap.read()

        # Convertir l'image en niveaux de gris pour la détection de visages
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détecter les visages dans l'image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        try :
            instance_robot.camera_face_pos_x = instance_robot.camera_largeur-faces[0][0]-(faces[0][2]//2)
            instance_robot.camera_face_pos_y = faces[0][1]+(faces[0][3]//2)
        except:
            pass

    # Libérer la webcam et fermer la fenêtre
    cap.release()
    cv2.destroyAllWindows()