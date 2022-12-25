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
        "min" : -90,
        "max" : 90,
        "step": 1,
        "ideal": 0,
    },
    "alpha": {
        "min": -60,
        "max": 55,
    },
    "beta": {
        "min": -90,
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
    "horizontal_x"             : 11,
    "horizontal_y"             : 11,
    "y_offset_body"            : 0,
    "initial_z_position_delta" : 5, # 3
}

margin = {
    1: 5,
    2: 6
}

leg_up = {
    1: 7,
    2: 4
}