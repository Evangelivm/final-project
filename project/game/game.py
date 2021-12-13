import math
import pprint

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Space Xcape"
MOVEMENT_SPEED = 4
BULLET_SPEED = 10
BULLET_COOLDOWN_TICKS = 10
ENEMY_SPAWN_INTERVAL = 1
ENEMY_SPEED = 1
JOY_DEADZONE = 0.2
ROTATE_OFFSET = -90

class Game():
    def dump_obj(obj):
        for key in sorted(vars(obj)):
            val = getattr(obj, key)
            print("{:30} = {} ({})".format(key, val, type(val).__name__))


    def dump_joystick(joy):
        print("========== {}".format(joy))
        print("x       {}".format(joy.x))
        print("y       {}".format(joy.y))
        print("z       {}".format(joy.z))
        print("rx      {}".format(joy.rx))
        print("ry      {}".format(joy.ry))
        print("rz      {}".format(joy.rz))
        print("hat_x   {}".format(joy.hat_x))
        print("hat_y   {}".format(joy.hat_y))
        print("buttons {}".format(joy.buttons))
        print("========== Extra joy")
        print("========== pprint joy")
        pprint.pprint(joy)
        print("========== pprint joy.device")
        pprint.pprint(joy.device)


    def dump_joystick_state(ticks, joy):
        fmt_str = "{:6d} "
        num_fmts = ["{:5.2f}"] * 6
        fmt_str += " ".join(num_fmts)
        fmt_str += " {:2d} {:2d} {}"
        buttons = " ".join(["{:5}".format(str(b)) for b in joy.buttons])
        print(fmt_str.format(ticks,
                            joy.x,
                            joy.y,
                            joy.z,
                            joy.rx,
                            joy.ry,
                            joy.rz,
                            joy.hat_x,
                            joy.hat_y,
                            buttons))


    def get_joy_position(x, y):
        """Given position of joystick axes, return (x, y, angle_in_degrees).
        If movement is not outside of deadzone, return (None, None, None)"""
        if x > JOY_DEADZONE or x < -JOY_DEADZONE or y > JOY_DEADZONE or y < -JOY_DEADZONE:
            y = -y
            rad = math.atan2(y, x)
            angle = math.degrees(rad)
            return x, y, angle
        return None, None, None
