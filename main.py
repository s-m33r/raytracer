import numpy as np


class Sphere:
    def __init__(self, idt, position, radius):
        self.idt = idt
        self.position = position
        self.radius = radius

    def hit(self, origin, direction):
        a = np.dot(direction, direction)
        b = np.dot(2 * direction, origin - self.position)
        c = np.dot(origin - self.position, origin - self.position) - self.radius**2

        discriminant = b**2 - 4 * a * c
        return discriminant >= 0


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


class Camera:
    def __init__(
        self,
        position,
        direction,
        image_width,
        viewport_width,
        aspect_ratio,
        focal_length,
    ):
        self.position = position
        self.direction = direction / np.linalg.norm(direction)

        self.image_width = image_width
        self.aspect_ratio = aspect_ratio
        self.image_height = int(self.image_width / self.aspect_ratio)

        self.focal_length = (
            focal_length  # is the distance b/w camera position and view plane
        )

        # view plane
        self.viewplane_width = viewport_width
        self.viewplane_height = (
            self.viewplane_width * self.image_height / self.image_width
        )

        self.pixel_width = self.viewplane_width / self.image_width
        self.pixel_height = self.viewplane_height / self.image_height

        # camera basis vectors
        self.cameraUp = np.array([0, 1, 0])  # Y is up
        self.cameraRight = np.cross(self.direction, self.cameraUp)

    def render(self, scene):
        print(f"P3\n{self.image_width} {self.image_height}\n255\n")

        cameraPositionOnViewPlane = self.position + (
            self.focal_length * self.direction
        )  # offset camera position onto view plane
        cameraPositionOnViewPlane = cameraPositionOnViewPlane.astype("float64")

        for y in range(1, self.image_height + 1):
            for x in range(1, self.image_width + 1):
                pixelU = (x + 0.5) / self.image_width  # normalized pixel coordinates
                pixelV = (y + 0.5) / self.image_height

                pixelPos = cameraPositionOnViewPlane + (
                    (pixelU - 0.5)
                    * self.viewplane_width
                    * -2
                    * self.cameraRight
                    * self.pixel_width
                )  # offset pixel position horizontally on view plane
                pixelPos -= (
                    (pixelV - 0.5)
                    * self.viewplane_height
                    * 2
                    * self.cameraUp
                    * self.pixel_height
                )  # offset pixel position vertically on view plane

                rayDirection = pixelPos - self.position
                rayDirection = rayDirection / np.linalg.norm(
                    rayDirection
                )  # normalized ray vector from camera origin into the scene, through view plane

                # calculate intersection points
                for obj in scene:

                    if obj.hit(self.position, rayDirection):
                        print("255 255 255", end=" ")
                        continue

                    print("0 0 0", end=" ")

                    # pixel brightness
                    # d = np.linalg.norm(intersection - self.position)
                    # grayValue = 255 - d
                    # print(grayValue, grayValue, grayValue, end=" ")

            print("\n")


if __name__ == "__main__":
    scene = [
        # Triangle(
        #    "triangle 1",
        #    np.array([1, 1, 0]),
        #    np.array([-1, 0, 1]),
        #    np.array([1, -1, 0]),
        # ),
        Sphere("sphere 1", np.array([0, 0, 0]), 7),
    ]

    camera = Camera(
        position=np.array([0, 0, -20]),
        direction=np.array([0, 0, 1]),  # looking straight into Z direction
        image_width=200,
        viewport_width=40,
        aspect_ratio=16 / 9,
        focal_length=10,
    )

    camera.render(scene)
