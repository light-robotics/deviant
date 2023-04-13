leg = {
    "a": 11,    # PointA to PointB - femur
    "b": 8,    # PointB to PointC - femur-tibia
    "c": 20,   # PointC to PointD - tibia / point toe length
    "d": 7.5,    # PointO to PointA - trochanter-coxa
    "mount_point_offset": 5.16,
    "phi_angle" : 0 # angle correction for the wheel block
}

angles = {
    "to_surface": {
        "min" : -80,
        "max" : 80,
        "step": 5,
        "ideal": 0,
    },
    "alpha": {
        "min": -60,
        "max": 83,
    },
    "beta": {
        "min": -150,
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
    "vertical"                 : 18,
    "horizontal_x"             : 16,
    "horizontal_y"             : 16,
    "x_offset_body"            : 0,
    "initial_z_position_delta" : 10, # 3
}

margin = 6

leg_up = {
    1: 5,
    2: 7
}
