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
        self.capture.release()
        cv2.destroyAllWindows()
    

