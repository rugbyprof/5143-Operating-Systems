LOAD R1, 0      # Initialize R1 with 0 (row index)
LOAD R9, 300    # Load R9 with the image width (number of columns)

LOOP_ROW:
  LOAD R2, 1    # Initialize R2 with 1 (column index)
  LOAD R3, 2    # Initialize R3 with 2 (channel index)

  LOOP_COL:
    # Calculate memory addresses for the current pixel and surrounding pixels
    ADD R4, R1, R2   # Calculate memory address for R channel of the current pixel
    ADD R5, R1, R2+1 # Calculate memory address for G channel of the current pixel
    ADD R6, R1, R2+2 # Calculate memory address for B channel of the current pixel
    ADD R7, R4, 300  # Calculate memory address for R channel of the next row's pixel
    ADD R8, R5, 300  # Calculate memory address for G channel of the next row's pixel
    ADD R9, R6, 300  # Calculate memory address for B channel of the next row's pixel

    # Load pixel values into registers
    LOAD R10, R4
    LOAD R11, R5
    LOAD R12, R6
    LOAD R13, R7
    LOAD R14, R8
    LOAD R15, R9

    # Compute moving average (blur)
    ADD R10, R10, R11
    ADD R10, R10, R12
    ADD R10, R10, R13
    ADD R10, R10, R14
    ADD R10, R10, R15
    ADD R10, R10, R16
    ADD R10, R10, R17
    ADD R10, R10, R18
    DIV R10, R10, 9

    # Store the result back to memory
    STORE R10, R4
    STORE R10, R5
    STORE R10, R6

    # Increment column index and check for completion
    ADD R2, R2, 3  # Assuming 3 color channels per pixel
    CMP R2, image_width
    JNE LOOP_COL

  # Increment row index and check for completion
  ADD R1, R1, 1
  CMP R1, image_height
  JNE LOOP_ROW