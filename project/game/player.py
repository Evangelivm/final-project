import arcade
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class Player(arcade.sprite.Sprite):
    def __init__(self, filename):
        super().__init__(filename=filename, scale=0.4, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
        self.shoot_up_pressed = False
        self.shoot_down_pressed = False
        self.shoot_left_pressed = False
        self.shoot_right_pressed = False
