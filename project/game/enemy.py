import arcade

ENEMY_SPEED = 1
class Enemy(arcade.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(filename=':resources:images/space_shooter/meteorGrey_med1.png', scale=0.5, center_x=x, center_y=y)

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of ENEMY_SPEED.
        """

        if self.center_y < player_sprite.center_y:
            self.center_y += min(ENEMY_SPEED, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(ENEMY_SPEED, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(ENEMY_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(ENEMY_SPEED, self.center_x - player_sprite.center_x)