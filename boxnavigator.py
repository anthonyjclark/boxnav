from box import Pt
from boxenv import BoxEnv
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Wedge
from enum import Enum
from math import sin, cos, degrees, radians


def close_enough(A: Pt, B: Pt, threshold: float = 1) -> bool:
    """Determine whether Pt A is close enough to Pt B depending on the threshold value.

    Args:
        A (Pt): First Pt to compare
        B (Pt): Second Pt to compare
        threshold (float, optional): How close Pt A has to be to Pt B to be considered "close enough". Defaults to 1.

    Returns:
        bool: Is Pt A close enough to Pt B given a threshold
    """
    # TODO: find good threshold value
    distance = (A - B).magnitude()
    return distance < threshold


class Action(Enum):
    """Simple class with 4 possible actions."""

    FORWARD = 0
    BACKWARD = 1
    ROTATE_LEFT = 2
    ROTATE_RIGHT = 3


class BoxNavigatorBase:
    """Base class for box navigators."""

    def __init__(self, position: Pt, rotation: float, env: BoxEnv) -> None:
        """Initialize member variables for any navigator.

        Args:
            position (Pt): initial position
            rotation (float): initial rotation
            env (BoxEnv): box environment
        """
        self.env = env
        self.position = position
        self.rotation = rotation

        self.target = self.env.boxes[0].target
        self.half_target_wedge = radians(5)

        self.translation_increment = 1
        self.rotation_increment = radians(2.5)

    def at_final_target(self) -> bool:
        """Is the navigator at the target for the box it is in."""
        return close_enough(self.position, self.env.boxes[-1].target)

    def take_action(self) -> tuple[Action, Action]:
        """Execute a single action in the environment.

        Raises:
            NotImplemented: implement in child classes.

        Returns:
            tuple[Action, Action]: return action taken and correct action.
        """
        raise NotImplemented

    def move_forward(self) -> None:
        """Move forward by a set amount."""
        new_x = self.position.x + self.translation_increment * cos(self.rotation)
        new_y = self.position.y + self.translation_increment * sin(self.rotation)
        self.move(Pt(new_x, new_y))

    def move_backward(self) -> None:
        """Move backward by a set amount."""
        new_x = self.position.x - self.translation_increment * cos(self.rotation)
        new_y = self.position.y - self.translation_increment * sin(self.rotation)
        self.move(Pt(new_x, new_y))

    def move(self, new_pt: Pt) -> None:
        """Jump to the given position if it is within a box.

        Args:
            new_pt (Pt): new position

        Raises:
            NotImplemented: position is not valid
        """

        if self.env.get_boxes(new_pt):
            self.position = new_pt
        else:
            # TODO: project to boundary?
            raise NotImplemented

    def rotate_right(self) -> None:
        """Rotate to the right by a set amount."""
        self.rotation -= self.rotation_increment

    def rotate_left(self) -> None:
        """Rotate to the left by a set amount."""
        self.rotation += self.rotation_increment

    def display(self, ax: plt.Axes, scale: float) -> None:
        """Plot the agent to the given axis.

        Args:
            ax (plt.Axes): axis for plotting
            scale (float): scale of arrows
        """

        # Plot agent and agent's heading
        ax.plot(self.position.x, self.position.y, "ro")
        wedge_lo = degrees(self.rotation - self.half_target_wedge)
        wedge_hi = degrees(self.rotation + self.half_target_wedge)
        ax.add_patch(Wedge(self.position.xy(), scale, wedge_lo, wedge_hi, color="red"))

        # Plot target and line to target
        ax.plot(self.target.x, self.target.y, "bo")
        dxy = (self.target - self.position).normalized() * scale
        ax.add_patch(Arrow(self.position.x, self.position.y, dxy.x, dxy.y, color="b"))


class PerfectNavigator(BoxNavigatorBase):
    """A "perfect" navigator that does not make mistakes."""

    def __init__(self, position: Pt, rotation: float, env: BoxEnv) -> None:
        """Initialize navigator position, initial orientation, and associated Box environment.

        Args:
            position (Pt): Initial x,y Coordinate for navigator
            rotation (float): Initial rotation of the navigator
            env (BoxEnv): Box Environment navigator will operate in
        """
        super().__init__(position, rotation, env)

    def take_action(self) -> tuple[Action, Action]:
        """Determine appropriate action to take.

        Returns:
            tuple[Action, Action]: return the action taken and correct action
        """
        # 1. Update target if needed
        surrounding_boxes = self.env.get_boxes(self.position)
        if close_enough(self.position, self.target) and len(surrounding_boxes) > 1:
            self.target = surrounding_boxes[-1].target

        # 2. Find the correct action
        heading_vector = Pt(cos(self.rotation), sin(self.rotation)).normalized()
        target_vector = (self.target - self.position).normalized()
        signed_angle_to_target = heading_vector.angle_between(target_vector)

        # 3. Take the correct action
        if abs(signed_angle_to_target) < self.half_target_wedge:
            self.move_forward()
            action = Action.FORWARD
        elif signed_angle_to_target > 0:
            self.rotate_left()
            action = Action.ROTATE_LEFT
        else:
            self.rotate_right()
            action = Action.ROTATE_RIGHT

        # The boy scout always chooses the "correct" action
        return action, action


class WandererNavigator(BoxNavigatorBase):
    """A navigator that wanders in a directed fashion toward the end goal."""

    def __init__(self, position: Pt, rotation: float, env: BoxEnv) -> None:
        super().__init__(position, rotation, env)

    def take_action(self) -> None:
        raise NotImplemented
