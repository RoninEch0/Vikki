
import threading
import time
import DFRobot_BloodOxygen_S

class Medical_Sensor:
    def __init__(self):
        self.I2C_1 = 0x01
        self.I2C_ADDRESS = 0x57
        self.max30102 = DFRobot_BloodOxygen_S.DFRobot_BloodOxygen_S_i2c(self.I2C_1 ,self.I2C_ADDRESS)
        self.spo2 = 0
        self.bpm = 0
        self.list_spo2=[]
        self.list_bpm=[]
        self.thread_medical_sensor=threading.Thread(target=self.medical_sensor_run)
        self.active_medical_sensor = False
    
    def thread_medical_sensor_start(self):
        self.active_medical_sensor=True
        self.thread_medical_sensor.start()
        
    def thread_medical_sensor_stop(self):
        self.active_medical_sensor=False
        self.thread_medical_sensor.join()
    
    def get_bpm_spo2(self):
        return({'bpm':self.list_bpm,'spo2':self.list_spo2})
    
    def medical_sensor_run(self):
        self.list_spo2=[]
        self.list_bpm=[]
        while (False == self.max30102.begin()):
            time.sleep(1)
        self.max30102.sensor_start_collect()
        time.sleep(1)
        while self.active_medical_sensor:
            self.max30102.get_heartbeat_SPO2()
            self.spo2=self.max30102.SPO2
            self.bpm=self.max30102.heartbeat
            if self.spo2!=-1:
                self.list_spo2.append(self.spo2)
            if self.bpm!=-1:
                self.list_bpm.append(self.bpm)
            time.sleep(1)
        self.max30102.sensor_end_collect()
