from enum import Enum

"""absolute tolerance value used for equality testing.
Should ideally be relative to magnitude"""
EPS = 1e-12


class Point:
    """
    Represents a point in the plane.
    Contains a dimension field and a list of coordinates for each dimension
    """
    def __init__(self, dimension, coords=None):
        self.dimension = dimension
        if coords is None:
            self.coords = [0. for _ in range(dimension)]
        else:
            assert len(coords) == dimension
            self.coords = coords[:]

    def __str__(self):
        return " ".join("{}".format(c) for c in self.coords)

    def __eq__(self, other):
        return self.sq_distance_to(other) < EPS

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(hash(self.coords[0]) + hash(self.coords[1])) # a bit finniky

    def sq_distance_to(self, other):
        assert self.dim_match(other)

        return sum((self.coords[i] - other.coords[i]) ** 2 for i in range(self.dimension))

    def add(self, other):
        assert self.dim_match(other)

        for i in range(self.dimension):
            self.coords[i] += other.coords[i]

    def sub(self, other):
        assert self.dim_match(other)

        for i in range(self.dimension):
            self.coords[i] -= other.coords[i]

    def mul(self, x):
        self.coords = [coord * x for coord in self.coords]
        return self

    def div(self, x):
        self.coords = [coord / x for coord in self.coords]
        return self

    def dim_match(self, other):
        return self.dimension == other.dimension

    def get(self, i):
        return self.coords[i]


class ClusterPoint(Point):
    """
    Point containing an additional clustering label and cluster function
    """

    DEFAULT_LABEL = -1

    class Func(Enum):
        NOISE = 0
        CORE = 1
        BORDER = 2

    def __init__(self, dimension, coords=None, label=DEFAULT_LABEL, func=Func.NOISE):
        super().__init__(dimension, coords)

        self.cluster_label = label
        self.func = func

    def __str__(self):
        return "{} {} {}".format(super().__str__(), self.cluster_label, self.func.name)

    def is_labeled(self):
        return self.cluster_label != self.DEFAULT_LABEL