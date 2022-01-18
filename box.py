from point import ClusterPoint
from enum import Enum


class Box():

    DEFAULT_LABEL = -1

    class Func(Enum):
        """
        Function of a box. Can be one of the following:\\
        NONE: No core points in box \\
        CORE: Only core points in box \\
        PARTIAL: Contains at least one core point
        """
        NONE = 1
        CORE = 2
        PARTIAL = 3

    def __init__(self, points, func=Func.NONE):
        self.points = points
        self.func = func
        self.neighbours = []
        self.label = self.DEFAULT_LABEL

        self.bounds = {
            "bottom": min(self.points, key=lambda x: x.coords[1]).coords[1],
            "top": max(self.points, key=lambda x: x.coords[1]).coords[1],
            "left": min(self.points, key=lambda x: x.coords[0]).coords[0],
            "right": max(self.points, key=lambda x: x.coords[0]).coords[0],
        }

    def is_labeled(self):
        """
        Returns whether a box is labeled
        """
        return not self.label == self.DEFAULT_LABEL

    def sqr_distance_to(self, other):
        """
        Returns the square of the minimal distance from self to other.\\
        Assumes that other and self do not overlap
        """

        # Determine difference in width
        if other.bounds["right"] < self.bounds["left"]:
            w = (self.bounds["left"] - other.bounds["right"])**2
        elif other.bounds["left"] > self.bounds["right"]:
            w = (other.bounds["left"] - self.bounds["right"])**2
        else:
            w = 0

        # Determine difference in height:
        if other.bounds["top"] < self.bounds["bottom"]:
            h = (self.bounds["bottom"] - other.bounds["top"])**2
        elif other.bounds["bottom"] > self.bounds["top"]:
            h = (other.bounds["bottom"] - self.bounds["top"])**2
        else:
            h = 0

        return w + h

    def is_core_neighbour(self, other, dist):
        """
        Returns whether there exists a core point A in this box and a core point B in the `other` box for which dist(A,B) <= `dist`
        """
        sqr_dist = dist**2
        my_core_points = [
            p for p in self.points if p.func == ClusterPoint.Func.CORE]
        other_core_points = [
            p for p in other.points if p.func == ClusterPoint.Func.CORE]
        for cp in my_core_points:
            for ocp in other_core_points:
                print('coords:', cp.coords, ocp.coords, cp.sq_distance_to(ocp) <= sqr_dist)
                if cp.sq_distance_to(ocp) <= sqr_dist:
                    return True
        return False

    def add_neighbour(self, neighbour):
        """
        Adds neighbour to list of neighbours
        """
        self.neighbours.append(neighbour)
