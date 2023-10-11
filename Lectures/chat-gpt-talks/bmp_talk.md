## Flatten

1. **Converting a BMP to a single contiguous list of memory locations:**

```python
from PIL import Image

def bmp_to_list(image_path):
    # Open the BMP image using Pillow
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    # Flatten the 2D data into a 1D list
    flattened_data = [pixel for sublist in pixels for pixel in sublist]
    return flattened_data

# Test
flattened_data = bmp_to_list("path_to_your_bmp.bmp")
print(flattened_data[:100])  # Just print the first 100 values for a quick look
```

2. **Converting the single dimensional list of pixel information back to 2D data and saving it as an image:**

```python
def list_to_bmp(data, image_path, width, height):
    # Convert the 1D data to 2D tuples for Pillow
    pixels_2d = [(data[i], data[i+1], data[i+2]) for i in range(0, len(data), 3)]
    
    # Create a new image using the 2D pixel data
    img = Image.new('RGB', (width, height))
    img.putdata(pixels_2d)
    img.save(image_path)

# Test (assuming the original image was 200x200 for example)
list_to_bmp(flattened_data, "restored_image.bmp", 200, 200)
```

To use this, replace `"path_to_your_bmp.bmp"` with the path to your BMP file. The `bmp_to_list` function will open the BMP, extract its pixel data, and flatten it into a single list. The `list_to_bmp` function will then take that flattened data, reconstruct the 2D pixel data, and save it as a new BMP image.

Ensure that you know the dimensions (width and height) of the image you're trying to reconstruct when using `list_to_bmp`. If you don't, you could include the width and height as metadata at the start of your flattened data list. For this example, I've assumed a 200x200 image, but you'll want to adjust that as necessary.

## BMP Edit

```python
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

        
```

## Gray Scale

Certainly, Terry! Incorporating registers brings us closer to the way actual assembly languages work. Here's a pseudo-assembly approach to grayscaling an image using registers:

1. We'll use `R1` to `R3` for storing the RGB values.
2. `R4` will be used to store the grayscale value.
3. `R5` will temporarily store intermediate results.
4. `R6` will be our memory address pointer, iterating over the flattened image data.
5. `R7`, `R8`, and `R9` will be used to store the constant weights for red, green, and blue.
6. `R10` is used for loop control.

```assembly
# Constants
LOADI R7, 0.299      # RED_WEIGHT
LOADI R8, 0.587      # GREEN_WEIGHT
LOADI R9, 0.114      # BLUE_WEIGHT
LOADI R6, 0          # ADDR pointer initialization
LOADI R10, [WIDTH * HEIGHT * BYTES_PER_PIXEL]

# Start of main loop
LOOP_START:

    # Check if we've processed all pixels
    CMP R6, R10
    JGE END_LOOP

    # Load RGB values into R1, R2, and R3
    LOAD R1, [R6]      # Load Red value
    LOAD R2, [R6 + 1]  # Load Green value
    LOAD R3, [R6 + 2]  # Load Blue value

    # Grayscale computation
    # R4 = 0.299*R1 + 0.587*R2 + 0.114*R3
    MUL R1, R7         # R1 = R1 * RED_WEIGHT
    MUL R2, R8         # R2 = R2 * GREEN_WEIGHT
    MUL R3, R9         # R3 = R3 * BLUE_WEIGHT

    ADD R5, R1, R2
    ADD R4, R5, R3

    # Store the grayscale value back to the image data
    STORE [R6], R4
    STORE [R6 + 1], R4
    STORE [R6 + 2], R4

    # Move to the next pixel
    ADDI R6, 3

    JUMP LOOP_START

END_LOOP:

# End of program
HALT
```

Explanation:

- `LOADI` is an instruction to load an immediate value into a register.
- `CMP` compares two values and sets some flags (not explicitly represented here).
- `JGE` is a conditional jump if greater than or equal.
- `MUL` multiplies a register by another value (could be another register or an immediate).
- `ADD` and `ADDI` add two registers or a register and an immediate value, respectively.
- `JUMP` is an unconditional jump.
- Addressing for `LOAD` and `STORE` is offset-based using the value in `R6`.

