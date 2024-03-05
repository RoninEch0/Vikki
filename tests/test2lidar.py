import serial
import time
import math

# Constants
BAUDRATE = 115200
ANGLE_MIN = -180
ANGLE_MAX = 180
RANGE_MIN = 0.1
RANGE_MAX = 12.0
READING_COUNT = 360

class LiPkg:
    # Define LiPkg class according to your implementation

class CallbackAsyncSerial:
    # Define CallbackAsyncSerial class according to your implementation

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class LD19Node:
    def __init__(self, port='/dev/ttyUSB0'):
        self.port_ = port
        self.lidar_ = None
        self.serial_port_ = None
        self.output_ = {
            'header': {'stamp': 0, 'frame_id': 'laser'},
            'angle_min': ANGLE_MIN,
            'angle_max': ANGLE_MAX,
            'range_min': RANGE_MIN,
            'range_max': RANGE_MAX,
            'angle_increment': 0.0,
            'time_increment': 0.0,
            'scan_time': 0.0,
            'ranges': [0.0] * READING_COUNT,
            'intensities': [0.0] * READING_COUNT
        }

        self.init_device()

    def init_device(self):
        self.lidar_ = LiPkg()

        try:
            self.serial_port_ = CallbackAsyncSerial(self.port_, BAUDRATE)
        except Exception as e:
            print(f"Error opening device port: {self.port_}: {e}")
            return False

        self.serial_port_.setCallback(lambda byte, len: self.handle_serial_data(byte, len))

        self.lidar_.SetPopulateCallback(lambda laser_data: self.populate_message(laser_data))

        if not self.serial_port_.isOpen():
            print(f"Error opening device port: {self.port_}")
            return False

        print(f"Successfully opened device port: {self.port_}")
        return True

    def populate_message(self, laser_data):
        angle_increment = math.radians(self.lidar_.GetSpeed() / 4500)
        max_index = int((ANGLE_MAX - ANGLE_MIN) / angle_increment)

        self.output_['header']['stamp'] = time.time()
        self.output_['angle_increment'] = angle_increment

        for point in laser_data:
            range_val = point.distance / 1000.0
            angle = math.radians(point.angle)

            index = int(map_range(angle, 0, 2 * math.pi, max_index, 0))
            index_offset = int(map_range(math.pi / 2, 0, 2 * math.pi, 0, max_index))
            index += index_offset

            if index > max_index:
                index -= max_index
            if index < 0:
                index += max_index

            if 0 <= index < max_index:
                self.output_['ranges'][index] = range_val

                if math.isnan(self.output_['ranges'][index]):
                    self.output_['ranges'][index] = range_val
                elif range_val < self.output_['ranges'][index]:
                    self.output_['ranges'][index] = range_val

                self.output_['intensities'][index] = point.confidence

    def handle_serial_data(self, byte, len):
        if self.lidar_.Parse(byte, len):
            self.lidar_.AssemblePacket()

    def get_laser_scan(self):
        return self.output_

def main():
    ld19_node = LD19Node()

    while True:
        laser_scan = ld19_node.get_laser_scan()
        print("Laser Scan:")
        print(laser_scan)
        time.sleep(0.1)

if __name__ == '__main__':
    main()