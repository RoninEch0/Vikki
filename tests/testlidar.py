import serial
import struct
import time

# D�finition du port s�rie
ser = serial.Serial('/dev/ttyUSB0', 230400, timeout=1)

# D�finition des constantes
POINT_PER_PACK = 12
HEADER = 0x54

# Structure de donn�es pour un point Lidar
class LidarPointStructDef:
    def __init__(self, distance, intensity):
        self.distance = distance
        self.intensity = intensity

# Structure de donn�es pour un paquet Lidar complet
class LiDARFrameTypeDef:
    def __init__(self, header, ver_len, speed, start_angle, points, end_angle, timestamp, crc8):
        self.header = header
        self.ver_len = ver_len
        self.speed = speed
        self.start_angle = start_angle
        self.points = points
        self.end_angle = end_angle
        self.timestamp = timestamp
        self.crc8 = crc8

# Fonction de calcul du CRC8
def cal_crc8(data):
    crc = 0
    for byte in data:
        crc = CrcTable[(crc ^ byte) & 0xff]
    return crc

CrcTable = [
    0x00, 0x4d, 0x9a, 0xd7, 0x79, 0x34, 0xe3, 0xae, 0xf2, 0xbf, 0x68, 0x25, 0x8b, 0xc6, 0x11, 0x5c,
    0xa9, 0xe4, 0x33, 0x7e, 0xd0, 0x9d, 0x4a, 0x07, 0x5b, 0x16, 0xc1, 0x8c, 0x22, 0x6f, 0xb8, 0xf5,
    0x1f, 0x52, 0x85, 0xc8, 0x66, 0x2b, 0xfc, 0xb1, 0xed, 0xa0, 0x77, 0x3a, 0x94, 0xd9, 0x0e, 0x43,
    0xb6, 0xfb, 0x2c, 0x61, 0xcf, 0x82, 0x55, 0x18, 0x44, 0x09, 0xde, 0x93, 0x3d, 0x70, 0xa7, 0xea,
    0x3e, 0x73, 0xa4, 0xe9, 0x47, 0x0a, 0xdd, 0x90, 0xcc, 0x81, 0x56, 0x1b, 0xb5, 0xf8, 0x2f, 0x62,
    0x97, 0xda, 0x0d, 0x40, 0xee, 0xa3, 0x74, 0x39, 0x65, 0x28, 0xff, 0xb2, 0x1c, 0x51, 0x86, 0xcb,
    0x21, 0x6c, 0xbb, 0xf6, 0x58, 0x15, 0xc2, 0x8f, 0xd3, 0x9e, 0x49, 0x04, 0xaa, 0xe7, 0x30, 0x7d,
    0x88, 0xc5, 0x12, 0x5f, 0xf1, 0xbc, 0x6b, 0x26, 0x7a, 0x37, 0xe0, 0xad, 0x03, 0x4e, 0x99, 0xd4,
    0x7c, 0x31, 0xe6, 0xab, 0x05, 0x48, 0x9f, 0xd2, 0x8e, 0xc3, 0x14, 0x59, 0xf7, 0xba, 0x6d, 0x20,
    0xd5, 0x98, 0x4f, 0x02, 0xac, 0xe1, 0x36, 0x7b, 0x27, 0x6a, 0xbd, 0xf0, 0x5e, 0x13, 0xc4, 0x89,
    0x63, 0x2e, 0xf9, 0xb4, 0x1a, 0x57, 0x80, 0xcd, 0x91, 0xdc, 0x0b, 0x46, 0xe8, 0xa5, 0x72
]

try:
    if ser.isOpen():
        print("Port s�rie ouvert avec succ�s.")
        
        # Vider le tampon de r�ception
        ser.flushInput()

        while True:
            # Lecture des 26 octets d'un paquet Lidar
            data = ser.read(26)
            print(data)
            print(len(data))
            if len(data) == 26 and data[0] == HEADER:
                # D�ballage des donn�es selon la structure d�finie
                frame = LiDARFrameTypeDef(*struct.unpack('!BBHH' + 'HHB' * POINT_PER_PACK + 'HHB', data))

                # V�rification du CRC
                data_for_crc = data[:-1]
                if cal_crc8(data_for_crc) == frame.crc8:
                    print("Paquet Lidar valide:")
                    print("  Speed:", frame.speed, "degrees per second")
                    print("  Start angle:", frame.start_angle / 100.0, "degrees")
                    print("  End angle:", frame.end_angle / 100.0, "degrees")
                    print("  Timestamp:", frame.timestamp, "milliseconds")

                    # Traitement des points Lidar
                    for i, point in enumerate(frame.points):
                        print(f"  Point {i + 1}: Distance: {point.distance}mm, Intensity: {point.intensity}")
                else:
                    print("CRC invalide. Paquet Lidar corrompu.")
                
            time.sleep(0.1)
            
except serial.SerialException as e:
    print("Erreur lors de l'ouverture du port s�rie:", e)
finally:
    ser.close()
    print("Port s�rie ferm�.")
