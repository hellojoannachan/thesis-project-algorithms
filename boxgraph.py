import sys
import os
from point import ClusterPoint
from box import Box


class BoxGraph():

    def __init__(self, n, d, epsilon, min_pts, points):
        # Save constants
        self.n = n
        self.d = d
        self.eps = epsilon
        self.min_pts = min_pts
        self.points = points

        # Useful objects
        self.eps_sqr = epsilon**2
        self.boxes = []

        # Setup graph
        grid = self.create_grid()
        self.compute_box_neighbors(grid)

    def create_grid(self):
        """
        Puts points in boxes of at most `self.eps`/sqrt(2) by `self.eps`/sqrt(2).\\
        First sweeping from left to right and creating strips.\\
        Then sweeping from from bottom to top through each strip creating boxes.
        """

        # Define constants
        stripsize = self.eps / (2**(1/2))

        # Get points sorted on first coordinate
        sorted_points = sorted(self.points, key=lambda p: p.coords[0])

        # Sweep from left to right
        ptr, strips = 0, []
        left = sorted_points[ptr].coords[0]
        for i, p in enumerate(sorted_points):
            if p.coords[0] > left + stripsize:
                strips.append(sorted_points[ptr:i])
                ptr = i
                left = sorted_points[ptr].coords[0]
        # Add remaining points to last strip
        if ptr < len(sorted_points):
            strips.append(sorted_points[ptr:])

        # Sort all points in all strips on second coordinate
        for i, _ in enumerate(strips):
            strips[i] = sorted(strips[i], key=lambda p: p.coords[1])
        
        # Create boxes from strips
        grid = [[] for _ in strips]
        for i, strip in enumerate(strips):

            # Sweep from bottom to top
            ptr = 0
            bottom = strip[ptr].coords[1]
            for j, p in enumerate(strip):
                if p.coords[1] > bottom + stripsize:
                    grid[i].append(Box(strip[ptr:j]))
                    ptr = j
                    bottom = strip[ptr].coords[1]
            # Add remaining points to last box
            if ptr < len(strip):
                grid[i].append(Box(strip[ptr:]))

        return grid

    def compute_box_neighbors(self, grid):
        """
        Link neighbouring boxes in grid
        """
        # Create priority queue (i.e. sorted list with lowest entry at the end)
        Q = []
        for i, strip in enumerate(grid):
            for box in strip:
                Q.append((box.bounds["bottom"], box, i))
                Q.append((box.bounds["top"] + self.eps, box, i))
        Q = sorted(Q, key=lambda x:x[0], reverse=True) # Sort on first entry of the tuple

        sweepline = [[] for _ in grid]
        while Q:
            (y, B, i) = Q.pop() # take last element (which has lowest priority)

            if y == B.bounds["bottom"]:
                for j in range(max(0, i-2), min(i+3, len(sweepline))): # recall, range is [i-2, i+3), so i+3 is not included
                    for box in sweepline[j]:
                        if B.sqr_distance_to(box) <= self.eps_sqr:
                            B.add_neighbour(box)
                            box.add_neighbour(B)
                sweepline[i].append(B)
            else:
                sweepline[i].remove(B)
        
        # Add all boxes to boxes list
        self.boxes += [a for b in grid for a in b]

        
    @staticmethod
    def read_input(file):
        """
        Parses the input file into a BoxGraph object

        `file`          opened file object (or stdio)\\
        `return`        a BoxGraph object for the input set
        """
        # read first line and split into list
        words = file.readline().split()

        # check whether first line contains correct nr. of parameters
        assert len(words) == 4

        n, d, epsilon, min_pts = int(words[0]), int(
            words[1]), float(words[2]), int(words[3])
        points = []

        # Read n points
        for _ in range(n):
            words = file.readline().split()

            # check whether input line contains exactly d coordinates
            assert len(words) == d

            # Read d coords
            coords = [float(word) for word in words]

            # Add point to array
            points.append(ClusterPoint(d, coords))

        return BoxGraph(n, d, epsilon, min_pts, points)

    def write_output(self, c, path_out, assignment_nr):
        """
        Writes current state of self to specified file

        `c`             number of created clusters\\
        `path_out`      location to write current state to\\
        `assignment_nr` number of this assignment 
        """

        # create directory if not exists
        os.makedirs(os.path.dirname(path_out), exist_ok=True)

        with open(path_out, "w+") as f:
            f.write("{}\n".format(assignment_nr))
            f.write("{} {} {} \n".format(self.n, self.d, c))

            for point in self.points:
                f.write("{}\n".format(point))
