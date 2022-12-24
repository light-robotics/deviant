import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware.lx16a import LX16A, read_all_servos

if __name__ == '__main__':      
    m1 = LX16A(Port='/dev/ttyAMA0') # 1-6
    m2 = LX16A(Port='/dev/ttyAMA2') # 7-12
    m3 = LX16A(Port='/dev/ttyAMA3') # 13-18
    m4 = LX16A(Port='/dev/ttyAMA1') # 19-24
    
    read_all_servos(m1, m2, m3, m4)

    """
    position_rate = 3000
    time.sleep(5)

    m1.move_servo_to_angle(id=2, angle=45, rate=position_rate)
    m1.move_servo_to_angle(id=3, angle=-45, rate=position_rate)
    m1.move_servo_to_angle(id=4, angle=90, rate=position_rate)
    m1.move_servo_to_angle(id=5, angle=-45, rate=position_rate)
    m1.move_servo_to_angle(id=6, angle=0, rate=position_rate)

    m2.move_servo_to_angle(id=8, angle=-45, rate=position_rate)
    m2.move_servo_to_angle(id=9, angle=-45, rate=position_rate)
    m2.move_servo_to_angle(id=10, angle=90, rate=position_rate)
    m2.move_servo_to_angle(id=11, angle=-45, rate=position_rate)
    m2.move_servo_to_angle(id=12, angle=0, rate=position_rate)

    m3.move_servo_to_angle(id=14, angle=45, rate=position_rate)
    m3.move_servo_to_angle(id=15, angle=-45, rate=position_rate)
    m3.move_servo_to_angle(id=16, angle=90, rate=position_rate)
    m3.move_servo_to_angle(id=17, angle=-45, rate=position_rate)
    m3.move_servo_to_angle(id=18, angle=0, rate=position_rate)

    m4.move_servo_to_angle(id=20, angle=-45, rate=position_rate)
    m4.move_servo_to_angle(id=21, angle=-45, rate=position_rate)
    m4.move_servo_to_angle(id=22, angle=90, rate=position_rate)
    m4.move_servo_to_angle(id=23, angle=-45, rate=position_rate)
    m4.move_servo_to_angle(id=24, angle=0, rate=position_rate)
    
    
    time.sleep(1)
    m1.motor_or_servo(1, 1, 1000)
    m2.motor_or_servo(7, 1, -1000)
    m3.motor_or_servo(13, 1, -1000)
    m4.motor_or_servo(19, 1, 1000)

    time.sleep(5)
    m1.motor_or_servo(1, 1, 0)
    m2.motor_or_servo(7, 1, 0)
    m3.motor_or_servo(13, 1, 0)
    m4.motor_or_servo(19, 1, 0)
    """