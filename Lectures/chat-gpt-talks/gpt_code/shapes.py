from PIL import Image, ImageDraw

def create_embedded_shapes(image_size, square_color, circle_color):
    """
    Create an image with embedded shapes using Pillow.

    Parameters:
        image_size (tuple): The dimensions of the image (width, height).
        square_color (tuple): RGB color for the square shape.
        circle_color (tuple): RGB color for the circle shape.

    Returns:
        Image: A PIL Image object representing the embedded shapes.
    """
    # Create a new image with white background
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)

    # Calculate dimensions
    square_size = min(image_size) // 1.5
    square_x = (image_size[0] - square_size) // 2
    square_y = (image_size[1] - square_size) // 2

    circle_radius = square_size // 2
    circle_x = square_x + circle_radius
    circle_y = square_y + circle_radius

    # Draw square
    draw.rectangle([square_x, square_y, square_x + square_size, square_y + square_size], fill=square_color)

    # Draw circle
    draw.ellipse([circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius], fill=circle_color)

    return img

# Example usage:
image_size = (256, 256)
square_color = (255, 0, 0)
circle_color = (0, 0, 255)

img = create_embedded_shapes(image_size, square_color, circle_color)
img.show()
img.save("shape.bmp")
