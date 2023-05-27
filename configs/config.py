obstacle = {
    "danger_offset": 1.0,
    "outer_danger_offset": 2.0,
}

modes = {
    "run_mode" : {
        "horizontal_xy" : 16,
    },
    "sentry_mode" : {
        "horizontal_xy" : 16,
    },
    "walking_mode" : {
        "horizontal_xy" : 17,
    },
    "battle_mode" : {
        "horizontal_xy" : 17,
    }
}
"""
speed = {
    "run" : 350,
    "hit" : 500,
}
"""



deviant = {    
    # parameters for moving further, when moving with feedback
    "servos": {
        "diff_from_target_limit": 1.0,
        "diff_from_prev_limit": 0.25
    },
    # issue next command a little faster, than previous is finished executing
    # when moving without feedback
    "movement_command_advance_ms" : 0.05,
    "movement_overshoot_coefficient" : 0.2,
}

mode = 90
