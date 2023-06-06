import math
from functools import lru_cache
from typing import List

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from cybernetic_core.geometry.lines import Point
from cybernetic_core.cybernetic_utils.constraints import leg_angles_correct

import configs.kinematics_config as cfg
import configs.code_config as code_config
import logging.config


@lru_cache(maxsize=None)
def get_leg_angles(delta_x, delta_z, logger):
    possible_angles = find_angles(delta_x, delta_z, logger)

    return get_best_angles(possible_angles)

def find_angles(Dx, Dy, logger):
    a, b, c = cfg.leg["a"], cfg.leg["b"], cfg.leg["c"]
    results = []
    full_dist = math.sqrt(Dx ** 2 + Dy ** 2)
    if full_dist > a + b + c:
        raise Exception('No decisions. Full distance : {0}'.format(full_dist))

    for k in range(cfg.angles["to_surface"]["min"], 
                   cfg.angles["to_surface"]["max"],
                   cfg.angles["to_surface"]["step"]):

        ksi = math.radians(k)

        Cx = Dx + c * math.cos(math.pi / 2 + ksi)
        Cy = Dy + c * math.sin(math.pi / 2 + ksi)
        dist = math.sqrt(Cx ** 2 + Cy ** 2)

        if dist > a + b or dist < abs(a - b):
            pass
        else:
            alpha1 = math.acos((a ** 2 + dist ** 2 - b ** 2) / (2 * a * dist))
            beta1 = math.acos((a ** 2 + b ** 2 - dist ** 2) / (2 * a * b))
            beta = -1 * (math.pi - beta1)

            alpha2 = math.atan2(Cy, Cx)
            alpha = alpha1 + alpha2

            Bx = a * math.cos(alpha)
            By = a * math.sin(alpha)

            BD = math.sqrt((Dx - Bx) ** 2 + (Dy - By) ** 2)
            angle_C = math.acos((b ** 2 + c ** 2 - BD ** 2) / (2 * b * c))

            for coef in [-1, 1]:
                gamma = coef * (math.pi - angle_C)

                Cx = Bx + b * math.cos(alpha + beta)
                Cy = By + b * math.sin(alpha + beta)
                new_Dx = Cx + c * math.cos(alpha + beta + gamma)
                new_Dy = Cy + c * math.sin(alpha + beta + gamma)
                if abs(new_Dx - Dx) > 0.01 or abs(new_Dy - Dy) > 0.01:
                    continue
                    # only one of two coeffs is correct
                
                if leg_angles_correct(
                    alpha=math.degrees(alpha), 
                    beta=math.degrees(beta), 
                    gamma=math.degrees(gamma),
                    logger=logger
                ):
                    results.append([alpha, beta, gamma])

    return results

def calculate_leg_angles(O: Point, D: Point, logger):
    tetta = math.atan2(D.y - O.y, D.x - O.x)
    #print(tetta, math.degrees(tetta))
    if not leg_angles_correct(tetta=tetta, logger=logger):
        logger.info(f'Bad tetta : {tetta}')
        raise Exception(f'Bad tetta : {tetta}')

    A = Point(O.x + cfg.leg["d"] * math.cos(tetta),
                O.y + cfg.leg["d"] * math.sin(tetta),
                O.z)    

    l = round(math.sqrt((D.x - A.x) ** 2 + (D.y - A.y) ** 2), 2)
    delta_z = round(D.z - O.z, 2)
    # logger.info(f'Trying l {l} and delta_z {delta_z}')
    #logger.info(f'Leg Angles: {O} -> {D}')
    alpha, beta, gamma = get_leg_angles(l, delta_z, logger)
    #logger.info(f'Leg Angles: {[math.degrees(alpha), math.degrees(beta), math.degrees(gamma)]}')
    
    # logger.info(f'Success: (surf) {round(math.degrees(alpha+beta+gamma), 1)} | {round(math.degrees(alpha), 1)}, {round(math.degrees(beta), 1)}, {round(math.degrees(gamma), 1)}')

    """
    D_calculated = calculate_D_point(O, tetta, alpha, beta, gamma)

    if abs(D_calculated.x - D.x) > 0.01 or \
        abs(D_calculated.y - D.y) > 0.01 or \
        abs(D_calculated.z - D.z) > 0.01:
        logger.info(f'Exception in calculate_leg_angles. O: {O}, D: {D}')
        logger.info(f'{abs(D_calculated.x - D.x)}, {abs(D_calculated.y - D.y)}, {abs(D_calculated.z - D.z)}')
        raise Exception('D_prev far from D. Angles : {0}'
                        .format(([math.degrees(x) for x in [tetta, alpha, beta, gamma]])))
    """
    return tetta, alpha, beta, gamma

