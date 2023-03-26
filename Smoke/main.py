import math
import random

import arcade
import numpy as np

from smoke import SmokeElement

SRC_X = 100
SRC_Y = 400


class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title="Smoke", center_window=True)
        self.smokeElement = arcade.SpriteList()
        self.pressed = False
        self.dest = np.array([10, 10], dtype=float)
        self.src = arcade.SpriteCircle(radius=30, color=arcade.color.WHITE)
        self.src.center_x = SRC_X
        self.src.center_y = SRC_Y

    def update(self, dt):
        if self.pressed:
            self.smokeElement.append(
                SmokeElement(SRC_X + random.randint(-10, 10), SRC_Y + random.randint(-10, 10), self.dest[0],
                             self.dest[1]))
        for e in self.smokeElement:
            e.update(dt)
            if e.time <= 0:
                e.kill()

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.pressed = True
        self.dest[0] = x
        self.dest[1] = y

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.pressed = False

    def on_draw(self):
        arcade.start_render()
        self.src.draw()
        for e in self.smokeElement:
            e.draw()
        if len(self.smokeElement) > 0:
            arcade.draw_line(SRC_X, SRC_Y, SRC_X + 100 * math.cos(self.smokeElement[-1].angle_tan),
                             SRC_Y + 100 * math.sin(self.smokeElement[-1].angle_tan), arcade.color.RED, 5)


def main():
    game = Game(1200, 800)
    arcade.schedule(game.update, 1 / 60)
    arcade.run()


if __name__ == "__main__":
    main()
