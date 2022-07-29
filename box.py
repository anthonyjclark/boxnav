def approx_equal(a: float, b: float, threshold: float = 0.0001) -> bool:
    return abs(a - b) < threshold


class Pt:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def __eq__(self, other) -> bool:
        return approx_equal(self.x, other.x) and approx_equal(self.y, other.y)


def dot(A: Pt, B: Pt):
    """Scalar product of two points."""
    return A.x * B.x + A.y * B.y


class Box:
    def __init__(self, A: Pt, B: Pt, C: Pt) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.target = ...

        self.AB = self.A - self.B
        self.dotAB = dot(self.AB, self.AB)

        self.BC = self.B - self.C
        self.dotBC = dot(self.BC, self.BC)

    def point_is_inside(self, M: Pt) -> bool:
        AM = self.A - M
        BM = self.B - M
        AB = self.AB
        BC = self.BC
        return (0 <= dot(AB, AM) <= self.dotAB) and (0 <= dot(BC, BM) <= self.dotBC)


if __name__ == "__main__":
    # Test from here: https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not

    A = Pt(5, 0)
    B = Pt(0, 2)
    C = Pt(1, 5)
    D = Pt(6, 3)  # Redundant point

    box = Box(A, B, C)

    M = Pt(4, 2)

    AB = B - A
    assert AB == Pt(-5, 2)

    BC = C - B
    assert BC == Pt(1, 3)

    dotAB = dot(AB, AB)
    assert dotAB == 29

    dotBC = dot(BC, BC)
    assert dotBC == 10

    AM = M - A
    assert AM == Pt(-1, 2)

    BM = M - B
    assert BM == Pt(4, 0)

    dotABAM = dot(AB, AM)
    assert dotABAM == 9

    dotBCBM = dot(BC, BM)
    assert dotBCBM == 4

    assert box.point_is_inside(M)

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
