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
    # read_all_servos(m1, m2, m3, m4)
    # Moving to {'leg1_tetta': 0.0, 'leg1_alpha': -15.55, 'leg1_beta': 80.39, 'leg1_gamma': -10.15, 'leg2_tetta': 0.0, 'leg2_alpha': -15.55, 'leg2_beta': 80.39, 'leg2_gamma': -10.15, 'leg3_tetta': 0.0, 'leg3_alpha': -15.55, 'leg3_beta': 80.39, 'leg3_gamma': -10.15, 'leg4_tetta': 0.0, 'leg4_alpha': -15.55, 'leg4_beta': 80.39, 'leg4_gamma': -10.15}. Move type: body
    #m1.move_servo_to_angle(5, -15, 1000)
    #m1.move_servo_to_angle(4, -80, 2000)
    #m1.move_servo_to_angle(3, 10, 1000)
    # m1.move_servo_to_angle(21, 0, 1000)
    #for j in range(1, 25):        
    #    m4.read_values(j)
    # m1.move_servo_to_angle(1, 0, 1000)
    # m4.read_values(24)
    # m4.move_servo_to_angle(24, 0, 1000)
    for i in [3, 4, 5, 21, 22, 23]:
        m1.read_values(i)
    for i in [9, 10, 11, 15, 16, 17]:
        m2.read_values(i)
    for i in [1, 2, 6, 7, 8, 12]:
        m3.read_values(i)
    for i in [13, 14, 18, 19, 20, 24]:
        m4.read_values(i)
    """
    tetta_0 = False
    side = True

    alpha_45 = False
    alpha_max = 83

    beta_90 = True

    delta_0 = False
    if tetta_0:
        delta_0 = True
    elif side:
        delta_60 = True
    else:
        delta_60 = False

    position_rate = 3000
    print(f'Before: {read_values(m3, 1)}')
    m3.move_servo_to_angle(id=1, angle=0, rate=1000)
    time.sleep(1.0)
    m3.move_servo_to_angle(id=1, angle=90, rate=1000)
    time.sleep(3.0)
    print(f'After: {read_values(m3, 1)}')
    m3.move_servo_to_angle(id=1, angle=0, rate=1000)
    """

    """
    m1.move_servo_to_angle(id=6, angle=0, rate=position_rate)
    m2.move_servo_to_angle(id=12, angle=0, rate=position_rate)
    m3.move_servo_to_angle(id=18, angle=0, rate=position_rate)
    m4.move_servo_to_angle(id=24, angle=0, rate=position_rate)
    """
    """
    if delta_0:
        m1.move_servo_to_angle(id=2, angle=0, rate=position_rate)
    elif delta_60:
        m1.move_servo_to_angle(id=2, angle=75, rate=position_rate)
    else:
        m1.move_servo_to_angle(id=2, angle=8, rate=position_rate)

    m1.move_servo_to_angle(id=3, angle=-90, rate=position_rate)
    if beta_90:
        m1.move_servo_to_angle(id=4, angle=90, rate=position_rate)
    else:
        m1.move_servo_to_angle(id=4, angle=45, rate=position_rate)
    if alpha_45:
        m1.move_servo_to_angle(id=5, angle=-45, rate=position_rate)
    else:
        m1.move_servo_to_angle(id=5, angle=-alpha_max, rate=position_rate)

    if tetta_0:
        m1.move_servo_to_angle(id=6, angle=0, rate=position_rate)
    elif side:
        m1.move_servo_to_angle(id=6, angle=30, rate=position_rate)
    else:
        m1.move_servo_to_angle(id=6, angle=-37, rate=position_rate)


    if delta_0:
        m2.move_servo_to_angle(id=8, angle=0, rate=position_rate)
    elif delta_60:
        m2.move_servo_to_angle(id=8, angle=-75, rate=position_rate)
    else:
        m2.move_servo_to_angle(id=8, angle=-8, rate=position_rate)

    m2.move_servo_to_angle(id=9, angle=-90, rate=position_rate)
    if beta_90:
        m2.move_servo_to_angle(id=10, angle=90, rate=position_rate)
    else:
        m2.move_servo_to_angle(id=10, angle=45, rate=position_rate)
    if alpha_45:
        m2.move_servo_to_angle(id=11, angle=-45, rate=position_rate)
    else:
        m2.move_servo_to_angle(id=11, angle=-alpha_max, rate=position_rate)
    if tetta_0:
        m2.move_servo_to_angle(id=12, angle=0, rate=position_rate)
    elif side:
        m2.move_servo_to_angle(id=12, angle=-30, rate=position_rate)
    else:
        m2.move_servo_to_angle(id=12, angle=37, rate=position_rate)

    if delta_0:
        m3.move_servo_to_angle(id=14, angle=0, rate=position_rate)
    elif delta_60:
        m3.move_servo_to_angle(id=14, angle=75, rate=position_rate)
    else:
        m3.move_servo_to_angle(id=14, angle=8, rate=position_rate)

    m3.move_servo_to_angle(id=15, angle=-90, rate=position_rate)
    if beta_90:
        m3.move_servo_to_angle(id=16, angle=90, rate=position_rate)
    else:
        m3.move_servo_to_angle(id=16, angle=45, rate=position_rate)
    if alpha_45:
        m3.move_servo_to_angle(id=17, angle=-45, rate=position_rate)
    else:
        m3.move_servo_to_angle(id=17, angle=-alpha_max, rate=position_rate)
    if tetta_0:
        m3.move_servo_to_angle(id=18, angle=0, rate=position_rate)
    elif side:
        m3.move_servo_to_angle(id=18, angle=30, rate=position_rate)
    else:
        m3.move_servo_to_angle(id=18, angle=-37, rate=position_rate)

    if delta_0:
        m4.move_servo_to_angle(id=20, angle=0, rate=position_rate)
    elif delta_60:
        m4.move_servo_to_angle(id=20, angle=-75, rate=position_rate)
    else:
        m4.move_servo_to_angle(id=20, angle=-8, rate=position_rate)

    m4.move_servo_to_angle(id=21, angle=-90, rate=position_rate)
    if beta_90:
        m4.move_servo_to_angle(id=22, angle=90, rate=position_rate)
    else:
        m4.move_servo_to_angle(id=22, angle=45, rate=position_rate)
    if alpha_45:
        m4.move_servo_to_angle(id=23, angle=-45, rate=position_rate)
    else:
        m4.move_servo_to_angle(id=23, angle=-alpha_max, rate=position_rate)
    if tetta_0:
        m4.move_servo_to_angle(id=24, angle=0, rate=position_rate)
    elif side:
        m4.move_servo_to_angle(id=24, angle=-30, rate=position_rate)
    else:
        m4.move_servo_to_angle(id=24, angle=37, rate=position_rate)
    
    """

    """
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