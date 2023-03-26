import math
import random

import arcade
import numpy as np

VELOCITY = 800
SIZE = 30
ACCELERATION = 500


class SmokeElement(arcade.SpriteSolidColor):
    def __init__(self, x, y, dest_x, dest_y):
        super(SmokeElement, self).__init__(width=SIZE, height=SIZE, color=arcade.color.WHITE)
        self.angle_tan = math.atan2(dest_y - y, dest_x - x)
        self.velocity = np.array([VELOCITY*(random.randint(90, 110)/100) * math.cos(self.angle_tan),
                                  VELOCITY*(random.randint(90, 110)/100) * math.sin(self.angle_tan)],
                                 dtype=float)
        self.center_x = x
        self.center_y = y
        self.position_current = np.array([x, y], dtype=float)
        self.position_old = np.array([x, y], dtype=float)
        self.time = random.randint(2, 4)
        self.acceleration = np.array([ACCELERATION * math.cos(self.angle_tan), ACCELERATION * math.sin(self.angle_tan)],
                                     dtype=float)

    def updateCenter(self):
        self.center_x = self.position_current[0]
        self.center_y = self.position_current[1]

    def updateVelocity(self, dt):
        if self.velocity[0] > 0:
            self.velocity -= self.acceleration * dt
        if self.velocity[0] <= random.randint(0, 600)/600:
            self.velocity[0] = 0
            self.velocity[1] = 0

    def update(self, dt=0):
        self.updateVelocity(dt)
        self.position_current += self.velocity * dt
        self.time -= dt
        self.updateCenter()

        # self.velocity = self.position_current - self.position_old
        # self.position_old = self.position_current
        # self.position_current = self.position_current + self.velocity + self.acceleration * dt * dt
        # self.updateCenter()

