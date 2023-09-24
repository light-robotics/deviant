leg = {
    "a": 7.4,    # PointA to PointB - femur
    "b": 8,    # PointB to PointC - femur-tibia
    "c": 16.1,   # PointC to PointD - tibia / point toe length
    "d": 7.5,    # PointO to PointA - trochanter-coxa
    "mount_point_offset": 5.16,
    "phi_angle" : 0, # angle correction if leg is not straight
    "wheely_angle" : -26, # 26, # angle correction for the wheel block
}

angles = {
    "to_surface": {
        "min" : -20,
        "max" : 20,
        "step": 2,
        "ideal": 0,
    },
    "alpha": {
        "min": -60,
        "max": 92,
        "ideal": 60,
    },
    "beta": {
        "min": -150,
        "max": 0,
        "ideal": -105,
    },
    "gamma": {
        "min": -90,
        "max": 0,
        "ideal": -45,
    },
    "delta": {
        "min": -45,
        "max": 45,
    },
    "tetta": {
        "min": -45,
        "max": 45,
    },
}

# car mode : 15-8-16
# spider mode : 13-16-16
# one legged : 13-14-14
start = {
    "vertical"                 : 18,
    "horizontal_x"             : 15,
    "horizontal_y"             : 15, 
    "x_offset_body"            : 0,
    "y_offset_body"            : -1,
    "initial_z_position_delta" : 10, # 3
}

modes = {
    "default":
        {
            "vertical"     : 13,
            "horizontal_x" : 16,
            "horizontal_y" : 16,           
        },
    "speed":
        {
            "vertical"     : 18,
            "horizontal_x" : 8,
            "horizontal_y" : 16,
        },
}

margin = 7

leg_up = {
    1: 6,
    2: 5
}

# movements
moves = {
    "up_or_down_cm"         : 2,
    "move_body_cm"          : 4,
    "forward_body_1_leg_cm" : 8,
    "forward_body_2_leg_cm" : 6,    
    #"reposition_cm"         : 1,
    #"side_look_angle"       : 12,
    #"vertical_look_angle"   : 30,
}