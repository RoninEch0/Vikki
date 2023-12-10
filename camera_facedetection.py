import cv2

def camera_face_detection(instance_robot):
    # Charger le classifieur de visage pré-entraîné
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Utiliser la webcam (index 0 par défaut, changez-le si vous avez plusieurs caméras)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    instance_robot.camera_largeur = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    instance_robot.camera_hauteur = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(instance_robot.camera_hauteur)
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

