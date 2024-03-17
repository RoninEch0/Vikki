import serial
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math

fig = plt.figure(figsize=(8,8))


ax = fig.add_subplot(111, projection='polar')
ax.set_title('Lidar LD19 (exit: Key E)',fontsize=18)

com_port = "/dev/ttyUSB0"

plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

ser = serial.Serial(port=com_port,
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)
tmpString = ""
angles = list()
distances = list()

i = 0
while True:
    loopFlag = True
    flag2c = False
    if (i % 40 == 39):
        if ('line' in locals()):
            line.remove()
        line = ax.scatter(angles, distances, c="blue", s=5)
        ax.set_theta_offset(math.pi / 2)
        plt.pause(0.005)
        angles.clear()
        distances.clear()
        i = 0
    while loopFlag:
        b = ser.read()
        tmpInt = int.from_bytes(b, 'big')
        if (tmpInt == 0x54):
            tmpString += b.hex() + " "
            flag2c = True
            continue
        elif (tmpInt == 0x2c and flag2c):
            tmpString += b.hex()
            if (not len(tmpString[0:-5].replace(' ','')) == 90):
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue
            lidarData = CalcLidarData(tmpString[0:-5])
            angles.extend(lidarData.Angle_i)
            distances.extend(lidarData.Distance_i)
            #print(distances)
            """
            tab=[[],[]]
            for test in range (len(angles)):
                tab[0].append(angles[test])
                tab[1].append(distances[test])
            """
            tmpString = ""
            loopFlag = False
        
        else:
            tmpString += b.hex()+ " "

        flag2c = False

    i += 1

ser.close()