def calculate_D_point(O: Point, tetta: float, alpha: float, beta: float, gamma: float) -> Point:
    A = Point(O.x + cfg.leg["d"] * math.cos(tetta),
                O.y + cfg.leg["d"] * math.sin(tetta),
                O.z)
    
    B_xz = [cfg.leg["a"] * math.cos(alpha),
            cfg.leg["a"] * math.sin(alpha)]
    C_xz = [B_xz[0] + cfg.leg["b"] * math.cos(alpha + beta),
            B_xz[1] + cfg.leg["b"] * math.sin(alpha + beta)]
    D_xz = [C_xz[0] + cfg.leg["c"] * math.cos(alpha + beta + gamma),
            C_xz[1] + cfg.leg["c"] * math.sin(alpha + beta + gamma)]

    D = Point(round(A.x + D_xz[0] * math.cos(tetta), 2),
                    round(A.y + D_xz[0] * math.sin(tetta), 2),
                    round(A.z + D_xz[1], 2))
    #print(f'A: {A}, B: {B_xz}, C: {C_xz}, D: {D_xz}. D: {D}. tetta: {math.degrees(tetta)}, sin: {math.sin(tetta)}, cos: {math.cos(tetta)}')
    return D

def convert_gamma(gamma: float) -> float:
    gamma_converted = -round(math.degrees(gamma) - cfg.leg["phi_angle"], 2)
    return gamma_converted

def convert_gamma_back(gamma_converted: float) -> float:
    gamma_initial = -round(math.radians(gamma_converted + cfg.leg["phi_angle"]), 4)
    return gamma_initial

def convert_alpha(alpha: float) -> float:
    alpha_converted = -round(math.degrees(alpha), 2)
    return alpha_converted

def convert_alpha_back(alpha_converted: float) -> float:
    alpha_initial = -round(math.radians(alpha_converted), 4)
    return alpha_initial

def convert_beta(beta: float) -> float:
    beta_converted = round(math.degrees(beta), 2)
    return beta_converted

def convert_beta_back(beta_converted: float) -> float:
    beta_initial = round(math.radians(beta_converted), 4)
    return beta_initial

def convert_tetta(tetta: float, leg_number: int) -> float:
    # virtual model to real servos
    tetta_degrees = math.degrees(tetta)
    if leg_number == 1:
        tetta_degrees -= 45
    elif leg_number == 2:
        tetta_degrees += 45
    elif leg_number == 3:
        tetta_degrees += 135
    elif leg_number == 4:
        tetta_degrees -= 135
    
    if tetta_degrees > 120:
        print(f'Tetta converted {tetta_degrees} -> {tetta_degrees - 360}')
        tetta_degrees -= 360
    if tetta_degrees < -120:
        print(f'Tetta converted {tetta_degrees} -> {tetta_degrees + 360}')
        tetta_degrees += 360

    return round(tetta_degrees, 2)

def convert_tetta_back(tetta_degrees: float, leg_number: int) -> float:
    # real servos to virtual model    
    if leg_number == 1:
        tetta_degrees += 135
    elif leg_number == 2:
        tetta_degrees += 45
    elif leg_number == 3:
        tetta_degrees -= 45
    elif leg_number == 4:
        tetta_degrees -= 135
    
    return round(math.radians(tetta_degrees), 4)

# TODO: make a converted dispatcher
def convert_legs_angles(legs_angles: List[float]) -> List[float]:
    return {
        "leg1_tetta": convert_tetta(legs_angles["leg1_tetta"], 1),
        "leg1_alpha": convert_alpha(legs_angles["leg1_alpha"]),
        "leg1_beta" : convert_beta(legs_angles["leg1_beta"]),
        "leg1_gamma": convert_gamma(legs_angles["leg1_gamma"]),
        "leg2_tetta": convert_tetta(legs_angles["leg2_tetta"], 2),
        "leg2_alpha": convert_alpha(legs_angles["leg2_alpha"]),
        "leg2_beta" : convert_beta(legs_angles["leg2_beta"]),
        "leg2_gamma": convert_gamma(legs_angles["leg2_gamma"]),
        "leg3_tetta": convert_tetta(legs_angles["leg3_tetta"], 3),
        "leg3_alpha": convert_alpha(legs_angles["leg3_alpha"]),
        "leg3_beta" : convert_beta(legs_angles["leg3_beta"]),
        "leg3_gamma": convert_gamma(legs_angles["leg3_gamma"]),
        "leg4_tetta": convert_tetta(legs_angles["leg4_tetta"], 4),
        "leg4_alpha": convert_alpha(legs_angles["leg4_alpha"]),
        "leg4_beta" : convert_beta(legs_angles["leg4_beta"]),
        "leg4_gamma": convert_gamma(legs_angles["leg4_gamma"]),
    }

