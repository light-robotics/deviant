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

speed = {
    "run" : 350,
    "hit" : 500,
}

moves = {
    "up_or_down_cm"         : 2,
    "move_body_cm"          : 7,
    "forward_body_1_leg_cm" : 8,
    "forward_body_2_leg_cm" : 8,    
    "reposition_cm"         : 1,
    "side_look_angle"       : 12,
    "vertical_look_angle"   : 30,
}

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


limits = {
    "body_forward"        : 7,
    "body_backward"       : 7,
    "body_sideways"       : 7,
    "side_look_angle"     : 24,
    "vertical_look_angle" : 30,
}

mode = 90
