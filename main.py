import numpy as np

class Sphere:
    def __init__(self, idt, position, radius):
        self.idt = idt
        self.position = position
        self.radius = radius

    def hit(self, origin, direction):
        a = np.dot(direction, direction)
        b = np.dot(2 * direction, origin - self.position)
        c = np.dot(origin - self.position, origin - self.position) - self.radius ** 2

        discriminant = b**2 - 4*a*c
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
        normal = np.cross(l1, l2) # angle of normal line

        ## full plane equation
        k = -np.dot(normal, t1)

        self.plane = [*normal, k]


class Camera:
    def __init__(self, position, direction, image_width, aspect_ratio, focal_length):
        self.position = position
        self.direction = direction / np.linalg.norm(direction)

        self.image_width = image_width
        self.aspect_ratio = aspect_ratio
        self.image_height = int( self.image_width / self.aspect_ratio )

        self.focal_length = focal_length # is the distance b/w camera position and view plane

        # view plane
        self.viewplane_width = self.image_width
        self.viewplane_height = self.image_height

        self.pixel_width = self.viewplane_width / self.image_width
        self.pixel_height = self.viewplane_height / self.image_height

        # camera basis vectors
        self.cameraUp = np.array([0, 1, 0]) # Y is up
        self.cameraRight = np.cross(self.direction, self.cameraUp)

    def render(self, scene):
        print(f"P3\n{self.image_width} {self.image_height}\n255\n")

        cameraPositionOnViewPlane = self.position + (self.focal_length * self.direction) # offset camera position onto view plane
        cameraPositionOnViewPlane = cameraPositionOnViewPlane.astype('float64')

        for y in range(self.image_height):
            for x in range(self.image_width):
                pixelU = x / self.image_width # normalized pixel coordinates
                pixelV = y / self.image_height
                
                pixelPos = cameraPositionOnViewPlane + pixelU * self.viewplane_width * -1 * self.cameraRight # offset pixel position horizontally on view plane
                pixelPos += pixelV * self.viewplane_height * self.cameraUp # offset pixel position vertically on view plane

                rayDirection = pixelPos - self.position
                rayDirection = rayDirection / np.linalg.norm(rayDirection) # normalized ray vector from camera origin into the scene, through view plane

                # calculate intersection points
                for obj in scene:
                    # intersections for object plane
                    ld = ( obj.plane[3] - np.dot(obj.plane[:3], self.position) ) / np.dot(obj.plane[:3], rayDirection)

                    if ld < 0: # intersection point behind camera
                        print("0 0 0", end=" ")
                        continue

                    intersection = ld * rayDirection + self.position

                    # check if point is inside the triangle
                    v1 = obj.t2 - obj.t3
                    a1 = np.cross(v1, intersection - obj.t3)
                    b1 = np.cross(v1, obj.t1 - obj.t3)
                    c1 = np.dot(a1, b1)

                    v2 = obj.t2 - obj.t1
                    a2 = np.cross(v2, intersection - obj.t1)
                    b2 = np.cross(v2, obj.t3 - obj.t1)
                    c2 = np.dot(a2, b2)

                    v3 = obj.t1 - obj.t2
                    a3 = np.cross(v3, intersection - obj.t2)
                    b3 = np.cross(v3, obj.t3 - obj.t2)
                    c3 = np.dot(a3, b3)

                    if c1 < 0 or c2 < 0 or c3 < 0: # not on the same side
                        print("0 0 0", end=" ")
                        continue
                    
                    # pixel brightness
                    d = np.linalg.norm(intersection - self.position)
                    grayValue = 255 - d
                    print(grayValue, grayValue, grayValue, end=" ")

            print("\n")



if __name__ == "__main__":
    scene = []

    scene.append(
        Triangle(
            "triangle 1",
            np.array([1, 1, 0]),
            np.array([-1, 0, 0]),
            np.array([1, -1, 0])
        )
    )

    camera = Camera(
        position=np.array([0, 0, -10]),
        direction=np.array([0, 0, 1]), # looking straight into Z direction
        image_width=100,
        aspect_ratio=16/9,
        focal_length=3
    )

    camera.render(scene)

