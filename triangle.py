import numpy as np


class Triangle:
    def __init__(self, idt: str, t1, t2, t3):
        """each triangle is a set of 3 coordinates"""
        self.idt = idt
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3

        # calculate triangle plane
        ## normal line
        l1 = t2 - t1
        l2 = t3 - t1
        normal = np.cross(l1, l2)  # angle of normal line

        ## full plane equation
        k = -np.dot(normal, t1)

        self.plane = [*normal, k]

    def hit(self, origin, direction):
        # intersections for object plane
        ld = (self.plane[3] - np.dot(self.plane[:3], origin)) / np.dot(
            self.plane[:3], direction
        )

        if ld < 0:  # intersection point behind camera
            return False

        intersection = ld * direction + origin

        # check if point is inside the triangle
        v1 = self.t2 - self.t3
        a1 = np.cross(v1, intersection - self.t3)
        b1 = np.cross(v1, self.t1 - self.t3)
        c1 = np.dot(a1, b1)

        v2 = self.t2 - self.t1
        a2 = np.cross(v2, intersection - self.t1)
        b2 = np.cross(v2, self.t3 - self.t1)
        c2 = np.dot(a2, b2)

        v3 = self.t1 - self.t2
        a3 = np.cross(v3, intersection - self.t2)
        b3 = np.cross(v3, self.t3 - self.t2)
        c3 = np.dot(a3, b3)

        if c1 < 0 or c2 < 0 or c3 < 0:  # not on the same side
            return False

        return True
