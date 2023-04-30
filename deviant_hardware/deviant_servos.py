import time
import sys
import os
import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware.lx16a import LX16A, read_values
import logging
import configs.config as config
import configs.code_config as code_config
import logging.config
logging.config.dictConfig(code_config.logger_config)


class WheelsDirection(Enum):
    FORWARD        = 1
    TURN           = 2
    WALK           = 3
    SIDEWAYS       = 4
    DIAGONAL_RIGHT = 5
    DIAGONAL_LEFT  = 6
    NEUTRAL        = 7

servos_to_angles_mapping = {
    2  : "leg1_delta",
    3  : "leg1_gamma",
    4  : "leg1_beta",
    5  : "leg1_alpha",
    6  : "leg1_tetta",
    8  : "leg2_delta",
    9  : "leg2_gamma",
    10 : "leg2_beta",
    11 : "leg2_alpha",
    12 : "leg2_tetta",
    14 : "leg3_delta",
    15 : "leg3_gamma",
    16 : "leg3_beta",
    17 : "leg3_alpha",
    18 : "leg3_tetta",
    20 : "leg4_delta",
    21 : "leg4_gamma",
    22 : "leg4_beta",
    23 : "leg4_alpha",
    24 : "leg4_tetta",
}

def convert_kinematic_angles_to_ids(angles: Dict[str, Dict[str, float]]) -> Dict[id, float]:
    angles_to_ids_values = {}

    for servo_id, angle_name in servos_to_angles_mapping.items():
        angles_to_ids_values[servo_id] = angles.get(angle_name, 0)

    return angles_to_ids_values

def target_overshoot(current: float, target: float) -> float:
    overshoot_value = 0
    if abs(target - current) > 2:
        overshoot_value = 3
    elif abs(target - current) > 1:
        overshoot_value = 2
    
    overshoot_value = math.copysign(overshoot_value, target - current)

    return target + overshoot_value

