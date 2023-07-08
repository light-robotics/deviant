import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware.lx16a import LX16A, read_all_servos, read_values

if __name__ == '__main__':      
    m1 = LX16A(Port='/dev/ttyAMA0') # 1-6
    m2 = LX16A(Port='/dev/ttyAMA2') # 7-12
    m3 = LX16A(Port='/dev/ttyAMA3') # 13-18
    m4 = LX16A(Port='/dev/ttyAMA1') # 19-24
    
    # 1: 3-5, 21-23
    # 2: 1,2, 6, (7,8), 12
    # 3: 9-11, 15-17
    # 4: (13,14), 18, (19,20), 24

    m2.move_servo_to_angle(6, 1, 2000)
    time.sleep(2.1)
    print(m2.read_angle(6))
