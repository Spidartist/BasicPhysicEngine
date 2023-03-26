import math
import random

import arcade
import numpy as np

VELOCITY = 900
SIZE = 256
ACCELERATION = 500


class SmokeElement(arcade.Sprite):
    def __init__(self, x, y, dest_x, dest_y):
        super(SmokeElement, self).__init__(filename="smoke.png", image_width=SIZE, image_height=SIZE, scale=0.02)
        self.angle_tan = math.atan2(dest_y - y, dest_x - x)
        self.velocity = np.array([VELOCITY*(random.randint(90, 110)/100) * math.cos(self.angle_tan),
                                  VELOCITY*(random.randint(90, 110)/100) * math.sin(self.angle_tan)],
                                 dtype=float)
        self.center_x = x
        self.center_y = y
        self.alpha = 40
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

    def updateAngle(self):
        self.angle += 0.5

    def updateScale(self):
        if self.scale < 1:
            self.scale += 0.03
        else:
            self.scale += 0.008

    def updateAlpha(self):
        if self.alpha > 10:
            self.alpha -= 3

    def update(self, dt=1/100):
        self.updateVelocity(dt)
        self.updateAlpha()
        self.updateScale()
        self.updateAngle()
        self.position_current += self.velocity * dt
        self.time -= dt
        self.updateCenter()

        # self.velocity = self.position_current - self.position_old
        # self.position_old = self.position_current
        # self.position_current = self.position_current + self.velocity + self.acceleration * dt * dt
        # self.updateCenter()

