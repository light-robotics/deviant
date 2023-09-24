import math
import copy
from dataclasses import dataclass
from typing import List, Dict
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybernetic_core.geometry.angles import calculate_leg_angles, calculate_D_point, turn_on_angle, convert_legs_angles, convert_legs_angles_back
from cybernetic_core.geometry.lines import Point, LinearFunc, calculate_intersection, move_on_a_line
import configs.code_config as code_config
import configs.kinematics_config as cfg
import logging.config
from cybernetic_core.cybernetic_utils.moves import Move, MoveSnapshot


class Leg:
    def __init__(self, O: Point, D: Point):
        logging.config.dictConfig(code_config.logger_config)
        self.logger = logging.getLogger('angles_logger') #logging.getLogger('main_logger')
        self.O = O
        self.D = D
        self.update_angles()

    def update_angles(self):
        # tetta is not fully correct, because it uses atan2
        # tetta is corrected via convert_tetta function
        calculated_angles = calculate_leg_angles(self.O, self.D, self.logger)
        self.tetta, self.alpha, self.beta, self.gamma = calculated_angles

    def move_mount_point(self, delta_x, delta_y, delta_z):
        self.O.move(delta_x, delta_y, delta_z)
        self.update_angles()
    
    def move_end_point(self, delta_x, delta_y, delta_z):
        self.D.move(delta_x, delta_y, delta_z)
        self.update_angles()