Again, this is illustrative pseudo-assembly and can be adjusted according to the specifics of the assembly language you define. But the idea is to give students a sense of working with registers, memory addressing, and basic arithmetic operations at the assembly level.

## Flip Horizontal

Absolutely, Terry. Let's rewrite the `flip image` pseudo assembly using the same register-based approach we just established for the grayscale example:

```assembly
# Assembly code to flip an image horizontally using R1-R10 registers.

# Load image width to R1 and height to R2
LOAD R1, IMAGE_WIDTH
LOAD R2, IMAGE_HEIGHT

# Set up a loop counter in R3 to traverse the rows
MOVE R3, 0

START_ROW_LOOP:

  # Calculate left and right pointers for each row
  # Left pointer (R4) = R3 * IMAGE_WIDTH
  # Right pointer (R5) = (R3 + 1) * IMAGE_WIDTH - 1
  MULT R4, R3, R1
  ADD R5, R4, R1
  SUB R5, R5, 1
  
  # Set up a loop counter in R6 to traverse half the width
  MOVE R6, 0

  START_COLUMN_LOOP:

    # Load pixel RGB values from the left and right pointers
    LOAD R7, [R4]     # R7 stores the RGB value from the left
    LOAD R8, [R5]     # R8 stores the RGB value from the right

    # Swap pixel values
    MOVE R9, R7       # Use R9 as a temporary storage
    MOVE R7, R8
    MOVE R8, R9

    # Store the swapped RGB values back to the memory
    STORE [R4], R7
    STORE [R5], R8

    # Move to the next column (increment left pointer and decrement right pointer)
    ADD R4, R4, 1
    SUB R5, R5, 1

    # Increment column loop counter and check if we've processed half the columns
    ADD R6, R6, 1
    IF R6 < (R1 / 2) GOTO START_COLUMN_LOOP

  # Move to the next row
  ADD R3, R3, 1
  IF R3 < R2 GOTO START_ROW_LOOP

# End of program
END
```

In this approach:
- We've got registers `R1` to `R10` at our disposal.
- Registers `R4` and `R5` are pointers that start at the leftmost and rightmost pixels of a row and work their way towards the center of the image.
- Registers `R7`, `R8`, and `R9` are used to facilitate the pixel value swapping.

This logic will achieve the effect of flipping the image horizontally. Remember that this pseudo assembly is a representation of the algorithm, and the actual commands might vary depending on the specific assembly language you're using or if this were to be implemented in a real-world scenario.

## Flip Vertical

Certainly, Terry! Let's adapt our previous pseudo assembly to flip an image vertically.

Here's the game plan:
1. We'll have two pointers. The first one will point to the top row of the image and the other to the bottom row.
2. We'll swap entire rows until we reach the center of the image.

Here's how the assembly might look:

```assembly
# Assembly code to flip an image vertically using R1-R10 registers.

# Load image width to R1 and height to R2
LOAD R1, IMAGE_WIDTH
LOAD R2, IMAGE_HEIGHT

# Calculate total number of pixels in the image into R10
MULT R10, R1, R2

# Set up top (R3) and bottom (R4) row pointers
MOVE R3, 0
MULT R4, R2, R1   # R4 points to the last row's first pixel
SUB R4, R4, R1

# Set up a loop counter in R5 for rows (we only need to process half the rows)
MOVE R5, 0

START_ROW_LOOP:

  # Set up a loop counter in R6 to traverse the width
  MOVE R6, 0

  START_COLUMN_LOOP:
    # Load pixel RGB values from top and bottom rows
    LOAD R7, [R3]     # R7 stores the RGB value from the top
    LOAD R8, [R4]     # R8 stores the RGB value from the bottom

    # Swap pixel values
    MOVE R9, R7       # Use R9 as a temporary storage
    MOVE R7, R8
    MOVE R8, R9

    # Store the swapped RGB values back to the memory
    STORE [R3], R7
    STORE [R4], R8

    # Move to the next column (increment both pointers)
    ADD R3, R3, 1
    ADD R4, R4, 1
    ADD R6, R6, 1
    IF R6 < R1 GOTO START_COLUMN_LOOP

  # Reset column pointer for top (R3) and decrement for bottom (R4)
  SUB R3, R3, R1
  SUB R4, R4, 2*R1

  # Increment row loop counter and check if we've processed half the rows
  ADD R5, R5, 1
  IF R5 < (R2 / 2) GOTO START_ROW_LOOP

# End of program
END
```

