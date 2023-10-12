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

    """
    angle = 90
    m1.move_servo_to_angle(3, angle, 1000)
    m1.move_servo_to_angle(21, angle, 1000)

    m3.move_servo_to_angle(9, angle, 1000)
    m3.move_servo_to_angle(15, angle, 1000)

    angle2 = -65
    m1.move_servo_to_angle(4, angle2, 1000)
    m1.move_servo_to_angle(22, angle2, 1000)

    m3.move_servo_to_angle(10, angle2, 1000)
    m3.move_servo_to_angle(16, angle2, 1000)

    angle3 = -65
    m1.move_servo_to_angle(5, angle3, 1500)
    m1.move_servo_to_angle(23, angle3, 1500)

    m3.move_servo_to_angle(11, angle3, 1500)
    m3.move_servo_to_angle(17, angle3, 1500)

    angle4 = -40
    angle5 = 40
    m2.move_servo_to_angle(6, angle5, 3000)
    m2.move_servo_to_angle(12, angle4, 3000)

    m4.move_servo_to_angle(18, angle5, 3000)
    m4.move_servo_to_angle(24, angle4, 3000)


    time.sleep(1.6)

    print(m1.read_angle(5))
    print(m1.read_angle(23))
    print(m3.read_angle(11))
    print(m3.read_angle(17))
    """

    
    #time.sleep(3)
    
    angle0 = 0
    m1.move_servo_to_angle(11, angle0, 1000)
    m2.move_servo_to_angle(17, angle0, 1000)
    m3.move_servo_to_angle(23, angle0, 1000)
    m4.move_servo_to_angle(5, angle0, 1000)
    
    spd = 1000

    angle1 = 40 # 30 -> 60
    m1.move_servo_to_angle(10, angle1, spd)
    m2.move_servo_to_angle(16, angle1, spd)
    m3.move_servo_to_angle(22, angle1, spd)
    m4.move_servo_to_angle(4, angle1, spd)

    angle2 = 70 # 45 -> 90
    m1.move_servo_to_angle(9, angle2, spd)
    m2.move_servo_to_angle(15, angle2, spd)
    m3.move_servo_to_angle(21, angle2, spd)
    m4.move_servo_to_angle(3, angle2, spd)

    time.sleep(1)
    
    spd2 = 1000

    angle1 = 75 # 30 -> 60
    m1.move_servo_to_angle(10, angle1, spd2)
    m2.move_servo_to_angle(16, angle1, spd2)
    m3.move_servo_to_angle(22, angle1, spd2)
    m4.move_servo_to_angle(4, angle1, spd2)

    angle2 = 100 # 45 -> 90
    m1.move_servo_to_angle(9, angle2, spd2)
    m2.move_servo_to_angle(15, angle2, spd2)
    m3.move_servo_to_angle(21, angle2, spd2)
    m4.move_servo_to_angle(3, angle2, spd2)
    
    time.sleep(1)

    for i in [9, 10, 11]:
        m1.read_values(i)
    for i in [15, 16, 17]:
        m2.read_values(i)
    for i in [21, 22, 23]:
        m3.read_values(i)
    for i in [3, 4, 5]:
        m4.read_values(i)