

from PIL import Image, ImageDraw
from math import pi, sin, cos

def fibonacci_spiral(image_size, num_points):
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)

    golden_angle = pi * (3 - 5**0.5)
    radius_increment = image_size[0] / (num_points * 2)

    for i in range(1, num_points + 1):
        angle = i * golden_angle
        radius = i * radius_increment
        x = int(image_size[0] // 2 + cos(angle) * radius)
        y = int(image_size[1] // 2 + sin(angle) * radius)

        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 0, 0))

    return img

# Example usage:
image_size = (512, 512)
num_points = 100

img = fibonacci_spiral(image_size, num_points)
img.show()
img.save("fib.bmp")