class DeviantServos:
    def __init__(self):
        self.m1 = LX16A(Port='/dev/ttyAMA0') # 5-8   # 1-4
        self.m2 = LX16A(Port='/dev/ttyAMA2') # 9-12  # 5-8
        self.m3 = LX16A(Port='/dev/ttyAMA3') # 13-16 # 9-12
        self.m4 = LX16A(Port='/dev/ttyAMA1') # 1-4   # 13-16
        self.speed = 500
        self.min_speed = 700
        self.max_speed = 0 # 130 # 0 is instant, 10000 is very slow
        self.wheels_direction = WheelsDirection.FORWARD
        self.motors_locked = False

        self.diff_from_target_limit = config.deviant["servos"]["diff_from_target_limit"] # when it's time to start next movement
        self.diff_from_prev_limit = config.deviant["servos"]["diff_from_prev_limit"] # 1.0 # start next movement if we're stuck

        self.logger = logging.getLogger('main_logger')
        
        # 0.16 sec / 60 degrees for 7.4V+
        # 0.18 sec / 60 degrees for 6V+
        # my max speed is for 45 degrees
        # that means that max speed should be 120 for 7.4V+ and 135 for 6V+
        self.servo_ids = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24]
        self.motor_ids = [1, 7, 13, 19]

    def get_board_by_id(self, id: int) -> LX16A:
        if id in [3, 4, 5, 21, 22, 23]:
            return self.m1
        if id in [1, 2, 6, 7, 8, 12]:
            return self.m2
        if id in [9, 10, 11, 15, 16, 17]:
            return self.m3
        if id in [13, 14, 18, 19, 20, 24]:
            return self.m4

    def get_current_angles(self) -> Dict[int, float]:
        current_angles = {}
        for id in self.servo_ids:
            angle_name = servos_to_angles_mapping[id]
            current_angles[angle_name] = self.get_board_by_id(id).read_angle(id)
        return current_angles

    def adapt_delta_angle(self, angles: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        adapted_angles = {**angles}
        if self.wheels_direction == WheelsDirection.FORWARD:
            adapted_angles["leg1_delta"] = adapted_angles["leg1_tetta"] - 45
            adapted_angles["leg2_delta"] = adapted_angles["leg2_tetta"] + 45
            adapted_angles["leg3_delta"] = adapted_angles["leg3_tetta"] - 45
            adapted_angles["leg4_delta"] = adapted_angles["leg4_tetta"] + 45
        elif self.wheels_direction == WheelsDirection.SIDEWAYS:
            adapted_angles["leg1_delta"] = adapted_angles["leg1_tetta"] + 45
            adapted_angles["leg2_delta"] = adapted_angles["leg2_tetta"] - 45
            adapted_angles["leg3_delta"] = adapted_angles["leg3_tetta"] + 45
            adapted_angles["leg4_delta"] = adapted_angles["leg4_tetta"] - 45
        elif self.wheels_direction in [WheelsDirection.TURN, WheelsDirection.WALK]:
            adapted_angles["leg1_delta"] = adapted_angles["leg1_tetta"] - 75
            adapted_angles["leg2_delta"] = adapted_angles["leg2_tetta"] + 75
            adapted_angles["leg3_delta"] = adapted_angles["leg3_tetta"] - 75
            adapted_angles["leg4_delta"] = adapted_angles["leg4_tetta"] + 75
        elif self.wheels_direction == WheelsDirection.NEUTRAL:
            adapted_angles["leg1_delta"] = adapted_angles["leg1_tetta"]
            adapted_angles["leg2_delta"] = adapted_angles["leg2_tetta"]
            adapted_angles["leg3_delta"] = adapted_angles["leg3_tetta"]
            adapted_angles["leg4_delta"] = adapted_angles["leg4_tetta"]
        #elif self.wheels_direction == WheelsDirection.WALK:
        #    adapted_angles["leg1_delta"] = adapted_angles["leg1_tetta"] + 120
        #    adapted_angles["leg2_delta"] = adapted_angles["leg2_tetta"] - 120
        #    adapted_angles["leg3_delta"] = adapted_angles["leg3_tetta"] + 120
        #    adapted_angles["leg4_delta"] = adapted_angles["leg4_tetta"] - 120
        return adapted_angles

    def send_command_to_servos(self, angles, rate=1000):
        adapted_angles = self.adapt_delta_angle(angles)
        angles_converted = convert_kinematic_angles_to_ids(adapted_angles)
        self.logger.info(f'DS. send_command_to_servos. {angles_converted, rate}')
        for id in self.servo_ids:
            self.get_board_by_id(id).move_servo_to_angle(id, angles_converted[id], rate)

    def send_command_to_motors(self, speeds: List[float] = [1000, 1000, 1000, 1000], duration: int = 0):
        self.logger.info(f'DS. send_command_to_motors. {speeds, duration}')
        for id, speed in zip(self.motor_ids, speeds):
            self.get_board_by_id(id).motor_or_servo(id, 1, round(speed))

        assert duration < 10
        if duration > 0:
            time.sleep(duration)
            for id in self.motor_ids:
                self.get_board_by_id(id).motor_or_servo(id, 1, 0)

    def process_motors_command(self, command, speed):
        if command in ('forward', 'backwards', 'forward_4'):
            self.wheels_direction = WheelsDirection.FORWARD
        elif command in ('turn', 'turn_ccw'):
            self.wheels_direction = WheelsDirection.TURN
        elif command in ('walking'):
            self.wheels_direction = WheelsDirection.WALK
            speed = 0
        elif command in ('neutral'):
            #self.wheels_direction = WheelsDirection.NEUTRAL
            self.wheels_direction = WheelsDirection.WALK
            speed = 0
        else:
            print(f'Unknown command {command}')
            return
        if abs(speed) > 0:
            self.motors_locked = False

            if command in ['backwards', 'turn_ccw']:
                speed = -speed

            if command in ['turn', 'turn_ccw']:
                self.send_command_to_motors([speed, speed, speed, speed])
            elif command == 'forward_2':
                self.send_command_to_motors([-speed, -speed, speed, speed], 2)
            else:
                self.send_command_to_motors([-speed, -speed, speed, speed])

    def lock_motors(self):
        if self.motors_locked:
            return

        self.logger.info(f'Motors hardlocked')
        for id in self.motor_ids:
            self.get_board_by_id(id).move_servo_to_angle(id, 0, 0)
        self.motors_locked = True

    def print_status(self):
        j = 1
        for m in [self.m1, self.m2, self.m3, self.m4]:
            for _ in range(6):
                m.read_values(j)
                j += 1
    
    def set_speed(self, new_speed):
        if new_speed > 10000 or new_speed < self.max_speed:
            raise Exception(f'Invalid speed value {new_speed}. Should be between {self.max_speed} and 10000')
        self.speed = new_speed
        self.logger.info(f'DeviantServos. Speed set to {self.speed}')

    def get_angles_diff(self, target_angles, test_angles=None):
        if test_angles is None:
            test_angles = self.get_current_angles()

        angles_diff = {}
        for angle, value in target_angles.items():
            angles_diff[angle] = value - test_angles[angle]

        max_angle_diff = max([abs(x) for x in angles_diff.values()])
        self.logger.info(f'[DIFF] Max : {max_angle_diff}. Avg : {sum([abs(x) for x in angles_diff.values()])/len(angles_diff)}. Sum : {sum([abs(x) for x in angles_diff.values()])}')
        return angles_diff, max_angle_diff

    def set_servo_values_paced_full_adjustment(self, angles):
        _, max_angle_diff = self.get_angles_diff(angles)
        rate = round(max(self.speed * max_angle_diff / 45, self.max_speed)) # speed is normalized
        self.logger.info(f'max_angle_diff: {max_angle_diff}, self.speed : {self.speed}, self.speed * max_angle_diff / 45 : {self.speed * max_angle_diff / 45}')
        prev_angles = self.get_current_angles()

        self.send_command_to_servos(angles, rate)
        self.logger.info(f'Command sent. Rate: {rate}, angles: {angles}')
        time.sleep(0.8 * rate / 1000)
        #time.sleep(0.05)
        adjustment_done = False
        adjusted_angles = None
        
        for s in range(50):
            self.logger.info(f'Step {s}')
            
            current_angles = self.get_current_angles()
            self.logger.info(f'current angles: {current_angles}')
            # if diff from prev angles or target angles is small - continue
            self.logger.info('Target, then prev')
            diff_from_target = self.get_angles_diff(angles, current_angles)
            diff_from_prev = self.get_angles_diff(current_angles, prev_angles)

            self.logger.info(f'Diff from prev  : {diff_from_prev[0]}')
            self.logger.info(f'Diff from target: {diff_from_target[0]}')
     
            if diff_from_target[1] < self.diff_from_target_limit:                
                self.logger.info(f'Ready to move further')
                break
            
            elif diff_from_prev[1] < self.diff_from_prev_limit and \
                    not adjustment_done:

                if diff_from_target[1] > 2 * self.diff_from_target_limit:
                    print('-----------ALARM-----------')
                    self.logger.info('-----------ALARM-----------')
                
                self.logger.info(f'Command sent : {angles}')
                if diff_from_target[1] > self.diff_from_target_limit * 3:
                    self.logger.info(f'We"re in trouble, too large diff : {diff_from_target[1]}')
                    break
                else:
                    adjusted_angles = {}
                    for angle, target in angles.items():
                        adjusted_angles[angle] = round(target + (1.5 * diff_from_target[0][angle]), 1)
                    self.logger.info(f'Adjusting to : {adjusted_angles}')
                    adjustment_done = True
                    self.send_command_to_servos(adjusted_angles, round(rate/4))
                    time.sleep(0.03)
                    break

            elif diff_from_prev[1] < self.diff_from_prev_limit and \
                    adjustment_done:
                self.logger.info(f'Unreachable. Moving further')
                break

            prev_angles = dict(current_angles)

        self.logger.info('Function set_servo_values_paced_full_adjustment')

        self.log_movement_result(angles, adjusted_angles)
        #diff_from_target = self.get_angles_diff(angles, current_angles)
        #self.logger.info(f'Final Diff from target: max: {diff_from_target[1]}, {diff_from_target[0]}')

    def set_servo_values_paced_single_adjustment(self, angles):
        _, max_angle_diff = self.get_angles_diff(angles)
        rate = round(max(self.speed * max_angle_diff / 45, self.max_speed)) # speed is normalized
        self.logger.info(f'max_angle_diff: {max_angle_diff}, self.speed : {self.speed}, self.speed * max_angle_diff / 45 : {self.speed * max_angle_diff / 45}')

        self.send_command_to_servos(angles, rate)
        self.logger.info(f'Command sent. Rate: {rate}, angles: {angles}')
        time.sleep(0.95 * rate / 1000)

        current_angles = self.get_current_angles()
        self.logger.info(f'current angles: {current_angles}')

        diff_from_target = self.get_angles_diff(angles, current_angles)
        self.logger.info(f'Diff from target: {diff_from_target[0]}')

        adjusted_angles = {}
        for angle, target in angles.items():
            adjusted_angles[angle] = round(target + (1.5 * diff_from_target[0][angle]), 1)

        self.logger.info(f'Adjusting to : {adjusted_angles}')
        self.send_command_to_servos(adjusted_angles, round(rate/2))
        time.sleep(0.2 * rate / 1000)
    
        current_angles = self.get_current_angles()
        self.logger.info(f'current angles: {current_angles}')

    def set_servo_values_paced_wo_feedback(self, angles):
        _, max_angle_diff = self.get_angles_diff(angles)
        rate = round(max(self.speed * max_angle_diff / 45, self.max_speed)) # speed is normalized
        self.logger.info(f'max_angle_diff: {max_angle_diff}, self.speed : {self.speed}, self.speed * max_angle_diff / 45 : {self.speed * max_angle_diff / 45}')
        
        self.send_command_to_servos(angles, rate)
        self.logger.info(f'Command sent. Rate: {rate}, angles: {angles}')
        time.sleep(rate / 1000)

        self.logger.info('Function set_servo_values_paced_wo_feedback')
        self.log_movement_result(angles)
    
    def paced_wof_overshoot(self, angles):
        current_angles = self.get_current_angles()
        # calculate new target
        new_target = {}
        for angle, value in angles.items():
            new_target[angle] = target_overshoot(current_angles[angle], value)
        
        diff_from_target = self.get_angles_diff(new_target, current_angles)
        self.logger.info(f'Diff from target: {diff_from_target[0]}')
        rate = round(max(self.speed * diff_from_target[1] / 45, self.max_speed)) # speed is normalized
        self.logger.info(f'max_angle_diff: {diff_from_target[1]}, self.speed : {self.speed}, rate : {rate}')

        self.send_command_to_servos(new_target, rate)
        self.logger.info(f'Command sent. Rate: {rate}, angles: {new_target}')
        time.sleep(rate / 1000)

        self.log_movement_result(angles, new_target)
    
    def log_movement_result(self, target, adjusted=None):
        current_angles = self.get_current_angles()
        for k, v in target.items():
            if adjusted:
                self.logger.info(f'Angle {k}. Current: {current_angles[k]}. Target: {v}. Adjusted: {adjusted[k]}')
            else:
                self.logger.info(f'Angle {k}. Current: {current_angles[k]}. Target: {v}.')


if __name__ == '__main__':
    dvnt = DeviantServos()
        
    """
    dvnt.set_speed(3000)
    dvnt.wheels_direction = WheelsDirection.WALK
    dvnt.send_command_to_motors(-1000)
    angles = {'leg1': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}, 'leg2': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}, 'leg3': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}, 'leg4': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}}
    dvnt.send_command_to_servos(angles, 2000)
    time.sleep(3)
    angles = {'leg1': {'tetta': 0.0, 'alpha': -19.47, 'beta': 88.95, 'gamma': -70.62}, 'leg2': {'tetta': 0.0, 'alpha': -19.47, 'beta': 88.95, 'gamma': -70.62}, 'leg3': {'tetta': 0.0, 'alpha': -19.47, 'beta': 88.95, 'gamma': -70.62}, 'leg4': {'tetta': 0.0, 'alpha': -19.47, 'beta': 88.95, 'gamma': -70.62}}
    dvnt.send_command_to_servos(angles, 5000)
    time.sleep(6)
    angles = {'leg1': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}, 'leg2': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}, 'leg3': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}, 'leg4': {'tetta': 0.0, 'alpha': -53.19, 'beta': 72.44, 'gamma': -94.85}}
    dvnt.send_command_to_servos(angles, 2000)
    time.sleep(3)
    dvnt.send_command_to_motors(0)
    """
    dvnt.wheels_direction = WheelsDirection.FORWARD
    # 10-13-13
    #angles = {'leg1': {'tetta': 0.0, 'alpha': -72.38, 'beta': 93.02, 'gamma': -96.45}, 'leg2': {'tetta': 0.0, 'alpha': -72.38, 'beta': 93.02, 'gamma': -96.45}, 'leg3': {'tetta': 0.0, 'alpha': -72.38, 'beta': 93.02, 'gamma': -96.45}, 'leg4': {'tetta': 0.0, 'alpha': -72.38, 'beta': 93.02, 'gamma': -96.45}}
    # 20-10-10
    #angles = {'leg1': {'tetta': 0.0, 'alpha': -17.05, 'beta': 108.58, 'gamma': -27.57}, 'leg2': {'tetta': 0.0, 'alpha': -17.05, 'beta': 108.58, 'gamma': -27.57}, 'leg3': {'tetta': 0.0, 'alpha': -17.05, 'beta': 108.58, 'gamma': -27.57}, 'leg4': {'tetta': 0.0, 'alpha': -17.05, 'beta': 108.58, 'gamma': -27.57}}
    # 20-13-13
    angles = {'leg1': {'tetta': 0.0, 'alpha': -21.17, 'beta': 108.95, 'gamma': -15.32}, 'leg2': {'tetta': 0.0, 'alpha': -21.17, 'beta': 108.95, 'gamma': -15.32}, 'leg3': {'tetta': 0.0, 'alpha': -21.17, 'beta': 108.95, 'gamma': -15.32}, 'leg4': {'tetta': 0.0, 'alpha': -21.17, 'beta': 108.95, 'gamma': -15.32}}
    dvnt.send_command_to_servos(angles, 2000)
    
    time.sleep(3)
    dvnt.send_command_to_motors(1000)
    time.sleep(2)
    dvnt.send_command_to_motors(0)

    #dvnt.send_command_to_motors(1000)
    #time.sleep(3)
    #dvnt.send_command_to_motors(0)

    #sequence = [[0.0, 60.0, 100.0, -10.0, 0.0, 60.0, 100.0, -10.0, 0.0, 60.0, 100.0, -10.0, 0.0, 60.0, 100.0, -10.0]]
        
    #for angles in sequence:     
    #    dvnt.set_servo_values_paced(angles)
    