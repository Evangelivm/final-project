import arcade, random,math
from game.player import Player
from game.enemy import Enemy
from game.game import Game as game
from typing import cast
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Alpha"
MOVEMENT_SPEED = 4
BULLET_SPEED = 10
BULLET_COOLDOWN_TICKS = 10
ENEMY_SPAWN_INTERVAL = 1
ENEMY_SPEED = 1
JOY_DEADZONE = 0.2
ROTATE_OFFSET = -90

class InitGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_music = arcade.load_sound("game\media\idea 1.wav")
        arcade.play_sound(self.background_music)
        self.game_over = False
        self.score = 0
        self.tick = 0
        self.bullet_cooldown = 0
        self.player = Player(":resources:images/space_shooter/playerShip1_green.png")
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.joy = None


    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE)
        joys = self.window.joys
        for joy in joys:
            game.dump_joystick(joy)
        if joys:
            self.joy = joys[0]
            print("Using joystick controls: {}".format(self.joy.device))
            arcade.window_commands.schedule(self.debug_joy_state, 0.1)
        if not self.joy:
            print("No joystick present, using keyboard controls")
        arcade.window_commands.schedule(self.spawn_enemy, ENEMY_SPAWN_INTERVAL)


    def debug_joy_state(self, _delta_time):
        game.dump_joystick_state(self.tick, self.joy)

    def spawn_enemy(self, _elapsed):
        if self.game_over:
            return
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        self.enemy_list.append(Enemy(x, y))

    def on_update(self, delta_time):
        self.tick += 1
        if self.game_over:
            return

        self.bullet_cooldown += 1

        for enemy in self.enemy_list:
            cast(Enemy, enemy).follow_sprite(self.player)

        if self.joy:
            # Joystick input - movement
            move_x, move_y, move_angle = game.get_joy_position(self.joy.move_stick_x, self.joy.move_stick_y)
            if move_angle:
                self.player.change_x = move_x * MOVEMENT_SPEED
                self.player.change_y = move_y * MOVEMENT_SPEED
                self.player.angle = move_angle + ROTATE_OFFSET
            else:
                self.player.change_x = 0
                self.player.change_y = 0

            # Joystick input - shooting
            shoot_x, shoot_y, shoot_angle = game.get_joy_position(self.joy.shoot_stick_x, self.joy.shoot_stick_y)
            if shoot_angle:
                self.spawn_bullet(shoot_angle)
        else:
            # Keyboard input - shooting
            if self.player.shoot_right_pressed and self.player.shoot_up_pressed:
                self.spawn_bullet(0 + 45)
            elif self.player.shoot_up_pressed and self.player.shoot_left_pressed:
                self.spawn_bullet(90 + 45)
            elif self.player.shoot_left_pressed and self.player.shoot_down_pressed:
                self.spawn_bullet(180 + 45)
            elif self.player.shoot_down_pressed and self.player.shoot_right_pressed:
                self.spawn_bullet(270 + 45)
            elif self.player.shoot_right_pressed:
                self.spawn_bullet(0)
            elif self.player.shoot_up_pressed:
                self.spawn_bullet(90)
            elif self.player.shoot_left_pressed:
                self.spawn_bullet(180)
            elif self.player.shoot_down_pressed:
                self.spawn_bullet(270)

        self.enemy_list.update()
        self.player.update()
        self.bullet_list.update()
        ship_death_hit_list = arcade.check_for_collision_with_list(self.player,
                                                                   self.enemy_list)
        if len(ship_death_hit_list) > 0:
            self.game_over = True
        for bullet in self.bullet_list:
            bullet_killed = False
            enemy_shot_list = arcade.check_for_collision_with_list(bullet,
                                                                   self.enemy_list)
            # Loop through each colliding sprite, remove it, and add to the score.
            for enemy in enemy_shot_list:
                enemy.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
                bullet_killed = True
                self.score += 1
            if bullet_killed:
                continue

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.shoot_right_pressed = True
        elif key == arcade.key.UP:
            self.player.shoot_up_pressed = True
        elif key == arcade.key.LEFT:
            self.player.shoot_left_pressed = True
        elif key == arcade.key.DOWN:
            self.player.shoot_down_pressed = True

        rad = math.atan2(self.player.change_y, self.player.change_x)
        self.player.angle = math.degrees(rad) + ROTATE_OFFSET

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.D:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player.shoot_right_pressed = False
        elif key == arcade.key.UP:
            self.player.shoot_up_pressed = False
        elif key == arcade.key.LEFT:
            self.player.shoot_left_pressed = False
        elif key == arcade.key.DOWN:
            self.player.shoot_down_pressed = False

        rad = math.atan2(self.player.change_y, self.player.change_x)
        self.player.angle = math.degrees(rad) + ROTATE_OFFSET

    def spawn_bullet(self, angle_in_deg):
        # only allow bullet to spawn on an interval
        if self.bullet_cooldown < BULLET_COOLDOWN_TICKS:
            return
        self.bullet_cooldown = 0

        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.75)

        # Position the bullet at the player's current location
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # angle the bullet visually
        bullet.angle = angle_in_deg
        angle_in_rad = math.radians(angle_in_deg)

        # set bullet's movement direction
        bullet.change_x = math.cos(angle_in_rad) * BULLET_SPEED
        bullet.change_y = math.sin(angle_in_rad) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_draw(self):
        # clear screen and start render process
        arcade.start_render()

        # draw game items
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.player.draw()

        # Put the score on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        # Game over message
        if self.game_over:
            arcade.draw_text("Sorry, Bad End",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2,
                             arcade.color.WHITE, 100,
                             width=SCREEN_WIDTH,
                             align="center",
                             anchor_x="center",
                             anchor_y="center")