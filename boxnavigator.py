from random import random, choice

from ue5env import UE5EnvWrapper
from box import Pt
from boxenv import BoxEnv

import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Wedge

from enum import Enum
from math import sin, cos, degrees, radians


def close_enough(A: Pt, B: Pt, threshold: float = 1) -> bool:
    # BROKEN, likely something to do with how plot is laid out
    """Determine whether Pt A is close enough to Pt B depending on the threshold value.

    Args:
        A (Pt): First Pt to compare
        B (Pt): Second Pt to compare
        threshold (float, optional): Distance to be considered close enough. Defaults to 1.

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
    """Base class for box navigators.

    A navigator can roam from box to box until it gets to the target
    location of the final box.
    """

    def __init__(
        self,
        position: Pt,
        rotation: float,
        env: BoxEnv,
        out_of_bounds: bool,
        ue5_wrapper: UE5EnvWrapper = None,
    ) -> None:
        """Initialize member variables for any navigator.

        Args:
            position (Pt): initial position
            rotation (float): initial rotation
            env (BoxEnv): box environment
        """
        self.env = env
        self.position = position
        self.rotation = rotation
        self.allow_out_of_bounds = out_of_bounds
        self.ue5 = ue5_wrapper

        self.target = self.env.boxes[0].target

        # TODO: change from wedge to field-of-view?
        self.half_target_wedge = radians(5)

        # How much a navigator should translate or rotate in a given step
        # of the simulation. These are fairly arbitrary.
        self.distance_threshold = 200
        self.translation_increment = 100
        self.rotation_increment = radians(10)

    def at_final_target(self) -> bool:
        """Is the navigator at the final target."""
        return close_enough(
            self.position, self.env.boxes[-1].target, self.distance_threshold
        )

    def correct_action(self):
        # TODO: docstring
        # TODO: cache this result?

        # Find the correct action by calculating the angle between the
        # target and the heading of the agent.
        heading_vector = Pt(cos(self.rotation), sin(self.rotation)).normalized()
        target_vector = (self.target - self.position).normalized()
        signed_angle_to_target = heading_vector.angle_between(target_vector)

        # Already facing correct direction
        if abs(signed_angle_to_target) < self.half_target_wedge:
            action = Action.FORWARD

        # Need to rotate left (think of unit circle)
        elif signed_angle_to_target > 0:
            action = Action.ROTATE_LEFT

        # Need to rotate right (think of unit circle)
        else:
            action = Action.ROTATE_RIGHT

        return action

    def take_action(self) -> tuple[Action, Action]:
        """Execute a single action in the environment.

        Returns:
            tuple[Action, Action]: return action taken and correct action.
        """
        self.update_target_if_needed()

        action_taken = self.navigator_specific_action()
        correct_action = self.correct_action()
        # self.sync_position_with_unreal()
        # "vget /camera/0/location"
        # update self.position
        # TODO: only sync when it is possible that we went out of bounds?
        # TODO: should we have a member parameter that turns syncing off?
        #       because we probably won't need to with the perfect navigator
        if action_taken == Action.FORWARD:
            self.move_forward(self.ue5)

        elif action_taken == Action.ROTATE_LEFT:
            self.rotate_left(self.ue5)
        elif action_taken == Action.ROTATE_RIGHT:
            self.rotate_right(self.ue5)
        else:
            self.move_backward(self.ue5)
            # self.sync_position_with_unreal()
            # "vget /camera/0/location"
            # update self.position

        # Sync rotation every so many steps?

        return action_taken, correct_action

    def navigator_specific_action(self) -> Action:
        """
        Raises:
            NotImplemented: implement in child classes
        """
        raise NotImplemented(
            "This method should only be implemented in the inheriting classes."
        )

    def update_target_if_needed(self) -> None:
        """Switch to next target when close enough to current target."""
        surrounding_boxes = self.env.get_boxes(self.position)
        if close_enough(self.position, self.target) and len(surrounding_boxes) > 1:
            self.target = surrounding_boxes[-1].target

    def move_forward(self, ue5: UE5EnvWrapper) -> None:
        """Move forward by a fixed amount."""
        new_x = self.position.x + self.translation_increment * cos(self.rotation)
        new_y = self.position.y + self.translation_increment * sin(self.rotation)

        if ue5 is not None:
            ue5.forward(self.translation_increment)
        self.move(Pt(new_x, new_y))

    def move_backward(self, ue5: UE5EnvWrapper) -> None:
        """Move backward by a fixed amount."""
        new_x = self.position.x - self.translation_increment * cos(self.rotation)
        new_y = self.position.y - self.translation_increment * sin(self.rotation)
        if ue5 is not None:
            ue5.back(self.translation_increment)
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

        elif self.allow_out_of_bounds:
            self.position = self.sync_with_unreal()
        else:
            raise NotImplementedError("Projecting to boundary is not implemented.")

    def sync_with_unreal(self) -> Pt:
        """Sets boxsim point to match coordinate of robot in Unreal"""
        x, y, z = self.ue5.getCameraLocation(0)
        return Pt(x, y)

    def rotate_right(self, ue5: UE5EnvWrapper) -> None:
        """Rotate to the right by a set amount."""
        self.rotation -= self.rotation_increment
        if ue5 is not None:
            # TODO keep as is or add functionality in the UE5 wrapper to covert from radians to degrees
            ue5.right(degrees(self.rotation_increment), 0)

    def rotate_left(self, ue5: UE5EnvWrapper) -> None:
        """Rotate to the left by a set amount."""
        self.rotation += self.rotation_increment
        if ue5 is not None:
            ue5.left(degrees(self.rotation_increment), 0)

    def display(self, ax: plt.Axes, scale: float) -> None:
        """Plot the agent to the given axis.

        Args:
            ax (plt.Axes): axis for plotting
            scale (float): scale of arrows
        """
        ax.invert_xaxis()
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

    # def __init__(
    #     self, position: Pt, rotation: float, env: BoxEnv, out_of_bounds: bool,
    # ) -> None:
    """Initialize navigator position, initial orientation, and associated Box environment.

    Args:
        position (Pt): Initial x,y Coordinate for navigator
        rotation (float): Initial rotation of the navigator
        env (BoxEnv): Box Environment navigator will operate in
        """
    # super().__init__(position, rotation, env, out_of_bounds)

    def navigator_specific_action(self) -> Action:
        """The perfect navigator always chooses the correct action."""
        return self.correct_action()


class WanderingNavigator(BoxNavigatorBase):
    """A navigator that wanders in a directed fashion toward the end goal."""

    # TODO: rename this

    def __init__(
        self, position: Pt, rotation: float, env: BoxEnv, out_of_bounds: bool
    ) -> None:
        super().__init__(position, rotation, env, out_of_bounds)
        self.possible_actions = [
            Action.FORWARD,
            Action.ROTATE_LEFT,
            Action.ROTATE_RIGHT,
        ]

        # TODO: make this a parameter
        self.chance_of_random_action = 0.5

    def navigator_specific_action(self) -> Action:
        # Take a random action some percent of the time
        return (
            choice(self.possible_actions)
            if random() < self.chance_of_random_action
            else self.correct_action()
        )
