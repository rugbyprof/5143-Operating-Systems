import sys

def edit_pixel(**kwargs):
    file = kwargs.get('file',None)
    imgw = kwargs.get('imgw',None)
    imgh = kwargs.get('imgh',None)
    px = kwargs.get('px',None)
    py = kwargs.get('py',None)

    # Open the BMP image in binary write mode
    with open(file, "rb+") as file:
        # Read the BMP header to get image information
        header = file.read(54)  # BMP headers are typically 54 bytes
        width = header[18] + header[19] * 256
        height = header[22] + header[23] * 256

        # Calculate the position of the pixel you want to modify
        # For example, if you want to change the pixel at (x=10, y=20):
        x = px
        y = py
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

def myKwargs(argv):
    """This process command line arguments and lets you "configure" the current run.
       It takes parameters that look like: key=value or num_people=100 (with NO spaces between)
       and puts them into a python dictionary that looks like:
       {
           "key":"value",
           "num_people":100
       }

       If a parameter doesn't have an "=" sign in it, it puts it into a list
       Both the dictionary (kwargs) and list (args) get returned.
       See usage below under if__name__=='__main__'
    """
    kwargs = {}
    args = []
    for param in argv:
        if '=' in param:
            k, v = param.split('=')
            if v.isnumeric():
                kwargs[k] = int(v)
            else:
                kwargs[k] = v
        else:
            if param.isnumeric():
                param = int(param)
            args.append(param)

    return kwargs, args

def usage():
    print("Usage: python this.py file=something.bmp imgw=800 imgh=800  px=250 py=250 ")

if __name__ == '__main__':
    kwargs, args = myKwargs(sys.argv)

    file = kwargs.get('file',None)
    imgw = kwargs.get('imgw',None)
    imgh = kwargs.get('imgh',None)
    px = kwargs.get('px',None)
    py = kwargs.get('py',None)

    if not file or not px or not py:
        usage()

    edit_pixel(file=file,imgw=imgw,imgh=imgh,px=px,py=py)

        
