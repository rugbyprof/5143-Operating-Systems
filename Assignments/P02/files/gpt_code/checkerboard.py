from PIL import Image, ImageDraw

def create_checkerboard(image_size, square_size, color1=(0, 0, 0), color2=(255, 255, 255)):
    """
    Create a checkerboard image using Pillow.

    Parameters:
        image_size (tuple): The dimensions of the image (width, height).
        square_size (int): The size of each square in the checkerboard.
        color1 (tuple): RGB color for the first type of square (default is black).
        color2 (tuple): RGB color for the second type of square (default is white).
    
    Returns:
        Image: A PIL Image object representing the checkerboard.
    """
    
    # Create a new image with white background
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)
    
    # Loop to draw the checkerboard
    for i in range(0, image_size[0], square_size):
        for j in range(0, image_size[1], square_size):
            color = color1 if (i // square_size) % 2 == (j // square_size) % 2 else color2
            draw.rectangle([i, j, i + square_size, j + square_size], fill=color)
    
    return img

# Example usage:
image_size = (1024, 1024)  # 256x256 pixels
square_size = 64  # Each square is 32x32 pixels

img = create_checkerboard(image_size, square_size,color1=(255,0,0),color2=(255,255,0))
img.show()  # This will display the image using the default image viewer
