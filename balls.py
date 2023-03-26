import timeit

import arcade
import numpy as np

RADIUS = 10
MAX_BALLS = 0


class VerletObject(arcade.SpriteCircle):
    def __init__(self, x, y, color, radius):
        super().__init__(radius=radius, color=color)
        self.center_x = x
        self.center_y = y
        self.position_current = np.array([x, y], dtype=float)
        self.position_old = np.array([x, y], dtype=float)
        self.acceleration = np.array([0, 0], dtype=float)
        self.movable = True

    def updateCenter(self):
        self.center_x = self.position_current[0]
        self.center_y = self.position_current[1]

    def update(self, dt=0):
        velocity = self.position_current - self.position_old
        self.position_old = self.position_current
        self.position_current = self.position_current + velocity + self.acceleration * dt * dt
        self.updateCenter()
        self.acceleration = np.array([0, 0], dtype=float)

    def accelerate(self, acc):
        self.acceleration += acc


class Link:
    def __init__(self):
        self.objs = arcade.SpriteList()
        self.objs.append(VerletObject(300, 400, arcade.color.WHITE, RADIUS))
        self.objs.append(VerletObject(300 + RADIUS * 2, 400, arcade.color.WHITE, RADIUS))
        self.objs.append(VerletObject(300 + RADIUS * 4, 400, arcade.color.WHITE, RADIUS))
        self.objs.append(VerletObject(300 + RADIUS * 6, 400, arcade.color.WHITE, RADIUS))
        self.objs.append(VerletObject(300 + RADIUS * 8, 400, arcade.color.WHITE, RADIUS))
        self.target_dist = RADIUS*2+3

    def apply(self):
        for i in range(len(self.objs)):
            for k in range(i+1, len(self.objs)):
                if k == i+1:
                    axis = self.objs[i].position_current - self.objs[k].position_current
                    dist = Game.calDistance(axis)
                    n = axis / dist
                    delta = self.target_dist - dist
                    # self.objs[i].position_current += 0.5 * delta * n
                    # self.objs[i].updateCenter()
                    self.objs[k].position_current -= 0.5 * delta * n
                    self.objs[k].updateCenter()



class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title="Balls", center_window=True)
        self.gravity = np.array([0, -500], dtype=float)
        self.balls = arcade.SpriteList()
        self.cnt_time = 0
        self.link = Link()

    def update(self, dt):
        sub_steps = 8
        sub_dt = dt / sub_steps
        for i in range(sub_steps):
            self.cnt_time += 1
            # total_program_time = int(timeit.default_timer() - self.program_start_time)
            if self.cnt_time % 2 == 0 and len(self.balls) < MAX_BALLS:
                self.balls.append(VerletObject(600, 400, arcade.color.WHITE, RADIUS))
            self.applyGravity()
            self.link.apply()
            self.applyConstraint()
            self.solveCollision()
            self.updatePositions(sub_dt)

    def updatePositions(self, dt):
        for i in range(len(self.link.objs)):
            self.link.objs[i].update(dt)
        for ball in self.balls:
            ball.update(dt)

    def applyGravity(self):
        for i in range(len(self.link.objs)):
            if i > 0:
                self.link.objs[i].accelerate(self.gravity)

        for ball in self.balls:
            ball.accelerate(self.gravity)

    @staticmethod
    def calDistance(inVec):
        return np.sqrt(np.square(inVec[0]) + np.square(inVec[1]))

    def applyConstraint(self):
        position = np.array([400, 400], dtype=float)
        radius = 300
        for i in range(len(self.link.objs)):
            to_obj = self.link.objs[i].position_current - position
            dist = Game.calDistance(to_obj)
            if dist > (radius - RADIUS):
                n = to_obj / dist
                self.link.objs[i].position_current = position + n * (radius - RADIUS)
                self.link.objs[i].updateCenter()
        for ball in self.balls:
            to_obj = ball.position_current - position
            dist = Game.calDistance(to_obj)
            if dist > (radius - RADIUS):
                n = to_obj / dist
                ball.position_current = position + n * (radius - RADIUS)
                ball.updateCenter()

    def solveCollision(self):
        cnt_ball = len(self.balls)
        min_dist = 2 * RADIUS
        for i in range(len(self.link.objs)):
            for k in range(i + 2, len(self.link.objs)):
                collision_axis = self.link.objs[i].position_current - self.link.objs[k].position_current
                dist = Game.calDistance(collision_axis)
                if dist < min_dist:
                    n = collision_axis / dist
                    delta = 0.5 * 0.75 * (min_dist - dist)
                    self.link.objs[i].position_current += delta * n
                    self.link.objs[i].updateCenter()
                    self.link.objs[k].position_current -= delta * n
                    self.link.objs[k].updateCenter()
        for i in range(0, cnt_ball):
            for k in range(i + 1, cnt_ball):
                collision_axis = self.balls[i].position_current - self.balls[k].position_current
                dist = Game.calDistance(collision_axis)
                if dist < min_dist:
                    n = collision_axis / dist
                    delta = 0.5 * 0.75 * (min_dist - dist)
                    self.balls[i].position_current += delta * n
                    self.balls[i].updateCenter()
                    self.balls[k].position_current -= delta * n
                    self.balls[k].updateCenter()

    def on_draw(self):
        # Start rendering and draw all the objects
        arcade.start_render()
        arcade.draw_circle_filled(400, 400, 300, color=arcade.color.BLACK)
        for ball in self.balls:
            ball.draw()
        for i in range(len(self.link.objs)):
            self.link.objs[i].draw()


def main():
    game = Game(800, 800)
    game.background_color = arcade.color.GRAY
    arcade.run()


if __name__ == "__main__":
    main()