# TODO: REDO THAT
def convert_legs_angles_back(legs_angles_converted: List[float]) -> List[float]:
    # input: 16 angles in RADIANS
    # output: 16 converted angles in DEGREES
    # was gamma, beta, alpha, tetta one leg after another
    # now tetta, alpha, beta, gamma one leg after another
    angles_initial = [
        convert_tetta_back(legs_angles_converted[0], 1),
        convert_alpha_back(legs_angles_converted[1]),
        convert_beta_back(legs_angles_converted[2]),
        convert_gamma_back(legs_angles_converted[3]),
        convert_tetta_back(legs_angles_converted[4], 2),
        convert_alpha_back(legs_angles_converted[5]),
        convert_beta_back(legs_angles_converted[6]),
        convert_gamma_back(legs_angles_converted[7]),
        convert_tetta_back(legs_angles_converted[8], 3),
        convert_alpha_back(legs_angles_converted[9]),
        convert_beta_back(legs_angles_converted[10]),
        convert_gamma_back(legs_angles_converted[11]),
        convert_tetta_back(legs_angles_converted[12], 4),
        convert_alpha_back(legs_angles_converted[13]),
        convert_beta_back(legs_angles_converted[14]),
        convert_gamma_back(legs_angles_converted[15]),
    ]

    return angles_initial

def get_best_angles(all_angles):
    if len(all_angles) == 0:
        raise Exception('No angles')
    best_angles = min(all_angles, key=get_angles_distance)

    return best_angles

def get_angles_distance(angles):
    # 100 -> endleg leaning inside
    #return (math.degrees(angles[0] + angles[1] + angles[2]) + cfg.angles["to_surface"]["ideal"]) ** 2
    #print('------------------------------')
    #print(f'Alpha: {math.degrees(angles[0])}. Beta: {math.degrees(angles[1])}. Gamma: {math.degrees(angles[2])}')
    #old_value = (math.degrees(angles[0] + angles[1] + angles[2]) + cfg.angles["to_surface"]["ideal"]) ** 2
    new_value = 2 * abs(math.degrees(angles[0]) - cfg.angles["alpha"]["ideal"]) + \
           2 * abs(math.degrees(angles[1]) - cfg.angles["beta"]["ideal"]) + \
           2 * abs(math.degrees(angles[2]) - cfg.angles["gamma"]["ideal"]) + \
           4 * abs(math.degrees(angles[0] + angles[1] + angles[2]) + cfg.angles["to_surface"]["ideal"])
    #print(f'Old algorithm: {old_value}. New: {new_value}')
    return new_value

# ----------------------
# moves for Fenix
def get_angle_by_coords(x1, y1):
    l = math.sqrt(x1 ** 2 + y1 ** 2)
    initial_angle = math.asin(abs(y1) / l)
    if x1 >= 0 and y1 >= 0:
        return initial_angle
    if x1 >= 0 and y1 < 0:
        return 2 * math.pi - initial_angle
    if x1 < 0 and y1 >= 0:
        return math.pi - initial_angle
    if x1 < 0 and y1 < 0:
        return initial_angle + math.pi

def turn_on_angle(start_x, start_y, x1, y1, angle):
    print(f'x1, y1 : {round(x1, 2)}, {round(y1, 2)}')
    l = math.sqrt((x1 - start_x) ** 2 + (y1 - start_y) ** 2)
    initial_angle = get_angle_by_coords((x1 - start_x), (y1 - start_y))
    result_angle = angle + initial_angle
    print(f'{math.degrees(initial_angle)} -> {math.degrees(result_angle)}')

    return round(start_x + math.cos(result_angle) * l, 2), \
           round(start_y + math.sin(result_angle) * l, 2)

if __name__ == '__main__':
    logging.config.dictConfig(code_config.logger_config)
    logger = logging.getLogger('angles_logger')

    #alpha, beta, gamma = get_leg_angles(11.0, -8, logger)
    #logger.info(f'Success: (surf) {round(math.degrees(alpha+beta+gamma), 1)} | {round(math.degrees(alpha), 1)}, {round(math.degrees(beta), 1)}, {round(math.degrees(gamma), 1)}')
    calculate_leg_angles(O=Point(x=-17.25, y=-8.75, z=15), D=Point(x=-20.5, y=-12, z=0), logger=logger)

