import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware.lx16a import LX16A, read_all_servos, read_values
from cybernetic_core.geometry.inverse_kinematics import leg_angles

if __name__ == '__main__':      
    m1 = LX16A(Port='/dev/ttyAMA0') # 1-6
    m2 = LX16A(Port='/dev/ttyAMA2') # 7-12
    m3 = LX16A(Port='/dev/ttyAMA3') # 13-18
    m4 = LX16A(Port='/dev/ttyAMA1') # 19-24
    
    time.sleep(2.0)
    angle0 = 0
    m1.move_servo_to_angle(11, angle0, 1000)
    m2.move_servo_to_angle(17, angle0, 1000)
    m3.move_servo_to_angle(23, angle0, 1000)
    m4.move_servo_to_angle(5, angle0, 1000)
    
    spd = 0
    alpha1, beta1 = leg_angles(18, 0)
    m1.move_servo_to_angle(10, alpha1, spd)
    m2.move_servo_to_angle(16, alpha1, spd)
    m3.move_servo_to_angle(22, alpha1, spd)
    m4.move_servo_to_angle(4, alpha1, spd)

    m1.move_servo_to_angle(9, beta1, spd)
    m2.move_servo_to_angle(15, beta1, spd)
    m3.move_servo_to_angle(21, beta1, spd)
    m4.move_servo_to_angle(3, beta1, spd)

    time.sleep(0.1)
    
    spd2 = 0

    alpha2, beta2 = leg_angles(10, 0)

    m1.move_servo_to_angle(10, alpha2, spd2)
    m2.move_servo_to_angle(16, alpha2, spd2)
    m3.move_servo_to_angle(22, alpha2, spd2)
    m4.move_servo_to_angle(4, alpha2, spd2)

    m1.move_servo_to_angle(9, beta2, spd2)
    m2.move_servo_to_angle(15, beta2, spd2)
    m3.move_servo_to_angle(21, beta2, spd2)
    m4.move_servo_to_angle(3, beta2, spd2)
    
    time.sleep(1)
    
    for i in [9, 10, 11]:
        m1.read_values(i)
    for i in [15, 16, 17]:
        m2.read_values(i)
    for i in [21, 22, 23]:
        m3.read_values(i)
    for i in [3, 4, 5]:
        m4.read_values(i)