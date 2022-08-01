from math import atan2, degrees, sqrt


def approx_equal(a: float, b: float, threshold: float = 0.0001) -> bool:
    return abs(a - b) < threshold


class Pt:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def normalized(self):
        magnitude = self.magnitude()
        return Pt(self.x / magnitude, self.y / magnitude)

    def magnitude(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, scale: float):
        return Pt(self.x * scale, self.y * scale)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __eq__(self, other) -> bool:
        return approx_equal(self.x, other.x) and approx_equal(self.y, other.y)


def dot(A: Pt, B: Pt):
    """Scalar product of two points."""
    return A.x * B.x + A.y * B.y


def dist(A: Pt, B: Pt) -> float:
    """Distance between two points."""
    return sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)


class Box:
    def __init__(self, A: Pt, B: Pt, C: Pt, target: Pt) -> None:
        """Create a arbitrarily rotated box.

        Args:
            A (Pt): origin point
            B (Pt): next point clockwise
            C (Pt): next point clockwise
        """
        self.A = A
        self.B = B
        self.C = C
        self.target = target

        self.AB = self.B - self.A
        self.dotAB = dot(self.AB, self.AB)

        self.BC = self.C - self.B
        self.dotBC = dot(self.BC, self.BC)

    @property
    def origin(self) -> tuple[float, float]:
        return self.A.x, self.A.y

    @property
    def width(self) -> float:
        return dist(self.B, self.C)

    @property
    def height(self) -> float:
        return dist(self.A, self.B)

    @property
    def angle_degrees(self) -> float:
        return 180 - degrees(atan2(self.A.x - self.B.x, self.A.y - self.B.y))

    def point_is_inside(self, M: Pt) -> bool:
        AM = M - self.A
        BM = M - self.B
        AB = self.AB
        BC = self.BC
        return (0 <= dot(AB, AM) <= self.dotAB) and (0 <= dot(BC, BM) <= self.dotBC)


if __name__ == "__main__":
    # Test from here: https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not

    # Describe box with three points
    A = Pt(5, 0)
    B = Pt(0, 2)
    C = Pt(1, 5)
    ignored_target = Pt(0, 0)
    box = Box(A, B, C, ignored_target)

    AB = B - A
    assert AB == Pt(-5, 2)

    BC = C - B
    assert BC == Pt(1, 3)

    dotAB = dot(AB, AB)
    assert dotAB == 29

    dotBC = dot(BC, BC)
    assert dotBC == 10

    # First point to test (this point is inside the box)
    M = Pt(4, 2)

    AM = M - A
    assert AM == Pt(-1, 2)

    BM = M - B
    assert BM == Pt(4, 0)

    dotABAM = dot(AB, AM)
    assert dotABAM == 9

    dotBCBM = dot(BC, BM)
    assert dotBCBM == 4

    assert box.point_is_inside(M)

    # Second point to test (this point is outside the box)
    M = Pt(6, 1)

    AM = M - A
    assert AM == Pt(1, 1)

    BM = M - B
    assert BM == Pt(6, -1)

    dotABAM = dot(AB, AM)
    assert dotABAM == -3

    dotBCBM = dot(BC, BM)
    assert dotBCBM == 3

    assert not box.point_is_inside(M)
