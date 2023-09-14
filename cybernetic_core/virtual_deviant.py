from typing import List, Tuple
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybernetic_core.kinematics import DeviantKinematics
from configs import kinematics_config as cfg

UP_OR_DOWN_CM   = cfg.moves["up_or_down_cm"]
FORWARD_BODY_CM = cfg.moves["move_body_cm"]
FORWARD_LEGS_1LEG_CM = cfg.moves["forward_body_1_leg_cm"]
FORWARD_LEGS_2LEG_CM = cfg.moves["forward_body_2_leg_cm"]


class VirtualDeviant(DeviantKinematics):
    """
    Class to separate getting sequences for commands from actual kinematics calculations
    """
    def __init__(self):
        super().__init__()

    def get_sequence(self, command: str):
        if command == 'keep_position':
            self.add_angles_snapshot()
        elif command == 'forward_1':
            # Legs 1 and 3 moved x1
            self.move_2_legs_phased_13(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_2':
            # Legs 2 and 4 moved x2
            self.move_2_legs_phased_24(0, 2 * FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_22':
            # Legs 2 and 4 moved x1
            self.move_2_legs_phased_24(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_3':
            # Legs 1 and 3 moved x2
            self.move_2_legs_phased_13(0, 2 * FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_32':
            # Legs 1 and 3 moved x1
            self.move_2_legs_phased_13(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'forward_one_legged':
            self.move_body_straight(0, FORWARD_LEGS_1LEG_CM, [1, 4, 2, 3])
            #self.leg_move_with_compensation(2, 0, -FORWARD_LEGS_1LEG_CM)
            #self.leg_move_with_compensation(2, 0, FORWARD_LEGS_1LEG_CM)
            #self.body_to_center()
        elif command in ['battle_mode', 'sentry_mode', 'walking_mode', 'run_mode']:
            self.switch_mode(command)
        elif command == 'body_forward':
            self.body_movement(0, FORWARD_BODY_CM, 0)
        elif command == 'body_backward':
            self.body_movement(0, -FORWARD_BODY_CM, 0)
        elif command == 'body_left':
            self.body_movement(-FORWARD_BODY_CM, 0, 0)
        elif command == 'body_right':
            self.body_movement(FORWARD_BODY_CM, 0, 0)
        elif command == 'body_to_center':
            self.body_to_center()
        elif command == 'up':
            self.body_movement(0, 0, UP_OR_DOWN_CM)
        elif command == 'up_down':
            self.body_movement(0, 0, 1)
            self.body_movement(0, 0, -1)
        elif command == 'up_6':
            self.body_movement(0, 0, 6)
        elif command == 'up_4':
            self.body_movement(0, 0, 4)
        elif command == 'down':
            self.body_movement(0, 0, -UP_OR_DOWN_CM)
        elif command == 'down_4':
            self.body_movement(0, 0, -4)
        elif command == 'down_6':
            self.body_movement(0, 0, -6)
        elif command == 'climb_1':
            self.two_legged_climbing_1(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'climb_2':
            self.two_legged_climbing_2(0, FORWARD_LEGS_2LEG_CM)
        elif command == 'spear_up':
            self.spear_up()
        elif command == 'spear_down':
            self.spear_down()
        elif command == 'reposition_wider_8':
            self.go_to_height(20)
            self.reposition_legs(8, -8)
        elif command == 'reposition_narrower_8':
            self.reposition_legs(-8, 8)
            self.go_to_height(14)
        elif command == 'legs_up_down':
            self.reposition_legs(0, 0)
        elif command == 'start':
            self.start()
        elif command == 'end':
            self.end()
        elif command == 'reset':
            self.reset()
        elif command == 'actualize_wheels':
            self.actualize_wheels()
        else:
            print(f'Unknown command')
        
        return self.sequence