In this approach:
- We've still got registers `R1` to `R10` at our disposal.
- Registers `R3` and `R4` point to the top and bottom rows of the image, respectively.
- Registers `R7`, `R8`, and `R9` are used to facilitate the pixel value swapping.

Again, this is a high-level representation of the algorithm, and the actual commands might vary based on the specific assembly language or if this were to be applied in a real-world scenario.

## Blur

Blurring an image is a bit more intricate than the previous operations. One common method for blurring is to use the **mean** of surrounding pixels (including the pixel itself) to generate the new value for that pixel. For simplicity, let's assume a 3x3 kernel for our blur operation.

Given a pixel at `(x, y)`, we will take the mean of all pixels in the 3x3 grid centered at `(x, y)`.

Here's how we can outline the algorithm in our pseudo assembly:

1. For each pixel `(x, y)`:
    1. Sum the RGB values of all pixels in the 3x3 grid centered at `(x, y)`.
    2. Divide the sum by 9 (the number of pixels in the grid) to compute the mean.
    3. Store the mean RGB values as the new value for the pixel `(x, y)`.

Let's see the assembly:

```assembly
# Assembly code to blur an image using R1-R10 registers.

# Load image width to R1 and height to R2
LOAD R1, IMAGE_WIDTH
LOAD R2, IMAGE_HEIGHT

# Iterate over each row
MOVE R3, 1  # We start from 1 to avoid edges for simplicity
START_ROW_LOOP:

  # Iterate over each column
  MOVE R4, 1  # We start from 1 to avoid edges for simplicity
  START_COLUMN_LOOP:

    # Initialize R6, R7, and R8 to accumulate RGB values for the 3x3 grid
    MOVE R6, 0
    MOVE R7, 0
    MOVE R8, 0

    # Calculate address offset for the current pixel: R3 * IMAGE_WIDTH + R4
    MULT R5, R3, R1
    ADD R5, R5, R4
    MOVE R9, R5  # R9 holds the base address for our 3x3 grid

    # Iterate over the 3x3 grid to accumulate RGB values
    MOVE R10, -1  # Start from the previous row
    START_3x3_ROW_LOOP:
      ADD R9, R5, R10
      SUB R9, R9, 1  # Start from the previous column
      START_3x3_COLUMN_LOOP:

        # Add RGB values from the pixel at (R3+R10, R4+R9-R5) to R6, R7, and R8
        LOAD R6, [R9]  # For the sake of simplicity, assume loading RGB into separate registers is abstracted
        LOAD R7, [R9]  # Similarly load G
        LOAD R8, [R9]  # Similarly load B

        # Increment R9 to move to the next column
        ADD R9, R9, 1

      # Check if we've processed 3 columns in the 3x3 grid
      IF (R9 - R5) < 3 GOTO START_3x3_COLUMN_LOOP

    # Move to the next row in the 3x3 grid
    ADD R10, R10, 1
    IF R10 < 2 GOTO START_3x3_ROW_LOOP

    # Now, we divide the accumulated RGB values in R6, R7, and R8 by 9 to compute the mean
    DIV R6, R6, 9
    DIV R7, R7, 9
    DIV R8, R8, 9

    # Store the mean RGB values as the new value for the pixel (R3, R4)
    STORE [R5], R6
    STORE [R5], R7
    STORE [R5], R8

    # Move to the next column
    ADD R4, R4, 1
    IF R4 < (R1 - 1) GOTO START_COLUMN_LOOP

  # Move to the next row
  ADD R3, R3, 1
  IF R3 < (R2 - 1) GOTO START_ROW_LOOP

# End of program
END
```

Note:
- We're using a simple mean blur and skipping the edges of the image for the sake of simplicity.
- This algorithm is inefficient, especially in an assembly context. Advanced algorithms like the Gaussian blur and the use of separable filters can achieve similar effects much more efficiently.
- Real-world assembly would require multiple instructions to accomplish tasks like multi-register arithmetic. The pseudo-code above abstracts many of these details for clarity.