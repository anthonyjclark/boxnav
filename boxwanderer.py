from box import Pt
from boxenv import BoxEnv
from boxnavigatorbase import BoxNavigatorBase


class BoxWanderer(BoxNavigatorBase):
    def __init__(self, env: BoxEnv, pt: Pt, theta: float) -> None:
        super().__init__(env, pt, theta)

    def take_action(self) -> None:
        """
        While not at target
            get direction to target
            rotate if outside cone
            otherwise, step toward target
        """
        ...
