from PIL import Image, ImageDraw
import math

def create_angle_gradient(image_size, color1, color2, angle):
    """
    Create a gradient image at a specified angle using Pillow.

    Parameters:
        image_size (tuple): The dimensions of the image (width, height).
        color1 (tuple): RGB color for the starting color.
        color2 (tuple): RGB color for the ending color.
        angle (float): The angle at which the gradient is applied, in degrees.

    Returns:
        Image: A PIL Image object representing the gradient.
    """
    img = Image.new("RGB", image_size)
    draw = ImageDraw.Draw(img)
    
    angle_rad = math.radians(angle)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)

    for y in range(image_size[1]):
        for x in range(image_size[0]):
            t = (x * cos_angle + y * sin_angle) / max(image_size)
            t = min(max(t, 0), 1)

            r = int(color1[0] + t * (color2[0] - color1[0]))
            g = int(color1[1] + t * (color2[1] - color1[1]))
            b = int(color1[2] + t * (color2[2] - color1[2]))

            draw.point((x, y), (r, g, b))

    return img

# Example usage:
image_size = (256, 256)
color1 = (255, 0, 0)
color2 = (0, 255, 255)
angle = 45  # 45-degree angle for the gradient

img = create_angle_gradient(image_size, color1, color2, angle)
img.show()
img.save("gradient.bmp")
