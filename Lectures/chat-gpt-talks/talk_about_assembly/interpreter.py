"""
Each of these "interpreter.py" files is a version provided by chat gpt. This is the latest version
where the interpreterN.py are ordered where smallest number is the oldest.
"""

class Memory:
    def __init__(self, size):
        self.size = size
        self.memory = [0] * size  # Initialize memory with zeros

    def read(self, mem_addr):
        # Read data from memory at the specified memory address
        if 0 <= mem_addr < self.size:
            return self.memory[mem_addr]
        else:
            raise ValueError("Memory address out of bounds")

    def write(self, mem_addr, data):
        # Write data to memory at the specified memory address
        if 0 <= mem_addr < self.size:
            self.memory[mem_addr] = data
        else:
            raise ValueError("Memory address out of bounds")

    def dump(self):
        # Dump the contents of memory (for debugging purposes)
        return self.memory



class PseudoAssemblyInterpreter:
    def __init__(self, memory):
        self.registers = {}
        self.memory = memory
        self.pc = 0  # Program counter
        self.loop_stack = []  # Stack to keep track of loop positions

    def execute_pseudo_assembly(self, code):
        instructions = code.split('\n')
        while self.pc < len(instructions):
            instruction = instructions[self.pc].strip()
            if instruction:
                self.execute_instruction(instruction)


    def execute_instruction(self, instruction):
        parts = instruction.split()
        opcode = parts[0].upper()

        if opcode == 'LOAD':
            # Handle LOAD instruction
            register = int(parts[1][1:])  # Parse register number from R1, R2, ...
            mem_addr = int(parts[2])
            self.load(register, mem_addr)
        elif opcode == 'STORE':
            # Handle STORE instruction
            register = int(parts[1][1:])  # Parse register number from R1, R2, ...
            mem_addr = int(parts[2])
            self.store(register, mem_addr)
        elif opcode == 'ADD':
            # Handle ADD instruction
            register_dest = int(parts[1][1:])
            register_src1 = int(parts[2][1:])
            value = int(parts[3])
            self.add(register_dest, register_src1, value)
        elif opcode == 'DIV':
            # Handle DIV instruction
            register_dest = int(parts[1][1:])
            register_src1 = int(parts[2][1:])
            value = int(parts[3])
            self.divide(register_dest, register_src1, value)
        elif opcode == 'CMP':
            # Handle CMP instruction
            register_src1 = int(parts[1][1:])
            value = int(parts[2])
            self.compare(register_src1, value)
        elif opcode == 'JNE':
            # Handle JNE instruction (conditional jump)
            target_label = parts[1]
            if self.registers['CMP'] != 0:
                self.jump_to_label(target_label)
        elif opcode == 'LOOP_ROW':
            # Handle LOOP_ROW label (start of row loop)
            self.loop_stack.append(self.pc)  # Push the current PC to the stack
        elif opcode == 'LOOP_COL':
            # Handle LOOP_COL label (start of column loop)
            if not self.loop_stack:
                raise ValueError("LOOP_COL without LOOP_ROW")
            # Jump back to the start of the row loop
            self.pc = self.loop_stack[-1]
        else:
            raise ValueError(f"Unknown instruction: {opcode}")

        self.pc += 1  # Increment program counter after executing an instruction

    def load(self, register, mem_addr):
        # Simulated loading from memory address mem_addr into register
        self.registers[register] = self.memory.read(mem_addr)

    def store(self, register, mem_addr):
        # Simulated storing data from register into memory address mem_addr
        self.memory.write(mem_addr, self.registers[register])

    def add(self, register_dest, register_src1, value):
        # Simulated ADD operation
        self.registers[register_dest] = self.registers[register_src1] + value

    def divide(self, register_dest, register_src1, value):
        # Simulated DIV operation
        self.registers[register_dest] = self.registers[register_src1] // value

    def compare(self, register_src1, value):
        # Simulated CMP operation (compare)
        self.registers['CMP'] = self.registers[register_src1] - value

    def jump_to_label(self, label):
        # Simulated jump to a label in the code
        for idx, instruction in enumerate(self.instructions):
            if label in instruction:
                self.pc = idx
                break

    def flatten_bmp(self,image_path, memory, image_width, image_height):
        # Simulated function to flatten a BMP image and load it into memory
        # In practice, you would use a BMP parsing library to load the image data
        with open(image_path, 'rb') as bmp_file:
            # Read BMP data and flatten it
            bmp_data = bmp_file.read()
            memory_size = image_width * image_height * 3
            if len(bmp_data) != memory_size:
                raise ValueError("Image dimensions do not match memory size")
            for mem_addr in range(memory_size):
                memory.write(mem_addr, bmp_data[mem_addr])

def grayscale_weighted(file_path, output_file):
    """
    Converts a BMP image to grayscale using weighted sum of RGB values.

    Parameters:
    - file_path (str): Path to the BMP image file to be converted.
    - output_file (str): Path to save the grayscaled BMP image.

    Description:
    This function reads pixel data from the provided BMP image and converts 
    each pixel to grayscale using a weighted sum of its RGB values. The weights 
    are chosen based on the typical human eye's sensitivity to RGB colors, which 
    is more sensitive to green and less to blue.

    The weighted grayscale formula used is:
    Gray = 0.299 * R + 0.587 * G + 0.114 * B

    Once the image is converted to grayscale, the function saves the result 
    to the specified output file path.

    Example Usage:
    grayscale_weighted("path_to_original.bmp", "path_to_save_grayscale.bmp")
    """
    header, pixels, width, height = get_pixels_from_bmp(file_path)
    
    # Convert each pixel to grayscale using weighted sum
    gray_pixels = [
        (
            int(0.299 * r + 0.587 * g + 0.114 * b),
            int(0.299 * r + 0.587 * g + 0.114 * b),
            int(0.299 * r + 0.587 * g + 0.114 * b)
        ) 
        for (b, g, r) in pixels
    ]

    save_pixels_to_bmp(output_file, header, gray_pixels, width, height)

