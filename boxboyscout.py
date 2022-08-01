from box import Pt, dot
from boxenv import BoxEnv
from boxnavigatorbase import BoxNavigatorBase

from math import acos, cos, radians, sin


class BoxBoyScout(BoxNavigatorBase):
    def __init__(self, env: BoxEnv, pt: Pt, theta: float) -> None:
        super().__init__(env, pt, theta)

    def take_action(self) -> None:
        target_box = self.env.get_boxes(self.position)[0]

        # 1. Find the correct action
        heading_vector = Pt(cos(self.rotation), sin(self.rotation))
        target_vector = target_box.target - self.position
        scalar_product = dot(heading_vector, target_vector)

        angle_to_target = acos(
            scalar_product / (heading_vector.magnitude() * target_vector.magnitude())
        )

        # 2. Take the correct action
        if abs(angle_to_target) < radians(5):
            self.move_forward()
        elif angle_to_target > 0:
            self.rotate_left()
        else:
            self.rotate_right()
