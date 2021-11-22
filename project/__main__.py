import arcade

import os
from typing import cast

from game.mygame import InitGame
from game.joyconfigview import JoyConfigView


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Alpha"
MOVEMENT_SPEED = 4
BULLET_SPEED = 5
BULLET_COOLDOWN_TICKS = 10
ENEMY_SPAWN_INTERVAL = 1
ENEMY_SPEED = 1
JOY_DEADZONE = 0.2
# An angle of "0" means "right", but the player's texture is oriented in the "up" direction.
# So an offset is needed.
ROTATE_OFFSET = -90

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Set the working directory (where we expect to find files) to the same
    # directory this .py file is in. You can leave this out of your own
    # code, but it is needed to easily run the examples using "python -m"
    # as mentioned at the top of this program.
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

    window.joys = arcade.get_joysticks()
    for j in window.joys:
        j.open()
    joy_config_method_names = (
        ("Move the movement stick left or right", "move_stick_x"),
        ("Move the movement stick up or down", "move_stick_y"),
        ("Move the shooting stick left or right", "shoot_stick_x"),
        ("Move the shooting stick up or down", "shoot_stick_y"),
    )
    game = InitGame()
    window.show_view(JoyConfigView(joy_config_method_names, window.joys, game, SCREEN_WIDTH, SCREEN_HEIGHT))
    arcade.run()