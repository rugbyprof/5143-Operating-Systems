"""
The mandelbrot looked amazing! But the fibonacci just looked like dots with no order or spiral.
"""


from PIL import Image, ImageDraw
from math import pi, sin, cos, sqrt

def fibonacci_spiral(image_size, num_points):
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)

    golden_angle = 2 * pi * (1 - (1 + sqrt(5)) / 2)
    center_x, center_y = image_size[0] // 2, image_size[1] // 2

    for i in range(num_points):
        angle = i * golden_angle
        distance = sqrt(i) * 10  # 10 is the distance between each dot; you can adjust as needed
        x = center_x + cos(angle) * distance
        y = center_y + sin(angle) * distance

        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 0, 0))

    return img

# Example usage:
image_size = (512, 512)
num_points = 100

img = fibonacci_spiral(image_size, num_points)
img.show()