def reduce_colors(file_path, percentage):
    """
    This function reduces the number of colors in an image.
    It works by quantizing the color channels. If percentage=50%, then
    colors are rounded to the nearest half of 255 (i.e., 0 or 128).
    """
    header, pixels, _, _ = get_pixels_from_bmp(file_path)
    factor = int(255 * (percentage / 100))
    new_pixels = [(blue - blue % factor, green - green % factor, red - red % factor) for blue, green, red in pixels]
    
    # Write back to the BMP
    with open("reduced_colors_" + file_path, 'wb') as f:
        flat_pixels = [byte for pixel in new_pixels for byte in pixel]
        f.write(header + bytearray(flat_pixels))

def reduce_colors1(file_path, output_file, k=64):
    """
    Reduces the number of unique colors in a BMP image.

    Parameters:
    - file_path (str): Path to the BMP image file to be processed.
    - output_file (str): Path to save the BMP image with reduced colors.
    - k (int): The target number of unique colors in the resulting image.

    Description:
    This function reduces the number of unique colors in a BMP image by 
    mapping each original color to the nearest of a set of representative colors. 
    The image's colors are reduced to a predefined set of k unique colors by 
    quantizing the 8-bit RGB values. This is achieved by dividing the value 
    of each color channel (R, G, and B) by a quantization step and then multiplying 
    it back to get the representative color.

    The quantization step is derived as:
    quantization_step = 256 / k

    Each RGB channel of a pixel is transformed as:
    new_value = int(old_value / quantization_step) * quantization_step

    The transformed pixel values will have fewer unique colors while retaining 
    the overall appearance and structure of the original image.

    Note:
    Reducing the number of colors may result in loss of image details and 
    noticeable color banding, especially if k is set to a very small value.

    Example Usage:
    reduce_colors("path_to_original.bmp", "path_to_reduced.bmp", k=32)
    """
    
    header, pixels, width, height = get_pixels_from_bmp(file_path)

    # Determine quantization step based on target number of colors
    quantization_step = 256 // k

    # Reduce number of colors by quantizing pixel values
    quantized_pixels = [
        (
            int(b // quantization_step) * quantization_step,
            int(g // quantization_step) * quantization_step,
            int(r // quantization_step) * quantization_step
        ) 
        for (b, g, r) in pixels
    ]

    save_pixels_to_bmp(output_file, header, quantized_pixels, width, height)

def get_approximately_unique_colors(file_path, threshold=30):
    """
    Determines the number of unique colors in a BMP image within a certain color distance.

    Parameters:
    - file_path (str): Path to the BMP image file.
    - threshold (int): The distance threshold to consider two colors as similar.

    Returns:
    - int: The number of approximately unique colors found in the image.

    Description:
    This function extracts pixel data from the provided BMP image and determines 
    the number of unique colors present, within a certain color distance. Each 
    pixel's color is represented as a tuple of (Blue, Green, Red) values. The 
    function analyzes the entire image to create a set of representative colors, 
    and then returns the size of this set, representing the number of 
    approximately unique colors.

    Colors are considered similar if their Euclidean distance in the RGB space 
    is less than the provided threshold.

    Example Usage:
    unique_colors = get_approximately_unique_colors("path_to_file.bmp", 40)
    """
    def color_distance(color1, color2):
        return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

    header, pixels, _, _ = get_pixels_from_bmp(file_path)
    unique_colors = []

    for pixel in pixels:
        if not any(color_distance(pixel, color) <= threshold for color in unique_colors):
            unique_colors.append(pixel)

    return len(unique_colors)

def get_pixels_from_bmp(file_path):
    """
    Extracts pixel data from a BMP image file.

    Parameters:
    - file_path (str): Path to the BMP image file.

    Returns:
    - header (bytes): The header section of the BMP file.
    - pixels (list of tuples): A list where each tuple represents a pixel in the 
                               format (Blue, Green, Red).
    - width (int): The width of the image in pixels.
    - height (int): The height of the image in pixels.

    Description:
    BMP files have a header that contains metadata about the image, such as its 
    width, height, and color depth. This function reads the BMP file, extracts 
    this metadata, and then reads the pixel data.

    The pixel data is stored in rows (from bottom to top) and in each row, pixels 
    are stored from left to right. Each pixel is represented by three bytes, 
    denoting its Blue, Green, and Red channels respectively. This function 
    returns the pixel data in a flattened list, where each item is a tuple 
    representing a pixel.

    This function assumes the BMP is in 24-bit format (3 bytes per pixel), which 
    is a common format. However, BMP files can come in other formats, so 
    more comprehensive BMP readers might need additional logic to handle 
    those cases.

    Example Usage:
    header, pixels, width, height = get_pixels_from_bmp("path_to_file.bmp")

    Note:
    While BMPs can vary in their internal structure, this function is designed 
    for the common 24-bit BMP format and may not be compatible with all BMP files.
    """
    with open(file_path, 'rb') as file:
        header = file.read(54)
        width = header[18] + header[19] * 256
        height = header[22] + header[23] * 256

        pixels = []
        for y in range(height):
            for x in range(width):
                pixel = tuple(file.read(3))
                pixels.append(pixel)
    return header, pixels, width, height


if __name__ == '__main__':
    pass
