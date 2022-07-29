from math import sin, cos
from box import Box, Pt
import numpy as np


class BoxEnv:
    """A simple 2D environment of interconnected boxes."""

    def __init__(self, x: float, y: float, theta: float, boxes: list[Box]) -> None:
        self.boxes = boxes
        self.x = x
        self.y = y
        self.angle = theta

    def move_forward(self, distance: float) -> None:
        new_x = self.x + distance * cos(self.angle)
        new_y = self.y + distance * sin(self.angle)
        self.move(new_x, new_y)

    def move_backward(self, distance: float) -> None:
        new_x = self.x - distance * cos(self.angle)
        new_y = self.y - distance * sin(self.angle)
        self.move(new_x, new_y)

    def move(self, new_x: float, new_y: float) -> None:

        if self.in_a_box(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            # TODO: project to boundary?
            raise NotImplemented

    def rotate_right(self, radians: float) -> None:
        self.angle -= radians

    def rotate_left(self, radians: float) -> None:
        self.angle -= radians

    def in_a_box(self, x: float, y: float) -> bool:

        for box in self.boxes:
            if box.point_is_inside(Pt(x, y)):
                return True

        return False

    def get_array_to_display(self) -> np.ndarray:
        raise NotImplemented
