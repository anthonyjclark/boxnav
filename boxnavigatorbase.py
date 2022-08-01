from box import Pt
from boxenv import BoxEnv

import matplotlib.pyplot as plt

from math import cos, sin, radians


class BoxNavigatorBase:
    def __init__(self, env: BoxEnv, pt: Pt, theta: float) -> None:
        self.env = env
        self.position = pt
        self.rotation = theta

        self.translation_increment = 1
        self.rotation_increment = radians(2.5)

    def take_action(self) -> None:
        raise NotImplemented

    def move_forward(self) -> None:
        new_x = self.position.x + self.translation_increment * cos(self.rotation)
        new_y = self.position.y + self.translation_increment * sin(self.rotation)
        self.move(Pt(new_x, new_y))

    def move_backward(self) -> None:
        new_x = self.position.x - self.translation_increment * cos(self.rotation)
        new_y = self.position.y - self.translation_increment * sin(self.rotation)
        self.move(Pt(new_x, new_y))

    def move(self, new_pt: Pt) -> None:

        if self.env.get_boxes(new_pt):
            self.position = new_pt
        else:
            # TODO: project to boundary?
            raise NotImplemented

    def rotate_right(self) -> None:
        self.rotation -= self.rotation_increment

    def rotate_left(self) -> None:
        self.rotation -= self.rotation_increment

    def display(self, ax: plt.Axes, scale: float) -> None:

        # Plot agent as circle with heading arrow
        dx = scale * cos(self.rotation)
        dy = scale * sin(self.rotation)
        ax.arrow(self.position.x, self.position.y, dx, dy, color="r")
        ax.plot(self.position.x, self.position.y, "ro")

        # Plot target
        boxes_including_agent = self.env.get_boxes(self.position)
        for box in boxes_including_agent:
            dxy = (box.target - self.position).normalized() * scale
            ax.arrow(self.position.x, self.position.y, dxy.x, dxy.y, color="b")
            ax.plot(box.target.x, box.target.y, "bo")
