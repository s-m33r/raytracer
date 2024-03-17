import numpy as np

from triangle import Triangle


def grayscale_value(distance, tmin, tmax):
    # Clamp the distance between the minimum and maximum values
    clamped_distance = max(tmin, min(tmax, distance))

    # Linearly interpolate the grayscale value based on the distance
    grayscale_value = 255 - ((clamped_distance - tmin) / (tmax - tmin)) * 255

    # Round and clamp to the valid range
    grayscale_value = int(round(grayscale_value))
    grayscale_value = max(0, min(255, grayscale_value))

    return grayscale_value


class Sphere:
    def __init__(self, idt, position, radius):
        self.idt = idt
        self.position = position
        self.radius = radius

    def hit(self, origin, direction) -> float | None:
        # vector from ray origin to sphere center
        oc = self.position - origin

        # projection of this vector onto ray direction
        proj = np.dot(oc, direction)

        # squared distance from ray to sphere center
        dist_squared = np.dot(oc, oc) - proj**2

        # If the ray misses the sphere, return None
        if dist_squared > self.radius**2:
            return None

        # Calculate the distance to the intersection point(s)
        dist_to_intersection = (self.radius**2 - dist_squared) ** 0.5

        # Calculate the intersection point(s)
        intersection_1 = origin + direction * (proj - dist_to_intersection)
        intersection_2 = origin + direction * (proj + dist_to_intersection)

        # Calculate the distances to the intersection points
        distance_1 = np.linalg.norm(intersection_1 - origin).astype(float)
        distance_2 = np.linalg.norm(intersection_2 - origin).astype(float)

        return min(distance_1, distance_2)

        # a = np.dot(direction, direction)
        # b = np.dot(2 * direction, origin - self.position)
        # c = np.dot(origin - self.position, origin - self.position) - self.radius**2

        # discriminant = b**2 - 4 * a * c
        # return discriminant >= 0


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

                    d = obj.hit(self.position, rayDirection)
                    if d:
                        grayValue = grayscale_value(d, abs(pixelPos[2]), 20)
                        print(grayValue, grayValue, grayValue, end=" ")
                    else:
                        print("0 0 0", end=" ")

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
        position=np.array([0, -5, -20]),
        direction=np.array([0, 0, 1]),  # looking straight into Z direction
        image_width=200,
        viewport_width=40,
        aspect_ratio=16 / 9,
        focal_length=10,
    )

    camera.render(scene)
