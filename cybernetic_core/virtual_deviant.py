from typing import List, Tuple
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybernetic_core.kinematics import DeviantKinematics
from configs import config as cfg
from configs import code_config
from cybernetic_core.cybernetic_utils.moves import Sequence

UP_OR_DOWN_CM   = cfg.moves["up_or_down_cm"]
FORWARD_BODY_CM = cfg.moves["move_body_cm"]
FORWARD_LEGS_1LEG_CM = cfg.moves["forward_body_1_leg_cm"]
FORWARD_LEGS_2LEG_CM = cfg.moves["forward_body_2_leg_cm"]
REPOSITION_CM   = cfg.moves["reposition_cm"]
SIDE_LOOK_ANGLE = cfg.moves["side_look_angle"]
VERTICAL_LOOK_ANGLE = cfg.moves["vertical_look_angle"]


class VirtualDeviant():
    """
    Class to separate getting sequences for commands from actual kinematics calculations
    """
    def __init__(self, logger):
        self.logger = logger
        self.dk = DeviantKinematics()

    def get_sequence(self, command: str):
        dk = self.dk    
        if command == 'forward_1':
            # Legs 1 and 3 moved x1
            dk.move_2_legs_phased_13(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_2':
            # Legs 2 and 4 moved x2
            dk.move_2_legs_phased_24(0, 2 * FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_22':
            # Legs 2 and 4 moved x1
            dk.move_2_legs_phased_24(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_3':
            # Legs 1 and 3 moved x2
            dk.move_2_legs_phased_13(0, 2 * FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_32':
            # Legs 1 and 3 moved x1
            dk.move_2_legs_phased_13(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_one_legged':
            dk.move_body_straight(0, FORWARD_LEGS_1LEG_CM)
        elif command in ['battle_mode', 'sentry_mode', 'walking_mode', 'run_mode']:
            dk.switch_mode(command)
        elif command == 'body_forward':
            if dk.body_delta_xy()[1] > cfg.limits["body_forward"]:
                print('Forward body limit reached')
            else:
                dk.body_movement(0, FORWARD_BODY_CM, 0)
        elif command == 'body_backward':
            if dk.body_delta_xy()[1] < -cfg.limits["body_forward"]:
                print('Backward body limit reached')
            else:
                dk.body_movement(0, -FORWARD_BODY_CM, 0)
        elif command == 'body_left':
            if dk.body_delta_xy()[0] < -cfg.limits["body_sideways"]:
                print('Body left limit reached')
            else:
                dk.body_movement(-FORWARD_BODY_CM, 0, 0)
        elif command == 'body_right':
            if dk.body_delta_xy()[0] > cfg.limits["body_sideways"]:
                print('Body right limit reached')
            else:
                dk.body_movement(FORWARD_BODY_CM, 0, 0)
        elif command == 'body_to_center':
            dk.body_to_center()
        elif command == 'up':
            dk.body_movement(0, 0, UP_OR_DOWN_CM)
        elif command == 'down':
            dk.body_movement(0, 0, -UP_OR_DOWN_CM)
        elif command == 'reposition_x_up':
            dk.reposition_legs(REPOSITION_CM, 0)
        elif command == 'reposition_x_down':
            dk.reposition_legs(-REPOSITION_CM, 0)
        elif command == 'reposition_y_up':
            dk.reposition_legs(0, REPOSITION_CM)
        elif command == 'reposition_y_down':
            dk.reposition_legs(0, -REPOSITION_CM)
        elif command == 'start':
            dk.start()
        elif command == 'end':
            dk.end()
        elif command == 'reset':
            dk.reset()
        else:
            print(f'Unknown command')
        
        return dk.sequence
