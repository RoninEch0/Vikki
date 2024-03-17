import serial
from CalcLidarData import CalcLidarData
import math
import threading


class Lidar:
    def __init__(self):
        self.ser=serial.Serial(port="/dev/ttyUSB0",baudrate=230400,timeout=5.0,bytesize=8,parity='N',stopbits=1)
        self.tmp_string = ""
        self.thread_lidar=threading.Thread(target=self.lidar_run)
        self.active_lidar = False
        self.data_lidar_list=[[],[]]
    
    def thread_lidar_start(self):
        self.active_lidar=True
        self.thread_lidar.start()
        
    def thread_lidar_stop(self):
        self.active_lidar=False
        self.thread_lidar.join()
    
    def get_data_lidar_list(self):
        return self.data_lidar_list
        
    
    def lidar_run(self):
        angles = []
        distances = []
        temp_data_lidar_list=[[],[]]
        self.data_lidar_list=[[],[]]
        while self.active_lidar:
            loopFlag = True
            flag2c = False
            while loopFlag:
                b = self.ser.read()
                tmpInt = int.from_bytes(b, 'big')
                if (tmpInt == 0x54):
                    self.tmp_string += b.hex() + " "
                    flag2c = True
                    continue
                elif (tmpInt == 0x2c and flag2c):
                    self.tmp_string += b.hex()
                    if (not len(self.tmp_string[0:-5].replace(' ','')) == 90):
                        self.tmp_string = ""
                        loopFlag = False
                        flag2c = False
                        continue
                    lidarData = CalcLidarData(self.tmp_string[0:-5])
                    angles = lidarData.Angle_i
                    distances = lidarData.Distance_i
                    for data_index in range (len(angles)):
                        if angles[data_index]<=0.01:
                            self.data_lidar_list = temp_data_lidar_list
                            temp_data_lidar_list=[[],[]]
                        temp_data_lidar_list[0].append(angles[data_index])
                        temp_data_lidar_list[1].append(distances[data_index])
                    self.tmp_string = ""
                    loopFlag = False
                else:
                    self.tmp_string += b.hex()+ " "
                flag2c = False
