# Open the BMP image in binary write mode
with open("brot.bmp", "rb+") as file:
    # Read the BMP header to get image information
    header = file.read(54)  # BMP headers are typically 54 bytes
    width = header[18] + header[19] * 256
    height = header[22] + header[23] * 256

    # Calculate the position of the pixel you want to modify
    # For example, if you want to change the pixel at (x=10, y=20):
    x = 400
    y = 400
    pixel_position = 54 + (y * width + x) * 3  # Each pixel is 3 bytes (RGB)

    # Move the file cursor to the pixel position
    file.seek(pixel_position)

    # Modify the pixel color (for example, set it to red)
    # BMP stores pixel data in reverse order (BGR)
    blue = 0
    green = 0
    red = 255
    new_pixel_data = bytes([blue, green, red])

    # Write the new pixel data
    file.write(new_pixel_data)

print("Pixel at (10, 20) modified to red.")
