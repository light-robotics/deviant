import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybernetic_core.kinematics import DeviantKinematics

goods = []
for body_up in range(3, 15):
    for step_len in range(10, 15):
        for narrowing_len in range(5, 15):
            try:
                dk = DeviantKinematics()
                dk.climb_obstacle(10, step_len=step_len, narrowing_len=narrowing_len, initial_body_movement_up=body_up)
                goods.append([body_up, step_len, narrowing_len])
            except Exception as e:
                print(f'BodyUp {body_up} failed. {e}')
            
print(f'Goods: {goods}')
