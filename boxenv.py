from box import Box, Pt

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def close_enough(A: Pt, B: Pt, threshold: float = 1) -> bool:
    # TODO: find good threshold value
    distance = (A - B).magnitude()
    return distance < threshold


class BoxEnv:
    """A simple 2D environment of interconnected boxes."""

    def __init__(self, boxes: list[Box]) -> None:
        self.boxes = boxes

        # Get scale for plotting
        padding = 5
        min_x = min(min(b.A.x, b.B.x, b.C.x) for b in boxes)
        max_x = max(max(b.A.x, b.B.x, b.C.x) for b in boxes)
        min_y = min(min(b.A.y, b.B.y, b.C.y) for b in boxes)
        max_y = max(max(b.A.y, b.B.y, b.C.y) for b in boxes)

        self.xlim = [min_x - padding, max_x + padding]
        self.ylim = [min_y - padding, max_y + padding]
        self.scale = 0.4 * min(abs(max_x - min_x), abs(max_y - min_y))

    def get_boxes(self, pt: Pt) -> list[Box]:
        return [box for box in self.boxes if box.point_is_inside(pt)]

    def at_final_target(self, pt: Pt) -> bool:
        return close_enough(pt, self.boxes[-1].target)

    def display(self, ax: plt.Axes) -> None:
        for box in self.boxes:
            rect = Rectangle(
                box.origin, box.width, box.height, box.angle_degrees, fill=None
            )
            ax.add_patch(rect)

        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)
        ax.set_aspect("equal")

    def test_display(self) -> None:
        _, ax = plt.subplots(1, 1)
        self.display(ax)
        plt.show()


if __name__ == "__main__":
    boxes = [Box(Pt(50, 0), Pt(0, 20), Pt(10, 50), Pt(25, 25))]
    env = BoxEnv(boxes)
    env.test_display()
