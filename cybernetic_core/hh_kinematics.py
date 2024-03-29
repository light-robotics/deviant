import logging.config
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import configs.code_config as code_config
import configs.kinematics_config as cfg
from cybernetic_core.geometry.inverse_kinematics import calculate_leg_angles
from cybernetic_core.geometry.lines import Point
from cybernetic_core.cybernetic_utils.moves import Move, MoveSnapshot


class Leg:
    def __init__(self, O: Point, C: Point):
        logging.config.dictConfig(code_config.logger_config)
        self.logger = logging.getLogger('angles_logger') #logging.getLogger('main_logger')
        self.O = O
        self.C = C
        self.update_angles()

    def update_angles(self):
        self.tetta, self.alpha, self.beta = calculate_leg_angles(self.O, self.C)

    def move_mount_point(self, delta_x, delta_y, delta_z):
        self.O.move(delta_x, delta_y, delta_z)
        self.update_angles()
    
    def move_end_point(self, delta_x, delta_y, delta_z):
        self.C.move(delta_x, delta_y, delta_z)
        self.update_angles()

class HHKinematics:
    def __init__(self):
        logging.config.dictConfig(code_config.logger_config)
        self.logger = logging.getLogger('main_logger')
        self.legs = self.initiate_legs()
        self.angles_history = []
        self.add_angles_snapshot('init')

    def add_angles_snapshot(self, move_type: str = 'unknown'):
        angles = {
            "leg1_alpha": self.legs[1].alpha,
            "leg1_beta": self.legs[1].beta,
            "leg1_tetta": self.legs[1].tetta,
            "leg2_alpha": self.legs[2].alpha,
            "leg2_beta": self.legs[2].beta,
            "leg2_tetta": self.legs[2].tetta,
            "leg3_alpha": self.legs[3].alpha,
            "leg3_beta": self.legs[3].beta,
            "leg3_tetta": self.legs[3].tetta,
            "leg4_alpha": self.legs[4].alpha,
            "leg4_beta": self.legs[4].beta,
            "leg4_tetta": self.legs[4].tetta,
        }

        self.angles_history.append(MoveSnapshot(move_type, angles))

    def reset_history(self):
        self.angles_history = []

    @property
    def sequence(self):
        sequence = []
        for move in self.angles_history:
            sequence.append(MoveSnapshot(move.move_type, move.angles_snapshot))
        return sequence

    def initiate_legs(self):
        O1 = Point(0, 0, cfg.start.vertical)
        D1 = Point(0, cfg.leg.d, 0)
        self.logger.info('[Init] Initiating leg 1')
        Leg1 = Leg(O1, D1)

        O2 = Point(0, 0, cfg.start.vertical)
        D2 = Point(0, cfg.leg.d, 0)
        self.logger.info('[Init] Initiating leg 2')
        Leg2 = Leg(O2, D2)

        O3 = Point(0, 0, cfg.start.vertical)
        D3 = Point(0, cfg.leg.d, 0)
        self.logger.info('[Init] Initiating leg 3')
        Leg3 = Leg(O3, D3)

        O4 = Point(0, 0, cfg.start.vertical)
        D4 = Point(0, cfg.leg.d, 0)
        self.logger.info('[Init] Initiating leg 4')
        Leg4 = Leg(O4, D4)

        self.logger.info('[Init] Initialization successful')

        return {1: Leg1, 2: Leg2, 3: Leg3, 4: Leg4}

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


if __name__ == '__main__':
    hh_kin = HHKinematics()
    hh_kin.body_movement(5, 0, 0)
    print(hh_kin.sequence)
