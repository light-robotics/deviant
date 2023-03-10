import time
from enum import Enum
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware.dualshock import DualShock
from deviant_hardware.neopixel_commands_setter import NeopixelCommandsSetter
from run.commands_writer import CommandsWriter
import configs.config as cfg


class DeviantModes(Enum):
    CLIMBING  = 1
    RUN       = 2
    TURN      = 3
    OBSTACLES = 4

class DeviantDualShock(DualShock):
    """
    To execute neopixel commands run deviant/run/neopixel_commands_reader.py before running this
    To execute servo commands run deviant/run/movement_processor.py AFTER running this
    """
    def __init__(self):
        self.neopixel = NeopixelCommandsSetter()
        self.connect()
        self.light_on = False
        self.started = False
        self.mode = DeviantModes.RUN
        self.command_writer = CommandsWriter()
        self.command_writer.write_command('none', 1000)
        self.command_writer.write_wheels_command('forward', 0)

    def connect(self):
        self.neopixel.issue_command('rainbow_blue')
        super().__init__()
        self.neopixel.issue_command('blink_blue')        
        time.sleep(3)
        self.neopixel.issue_command('shutdown')

    def start(self):
        super().listen()

    def on_playstation_button_press(self):
        if self.started:
            self.started = False
            self.command_writer.write_command('end', 1000)
        else:
            self.started = True
            self.command_writer.write_command('start', 1000)
    
    def on_options_press(self):
        self.command_writer.write_command('exit', 0)
        time.sleep(0.5)
        self.command_writer.write_command('none', 1000)
    
    def on_share_press(self):
        self.command_writer.write_command('reset', 1000)

    def on_R1_press(self):
        if self.light_on:
            self.light_on = False
            self.neopixel.issue_command('light_off')
            print('Turn the lights off')
        else:
            self.light_on = True
            self.neopixel.issue_command('light_on')
            print('Turn the lights on')        
    
    def on_R2_press(self, value):
        if not self.light_on:
            # -32k to 32k -> 50 -> 255
            value1 = value + 32768
            value2 = int(50 + value1/320)
            print(value2)
            self.neopixel.issue_command('light', value=value2)
            print(f'Flashlight for {value} power')
    
    def on_R2_release(self):
        self.light_on = False
        self.neopixel.issue_command('light_off')
        print('Flashlight off')

    def on_L1_press(self):
        if self.light_on:
            self.light_on = False
            self.neopixel.issue_command('light_off')
            print('Turn the lights off')
        else:
            self.light_on = True
            self.neopixel.issue_command('dipped_headlights')
            print('Turn the dim lights on')   
    
    def on_L2_press(self, value):
        self.light_on = True
        self.neopixel.issue_command('rampage')
        print('Rampage')

    @staticmethod
    def convert_value_to_speed(value):
        """
        max_speed = 100, min_speed = 2000
        abs(value) from 0 to 32768
        """
        
        value = abs(value)
        if value < 12000:
            return 1500 # > 1000 will be ignored for moving
        """
        if value < 20000:
            return 400
        if value < 25000:
            return 300
        if value < 30000:
            return 250
        """
        return 1000

    @staticmethod
    def convert_value_to_wheels_speed(value):
        """
        max_speed = 1000, min_speed = 250
        abs(value) from 0 to 32768
        """
        
        value = abs(value)
        if value < 12000:
            return 250 # > 1000 will be ignored for moving
        if value < 20000:
            return 400
        if value < 25000:
            return 600
        if value < 30000:
            return 800

        return 1000
    
    def on_L3_up(self, value):
        if self.mode in [DeviantModes.RUN, DeviantModes.CLIMBING, DeviantModes.OBSTACLES]:
            self.command_writer.write_wheels_command('forward', self.convert_value_to_wheels_speed(value))
        elif self.mode == DeviantModes.TURN:
            self.command_writer.write_wheels_command('turn', self.convert_value_to_wheels_speed(value))
    
    def on_L3_down(self, value):
        if self.mode in [DeviantModes.RUN, DeviantModes.CLIMBING, DeviantModes.OBSTACLES]:
            self.command_writer.write_wheels_command('backwards', self.convert_value_to_wheels_speed(value))
        elif self.mode == DeviantModes.TURN:
            self.command_writer.write_wheels_command('turn_ccw', self.convert_value_to_wheels_speed(value))

    def on_L3_left(self, value):
        pass

    def on_L3_right(self, value):
        pass
    
    def on_L3_press(self):
        pass
    
    def on_L3_y_at_rest(self):
        self.command_writer.write_command('none', 250)
        if self.mode in [DeviantModes.RUN, DeviantModes.CLIMBING, DeviantModes.OBSTACLES]:
            self.command_writer.write_wheels_command('forward', 0)
        elif self.mode == DeviantModes.TURN:
            self.command_writer.write_wheels_command('turn', 0)

    def on_L3_x_at_rest(self):
        self.command_writer.write_command('none', 250)
        if self.mode in [DeviantModes.RUN, DeviantModes.CLIMBING, DeviantModes.OBSTACLES]:
            self.command_writer.write_wheels_command('forward', 0)
        if self.mode == DeviantModes.TURN:
            self.command_writer.write_wheels_command('turn', 0)
    
    def on_R3_up(self, value):
        if self.mode in [DeviantModes.RUN, DeviantModes.CLIMBING]:
            self.command_writer.write_command('forward_two_legged', 250)
    
    def on_R3_down(self, value):
        pass
    
    def on_R3_left(self, value):
        pass
    
    def on_R3_right(self, value):
        pass

    def on_R3_press(self):
        pass
    
    def on_R3_y_at_rest(self):
        self.command_writer.write_command('none', 250)
    
    def on_R3_x_at_rest(self):
        self.command_writer.write_command('none', 250)

    def on_right_arrow_press(self):
        if self.mode in [DeviantModes.OBSTACLES]:
            self.command_writer.write_command('reposition_wider', 500)

    def on_left_arrow_press(self):
        if self.mode in [DeviantModes.OBSTACLES]:
            self.command_writer.write_command('reposition_narrower', 500)
      
    def on_up_arrow_press(self):
        if self.mode in [DeviantModes.RUN, DeviantModes.OBSTACLES]:
            self.command_writer.write_command('up', 1000)
        elif self.mode == DeviantModes.TURN:
            self.command_writer.write_command('up_6', 1000)
        elif self.mode == DeviantModes.CLIMBING:
            self.command_writer.write_command('climb_12_1', 1000)

    def on_down_arrow_press(self):
        if self.mode in [DeviantModes.RUN, DeviantModes.CLIMBING, DeviantModes.OBSTACLES]:
            self.command_writer.write_command('down', 1000)
        elif self.mode == DeviantModes.TURN:
            self.command_writer.write_command('down_6', 1000)

    def on_up_down_arrow_release(self):
        self.command_writer.write_command('none', 500)
        
    def on_x_press(self):
        self.mode = DeviantModes.OBSTACLES
        self.neopixel.issue_command('steady', color='purple')
        self.command_writer.write_wheels_command('forward', 0)
        self.command_writer.write_command('actualize_wheels', 300)
        print('Switched mode to OBSTACLES')

    def on_triangle_press(self):
        self.mode = DeviantModes.RUN
        self.neopixel.issue_command('steady', color='cyan')
        self.command_writer.write_wheels_command('forward', 0)
        self.command_writer.write_command('actualize_wheels', 300)
        print('Switched mode to RUN')

    def on_circle_press(self):
        self.mode = DeviantModes.TURN
        self.neopixel.issue_command('steady', color='green')
        self.command_writer.write_wheels_command('turn', 0)
        self.command_writer.write_command('actualize_wheels', 300)
        print('Switched mode to TURN')

    def on_square_press(self):
        self.mode = DeviantModes.CLIMBING
        self.neopixel.issue_command('steady', color='blue')    
        self.command_writer.write_wheels_command('forward', 0)
        self.command_writer.write_command('actualize_wheels', 300)
        print('Switched mode to CLIMBING')

if __name__ == '__main__':
    DeviantDualShock().start()
