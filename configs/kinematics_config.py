leg = {
    "a": 6.9,    # PointA to PointB - femur
    "b": 8.6,    # PointB to PointC - femur-tibia
    "c": 13.9,   # PointC to PointD - tibia / point toe length
    "d": 6.0,    # PointO to PointA - trochanter-coxa
    "mount_point_offset": 3.8,
    "phi_angle" : 14.1 # angle correction for the wheel block
}

angles = {
    "to_surface": {
        "min" : -30,
        "max" : 30,
        "step": 5,
        "ideal": 0,
    },
    "alpha": {
        "min": -60,
        "max": 73,
    },
    "beta": {
        "min": -125,
        "max": 0,
    },
    "gamma": {
        "min": -90,
        "max": 0,
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

start = {
    "vertical"                 : 15,
    "horizontal_x"             : 14,
    "horizontal_y"             : 14,
    "x_offset_body"            : 0.5,
    "initial_z_position_delta" : 5, # 3
}

margin = 7

leg_up = {
    1: 6,
    2: 5
}
