from PIL import Image, ImageDraw

def mandelbrot(c,max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_image(size, max_iter):
    img = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(img)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            c = complex(x/size[0]*3.5 - 2.5, y/size[1]*2 - 1)
            color = mandelbrot(c,max_iter)
            draw.point((x,y), (color, color, color))

    return img

# Example usage:
size = (800, 800)
max_iter = 256

img = mandelbrot_image(size, max_iter)
img.show()
img.save('brot.bmp')
