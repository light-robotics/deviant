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
    m1.move_servo_to_angle(id=2, angle=45, rate=1000)
    m1.move_servo_to_angle(id=3, angle=-45, rate=1000)
    m1.move_servo_to_angle(id=4, angle=90, rate=1000)
    m1.move_servo_to_angle(id=5, angle=-45, rate=1000)
    m1.move_servo_to_angle(id=6, angle=0, rate=1000)

    m2.move_servo_to_angle(id=8, angle=-45, rate=1000)
    m2.move_servo_to_angle(id=9, angle=-45, rate=1000)
    m2.move_servo_to_angle(id=10, angle=90, rate=1000)
    m2.move_servo_to_angle(id=11, angle=-45, rate=1000)
    m2.move_servo_to_angle(id=12, angle=0, rate=1000)
    """
    """
    time.sleep(1)
    m1.motor_or_servo(1, 1, 1000)
    m2.motor_or_servo(7, 1, -1000)

    time.sleep(1)
    m1.motor_or_servo(1, 1, 0)
    m2.motor_or_servo(7, 1, 0)
    """