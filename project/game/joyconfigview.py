import arcade,time
import pyglet.input.base
class JoyConfigView(arcade.View):
    """A View that allows a user to interactively configure their joystick"""
    REGISTRATION_PAUSE = 1.5
    NO_JOYSTICK_PAUSE = 2.0
    JOY_ATTRS = ("x", "y", "z", "rx", "ry", "rz")

    def __init__(self, joy_method_names, joysticks, next_view, width, height):
        super().__init__()
        self.next_view = next_view
        self.width = width
        self.height = height
        self.msg = ""
        self.script = self.joy_config_script()
        self.joys = joysticks
        arcade.set_background_color(arcade.color.WHITE)
        if len(joysticks) > 0:
            self.joy = joysticks[0]
            self.joy_method_names = joy_method_names
            self.axis_ranges = {}

    def config_axis(self, joy_axis_label, method_name):
        self.msg = joy_axis_label
        self.axis_ranges = {a: 0.0 for a in self.JOY_ATTRS}
        while max([v for k, v in self.axis_ranges.items()]) < 0.85:
            for attr, farthest_val in self.axis_ranges.items():
                cur_val = getattr(self.joy, attr)
                if abs(cur_val) > abs(farthest_val):
                    self.axis_ranges[attr] = abs(cur_val)
            yield

        max_val = 0.0
        max_attr = None
        for attr, farthest_val in self.axis_ranges.items():
            if farthest_val > max_val:
                max_attr = attr
                max_val = farthest_val
        self.msg = "Registered!"

        setattr(pyglet.input.base.Joystick, method_name, property(lambda that: getattr(that, max_attr), None))

        # pause briefly after registering an axis
        yield from self._pause(self.REGISTRATION_PAUSE)

    def joy_config_script(self):
        if len(self.joys) == 0:
            self.msg = "This is a Alpha Release."
            yield from self._pause(self.NO_JOYSTICK_PAUSE)
            return

        for joy_axis_label, method_name in self.joy_method_names:
            yield from self.config_axis(joy_axis_label, method_name)

    def on_update(self, delta_time):
        try:
            next(self.script)
        except StopIteration:
            self.window.show_view(self.next_view)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("use W,A,S and D to move, and arrows for shoot", self.width / 2, self.height / 2 + 100,
                         arcade.color.BLACK, font_size=32, anchor_x="center")
        arcade.draw_text(self.msg, self.width / 2, self.height / 2,
                         arcade.color.BLACK, font_size=24, anchor_x="center")

    def _pause(self, delay):
        """Block a generator from advancing for the given delay. Call with 'yield from self._pause(1.0)"""
        start = time.time()
        end = start + delay
        while time.time() < end:
            yield