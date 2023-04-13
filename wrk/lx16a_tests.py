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
    # 2: 9-11, 15-17
    # 3: 1,2, 6, (7,8), 12
    # 4: (13,14), 18, (19,20), 24

    #m3.move_servo_to_angle(2, 0, 1000)
    #m3.move_servo_to_angle(8, 0, 1000)
    #m4.move_servo_to_angle(14, 0, 1000)
    #m4.move_servo_to_angle(20, 0, 1000)

    # m1.move_servo_to_angle(4, 0, 1000)
    # m1.move_servo_to_angle(3, 0, 1000)

    # m1.move_servo_to_angle(22, -150, 3000)
    # time.sleep(3.0)
    #m1.move_servo_to_angle(22, 2, 3000)
    #time.sleep(3.0)
    # m3.move_servo_to_angle(11, -85, 3000)
    # time.sleep(3.0)
    # print(m3.read_angle(11))

    angle = 45
    m1.move_servo_to_angle(3, angle, 1000)
    m1.move_servo_to_angle(21, angle, 1000)

    m3.move_servo_to_angle(9, angle, 1000)
    m3.move_servo_to_angle(15, angle, 1000)

    angle2 = 45
    m1.move_servo_to_angle(4, angle2, 1000)
    m1.move_servo_to_angle(22, angle2, 1000)

    m3.move_servo_to_angle(10, angle2, 1000)
    m3.move_servo_to_angle(16, angle2, 1000)

    angle3 = 0
    m1.move_servo_to_angle(5, angle3, 1000)
    m1.move_servo_to_angle(23, angle3, 1000)

    m3.move_servo_to_angle(11, angle3, 1000)
    m3.move_servo_to_angle(17, angle3, 1000)

    angle4 = -45
    angle5 = 45
    m2.move_servo_to_angle(6, angle5, 1000)
    m2.move_servo_to_angle(12, angle4, 1000)

    m4.move_servo_to_angle(18, angle5, 1000)
    m4.move_servo_to_angle(24, angle4, 1000)


    time.sleep(1.1)

    """
    print(m2.read_angle(6))
    print(m2.read_angle(12))
    print(m4.read_angle(18))
    print(m4.read_angle(24))
    """
    print(m1.read_angle(5))
    print(m1.read_angle(23))
    print(m3.read_angle(11))
    print(m3.read_angle(17))

    for i in [3, 4, 5, 21, 22, 23]:
        m1.read_values(i)
    for i in [1, 2, 6, 7, 8, 12]:
        m2.read_values(i)
    for i in [9, 10, 11, 15, 16, 17]:
        m3.read_values(i)
    for i in [13, 14, 18, 19, 20, 24]:
        m4.read_values(i)
    

