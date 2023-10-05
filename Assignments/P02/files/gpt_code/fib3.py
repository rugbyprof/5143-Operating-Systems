"""

I think the math behind the gold ratio is correct, however, simply drawing dots does not portray the overall pattern. 
It simply looks like a collection of dots (that in a tiny way may have a spiral effect). Is there any you can connect 
each dot in sequence? Or maybe size each dot to emphasize the spiral effect?
"""

from PIL import Image, ImageDraw
from math import pi, sin, cos, sqrt

def fibonacci_spiral(image_size, num_points):
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)

    golden_angle = 2 * pi * (1 - (1 + sqrt(5)) / 2)
    center_x, center_y = image_size[0] // 2, image_size[1] // 2
    prev_x, prev_y = None, None

    for i in range(1, num_points + 1):
        angle = i * golden_angle
        distance = sqrt(i) * 10
        x = center_x + cos(angle) * distance
        y = center_y + sin(angle) * distance

        dot_size = i // 10  # increasing dot size based on its sequence; you can adjust this formula
        draw.ellipse((x - dot_size, y - dot_size, x + dot_size, y + dot_size), fill=(255, 0, 0))

        if prev_x is not None:
            draw.line((prev_x, prev_y, x, y), fill=(0, 0, 0))

        prev_x, prev_y = x, y

    return img

# Example usage:
image_size = (512, 512)
num_points = 300  # increased for a more dense spiral

img = fibonacci_spiral(image_size, num_points)
img.show()