class DeviantKinematics:
    def __init__(self, v=None, h_x=None, h_y=None):
        logging.config.dictConfig(code_config.logger_config)
        self.logger = logging.getLogger('main_logger')

        if v and h_x and h_y:
            self.legs_offset_v = v
            self.legs_offset_h_x = h_x
            self.legs_offset_h_y = h_y
        else:
            self.legs_offset_v = cfg.start['vertical']
            self.legs_offset_h_x = cfg.start['horizontal_x']
            self.legs_offset_h_y = cfg.start['horizontal_y']
        self.legs = self.initiate_legs()

        if False:    
            print(f"""
            Kinematics created with 
            v = {self.legs_offset_v}, 
            h_x = {self.legs_offset_h_x},
            h_y = {self.legs_offset_h_y}
            """)
        
        self.angles_history = []
        self.add_angles_snapshot('init')

    def reset_history(self):
        self.angles_history = []
    
    def save_state(self):
        self.legs_backup = copy.deepcopy(self.legs)

    def load_state(self):
        self.legs = self.legs_backup

    def add_angles_snapshot(self, move_type: str = 'unknown'):
        angles = {
            "leg1_alpha": self.legs[1].alpha,
            "leg1_beta": self.legs[1].beta,
            "leg1_gamma": self.legs[1].gamma,
            "leg1_tetta": self.legs[1].tetta,
            "leg2_alpha": self.legs[2].alpha,
            "leg2_beta": self.legs[2].beta,
            "leg2_gamma": self.legs[2].gamma,
            "leg2_tetta": self.legs[2].tetta,
            "leg3_alpha": self.legs[3].alpha,
            "leg3_beta": self.legs[3].beta,
            "leg3_gamma": self.legs[3].gamma,
            "leg3_tetta": self.legs[3].tetta,
            "leg4_alpha": self.legs[4].alpha,
            "leg4_beta": self.legs[4].beta,
            "leg4_gamma": self.legs[4].gamma,
            "leg4_tetta": self.legs[4].tetta,
        }

        self.angles_history.append(MoveSnapshot(move_type, angles))

    @property
    def sequence(self):
        sequence = []
        for move in self.angles_history:
            sequence.append(MoveSnapshot(move.move_type, convert_legs_angles(move.angles_snapshot)))
        return sequence
    
    @property
    def current_position(self):
        return self.angles_history[-1].angles_snapshot

    def initiate_legs(self):
        O1 = Point(cfg.leg["mount_point_offset"],
                   cfg.leg["mount_point_offset"],
                   self.legs_offset_v)
        D1 = Point(self.legs_offset_h_x - cfg.start["x_offset_body"],
                   self.legs_offset_h_y - cfg.start["y_offset_body"],
                   0)
        self.logger.info('[Init] Initiating leg 1')
        Leg1 = Leg(O1, D1)

        O2 = Point(cfg.leg["mount_point_offset"],
                   -cfg.leg["mount_point_offset"],
                   self.legs_offset_v)
        D2 = Point(self.legs_offset_h_x - cfg.start["x_offset_body"],
                   -self.legs_offset_h_y - cfg.start["y_offset_body"],
                   0)
        self.logger.info('[Init] Initiating leg 2')
        Leg2 = Leg(O2, D2)

        O3 = Point(-cfg.leg["mount_point_offset"],
                   -cfg.leg["mount_point_offset"],
                   self.legs_offset_v)
        D3 = Point(-self.legs_offset_h_x - cfg.start["x_offset_body"],
                   -self.legs_offset_h_y - cfg.start["y_offset_body"],
                   0)
        self.logger.info('[Init] Initiating leg 3')
        Leg3 = Leg(O3, D3)

        O4 = Point(-cfg.leg["mount_point_offset"],
                   cfg.leg["mount_point_offset"],
                   self.legs_offset_v)
        D4 = Point(-self.legs_offset_h_x - cfg.start["x_offset_body"],
                   self.legs_offset_h_y - cfg.start["y_offset_body"],
                   0)
        self.logger.info('[Init] Initiating leg 4')
        Leg4 = Leg(O4, D4)

        self.logger.info('[Init] Initialization successful')

        return {1: Leg1, 2: Leg2, 3: Leg3, 4: Leg4}

    def actualize_wheels(self):
        # method to adapt wheels position to current servos and changed mode
        self.add_angles_snapshot('endpoint')

    ################## MOVEMENTS START HERE ##################
    def leg_movement(self, leg_num, leg_delta):
        self.logger.info(f'Move. Leg {leg_num} for {leg_delta}')
        leg = self.legs[leg_num]

        leg.move_end_point(leg_delta[0], leg_delta[1], leg_delta[2])
        self.add_angles_snapshot('endpoint')

    def body_movement(self, delta_x, delta_y, delta_z, snapshot=True):
        self.logger.info(f'Body movement [{delta_x}, {delta_y}, {delta_z}]')
        if delta_x == delta_y == delta_z == 0:
            return

        for leg_num, leg in self.legs.items():
            self.logger.info(f'Moving mount point for {leg_num} : {[delta_x, delta_y, delta_z]}')
            leg.move_mount_point(delta_x, delta_y, delta_z)

        if snapshot:
            self.add_angles_snapshot('body')

    # ?
    def start(self):
        self.body_movement(0, 0, -cfg.start["vertical"] + cfg.start["initial_z_position_delta"])
        self.body_movement(0, 0, cfg.start["vertical"] - cfg.start["initial_z_position_delta"])
    
    # ?
    def reset(self):
        self.logger.info('Processing reset command')
        self.body_to_center()
        delta_z = self.legs[1].O.z - self.legs[1].D.z - cfg.start["vertical"]
        self.body_movement(0, 0, -delta_z)

    # ?
    def end(self):
        self.reset()
        self.body_movement(0, 0, -cfg.start["vertical"] + 
                                  cfg.start["initial_z_position_delta"])

    def go_to_height(self, height):
        delta_z = self.legs[1].O.z - self.legs[1].D.z - height
        self.body_movement(0, 0, -delta_z)

    def body_delta_xy(self, delta_y=cfg.start["y_offset_body"], delta_x=cfg.start["x_offset_body"]):
        # move body to center
        avg_o_x, avg_o_y, avg_d_x, avg_d_y = 0, 0, 0, 0
        for leg in self.legs.values():
            avg_o_x += leg.O.x
            avg_o_y += leg.O.y
            avg_d_x += leg.D.x
            avg_d_y += leg.D.y

        avg_o_x /= 4
        avg_o_y /= 4
        avg_d_x /= 4
        avg_d_y /= 4

        return [round(avg_o_x - avg_d_x - delta_x, 2),
                round(avg_o_y - avg_d_y - delta_y, 2)]
                           

    def body_to_center(self, delta_y=cfg.start["y_offset_body"], delta_x=cfg.start["x_offset_body"]):
        # move body to center
        
        body_delta_xy = self.body_delta_xy(delta_y, delta_x)
        self.logger.info(f'Moving body: {body_delta_xy}')
        self.body_movement(-body_delta_xy[0],
                           -body_delta_xy[1],
                           0)

    # body compensation for moving up one leg
    def target_body_position(self, leg_in_the_air_number, margin=cfg.margin):
        """
        provide the number of leg_in_the_air
        return target position of body to let the leg go into the air
        """

        # find intersection point of basement lines
        func1 = LinearFunc(self.legs[1].D, self.legs[3].D)
        func2 = LinearFunc(self.legs[2].D, self.legs[4].D)
        intersection = Point(*calculate_intersection(func1, func2), 0)

        target_leg_number_by_air_leg_number = {1: 3, 2: 4, 3: 1, 4: 2}
        target_leg_number = target_leg_number_by_air_leg_number[leg_in_the_air_number]
        target_leg = self.legs[target_leg_number]
        body_target_point = move_on_a_line(intersection,
                                           target_leg.D,
                                           margin)

        return body_target_point

    def body_compensation_for_a_leg(self, leg_num, margin=cfg.margin):        
        target = self.target_body_position(leg_num, margin)
        self.logger.info(f'Move. body_compensation_for_a_leg {leg_num}. Target : {target}')
        current_body_x = (self.legs[1].O.x +
                          self.legs[2].O.x +
                          self.legs[3].O.x +
                          self.legs[4].O.x) / 4

        current_body_y = (self.legs[1].O.y +
                          self.legs[2].O.y +
                          self.legs[3].O.y +
                          self.legs[4].O.y) / 4

        self.body_movement(target[0] - current_body_x,
                           target[1] - current_body_y,
                           0)

    def compensated_leg_movement(self, leg_num, leg_delta):
        # moving body to compensate future movement
        self.logger.info(f'Processing leg {leg_num} body_compensation_for_a_leg')
        self.body_compensation_for_a_leg(leg_num)

        self.logger.info(f'Processing leg {leg_num} move_end_point {leg_delta}')
        self.legs[leg_num].move_end_point(*leg_delta)
        self.add_angles_snapshot('endpoint')

    def leg_move_with_compensation(self, leg_num, delta_x, delta_y):
        self.compensated_leg_movement(leg_num, [0, 0, cfg.leg_up[1]])
        self.compensated_leg_movement(leg_num, [delta_x, delta_y, 0])
        self.logger.info(f'Processing leg {leg_num} move_end_point {[0, 0, -cfg.leg_up[1]]}')
        self.move_leg_endpoint(leg_num, [0, 0, -cfg.leg_up[1]])

    def leg_move_with_compensation_obstacled(self, leg_num, delta_x, delta_y, obstacle_z):
        self.obstacled_leg_up = cfg.leg_up[1] - 2
        self.logger.info(f'Move. leg_num = {leg_num}, delta_x = {delta_x}, delta_y = {delta_y}, obstacle_z = {obstacle_z}')
        self.logger.info(f'Move. Trying move for {[0, 0, self.obstacled_leg_up + obstacle_z]}')
        self.compensated_leg_movement(leg_num, [0, 0, self.obstacled_leg_up + obstacle_z])
        self.logger.info(f'Move. Trying move for {[delta_x, delta_y, 0]}')
        self.compensated_leg_movement(leg_num, [delta_x, delta_y, 0])

        self.logger.info(f'Move. Trying move for {-self.obstacled_leg_up}')
        self.move_leg_endpoint(leg_num, [0, 0, -self.obstacled_leg_up])
        self.logger.info('Move. Endpoint ok')

    def move_leg_endpoint(self, leg_num, leg_delta):        
        self.legs[leg_num].move_end_point(*leg_delta)
        #self.legs_deltas[leg_num] = [x + y for x, y in zip(self.legs_deltas[leg_num], leg_delta)]        
        self.add_angles_snapshot('endpoint')

    # 1-legged movements
    def move_body_straight(self, delta_x, delta_y, leg_seq=[2, 4, 1, 3]):
        for leg_number in leg_seq:
            self.logger.info(f'Processing leg {leg_number} with compensation')
            self.leg_move_with_compensation(leg_number, delta_x, delta_y)
        self.logger.info(f'Processing body to center')
        self.body_to_center()

    def two_legged_climbing_1(self, delta_x: int = 0, delta_y: int = 0):
        
        self.body_movement(0, -8, 0)

        self.legs[1].move_end_point(0, 0, 2.5*cfg.leg_up[2])
        #self.legs[3].move_end_point(delta_x, delta_y, cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')
        self.legs[1].move_end_point(delta_x, delta_y, 0)
        self.add_angles_snapshot('endpoints')

        #for leg in [self.legs[1], self.legs[3]]:
        #leg.move_end_point(0, 0, -cfg.leg_up[2])
        self.legs[1].move_end_point(0, 0, -1.5*cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')

        #self.legs[2].move_end_point(delta_x, delta_y, cfg.leg_up[2])
        self.legs[4].move_end_point(0, 0, 2.5*cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')
        self.legs[4].move_end_point(delta_x, delta_y, 0)
        self.add_angles_snapshot('endpoints')

        #for leg in [self.legs[2], self.legs[4]]:
        #leg.move_end_point(0, 0, -cfg.leg_up[2])
        self.legs[4].move_end_point(0, 0, -1.5*cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')

        #self.body_movement(round(delta_x, 1), round(delta_y, 1), 0)
        self.body_movement(round(delta_x, 1), round(delta_y, 1) + 8, cfg.leg_up[2])

    def two_legged_climbing_2(self, delta_x: int = 0, delta_y: int = 0):
        self.body_movement(round(delta_x / 2, 1), round(delta_y / 2, 1), 0)

        self.legs[1].move_end_point(delta_x, delta_y, cfg.leg_up[2])
        self.legs[3].move_end_point(delta_x, delta_y, 2*cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')

        for leg in [self.legs[1], self.legs[3]]:
            leg.move_end_point(0, 0, -cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')
        self.body_movement(round(delta_x / 2, 1), round(delta_y / 2, 1), 0)

        self.legs[2].move_end_point(delta_x, delta_y, 2*cfg.leg_up[2])
        self.legs[4].move_end_point(delta_x, delta_y, cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')

        for leg in [self.legs[2], self.legs[4]]:
            leg.move_end_point(0, 0, -cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')


    """
    Two phased moves
    """
    # phased 2-legged movement
    def move_2_legs_phased_13(self, delta_x: int = 0, delta_y: int = 0) -> None:
        self.body_movement(round(delta_x / 2, 1), round(delta_y / 2, 1), 0)

        for leg in [self.legs[1], self.legs[3]]:
            leg.move_end_point(delta_x, delta_y, cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')

        for leg in [self.legs[1], self.legs[3]]:
            leg.move_end_point(0, 0, -cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')
        
    def move_2_legs_phased_24(self, delta_x: int = 0, delta_y: int = 0) -> None:
        self.body_movement(round(delta_x / 2, 1), round(delta_y / 2, 1), 0)

        for leg in [self.legs[2], self.legs[4]]:
            leg.move_end_point(delta_x, delta_y, cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')

        for leg in [self.legs[2], self.legs[4]]:
            leg.move_end_point(0, 0, -cfg.leg_up[2])
        self.add_angles_snapshot('endpoints')      

    def reposition_legs(self, delta_x, delta_y):
        self.logger.info(f'reposition_legs ({delta_x}, {delta_y})')

        self.legs[2].move_end_point(delta_x, -delta_y, cfg.leg_up[1])
        self.legs[4].move_end_point(-delta_x, delta_y, cfg.leg_up[1])
        self.add_angles_snapshot('endpoints')
        self.logger.info(f'Legs 2-4 up')

        self.legs[2].move_end_point(0, 0, -cfg.leg_up[1])
        self.legs[4].move_end_point(0, 0, -cfg.leg_up[1])
        self.add_angles_snapshot('endpoints')
        self.logger.info(f'Legs 2-4 down')

        self.legs[1].move_end_point(delta_x, delta_y, cfg.leg_up[1])
        self.legs[3].move_end_point(-delta_x, -delta_y, cfg.leg_up[1])
        self.add_angles_snapshot('endpoints')
        self.logger.info(f'Legs 1-3 up')

        self.legs[1].move_end_point(0, 0, -cfg.leg_up[1])
        self.legs[3].move_end_point(0, 0, -cfg.leg_up[1])
        self.add_angles_snapshot('endpoints')
        self.logger.info(f'Legs 1-3 down')

    def climb_obstacle_1(self, step_len=8, obstacle_z=8):
        # self.body_movement(0, 0, obstacle_z)

        self.compensated_leg_movement(1, [0, 0, obstacle_z+3])
        self.legs[1].move_end_point(0, step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.legs[1].move_end_point(0, 0, -3)
        self.add_angles_snapshot('endpoint')

    def climb_obstacle_4(self, step_len=8, obstacle_z=8):
        delta = 0
        self.compensated_leg_movement(4, [-delta, -delta, obstacle_z+3])
        self.legs[4].move_end_point(0 + delta, step_len + delta, 0)
        self.add_angles_snapshot('endpoint')
        self.legs[4].move_end_point(0, 0, -3)
        self.add_angles_snapshot('endpoint')
        self.body_to_center()

        #self.climb_obstacle_2()

    def climb_obstacle_3(self, step_len=8, obstacle_z=8):
        #self.compensated_leg_movement(3, [0, 0, obstacle_z+3])
        self.body_movement(0, 0, 4)
        self.compensated_leg_movement(1, [0, 0, 6])
        self.legs[1].move_end_point(0, step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.legs[1].move_end_point(0, 0, -6)
        self.add_angles_snapshot('endpoint')

        self.compensated_leg_movement(4, [0, 0, 6])
        self.legs[4].move_end_point(0, -step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.legs[4].move_end_point(0, 0, -6)
        self.add_angles_snapshot('endpoint')

        self.body_movement(0, 0, -4)
        
        self.logger.info('wtf4')
        self.compensated_leg_movement(3, [0, 0, obstacle_z+3])
        self.logger.info('wtf5')
        self.legs[3].move_end_point(0, step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.logger.info('wtf7')
        self.legs[3].move_end_point(0, 0, -3)
        self.add_angles_snapshot('endpoint')

        self.body_movement(0, 0, 4)
        self.compensated_leg_movement(4, [0, 0, 6])
        self.legs[4].move_end_point(0, step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.legs[4].move_end_point(0, 0, -6)
        self.add_angles_snapshot('endpoint')
        self.body_to_center()
        self.body_movement(0, 0, -4)
        self.body_movement(0, 0, obstacle_z)
    
    def climb_obstacle_2(self, step_len=8, obstacle_z=8):
        #self.body_movement(0, 2, 0)
        self.compensated_leg_movement(1, [0, 0, 6])
        self.legs[1].move_end_point(0, -step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.legs[1].move_end_point(0, 0, -6)
        self.add_angles_snapshot('endpoint')

        """
        self.compensated_leg_movement(4, [0, 0, 6])
        self.legs[4].move_end_point(0, -step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.legs[4].move_end_point(0, 0, -6)
        self.add_angles_snapshot('endpoint')
        """

        self.logger.info('wtf0')
        self.compensated_leg_movement(2, [0, 0, obstacle_z+3])
        self.logger.info('wtf1')
        self.legs[2].move_end_point(0, step_len, 0)
        self.add_angles_snapshot('endpoint')
        self.logger.info('wtf2')
        self.legs[2].move_end_point(0, 0, -3)
        self.add_angles_snapshot('endpoint')
        self.logger.info('wtf3')
        

    def spear_up(self):
        self.leg_move_with_compensation(4, 12, 0)
        self.body_movement(0, -6, 0)
        self.legs[1].move_end_point(0, 5, 7)
        self.add_angles_snapshot('endpoint')
        self.legs[1].move_end_point(0, 15, 7)
        self.add_angles_snapshot('endpoint')
        #self.body_to_center()

    def spear_down(self):
        #self.compensated_leg_movement(1, [0, -15, -3])
        #self.compensated_leg_movement(1, [0, -5, -7])
        self.legs[1].move_end_point(0, -15, -7)
        self.add_angles_snapshot('endpoint')
        self.legs[1].move_end_point(0, -5, -7)
        self.add_angles_snapshot('endpoint')
        self.body_movement(0, 6, 0)
        self.leg_move_with_compensation(4, -12, 0)
        self.body_to_center()
        

if __name__ == '__main__':
    for step_len in [10, 11]:
        for obstacle_z in [13]:
            for v in [12, 13, 14, 15, 16]:
                for h_x in [13, 14, 15]:
                    for h_y in [13, 14, 15]:
                        try:
                            fk = DeviantKinematics(v, h_x, h_y)
                            fk.climb_obstacle(step_len, obstacle_z)
                            print(f'Success: {step_len}/{obstacle_z} {v}/{h_x}/{h_y}')
                        except:
                            pass
    
