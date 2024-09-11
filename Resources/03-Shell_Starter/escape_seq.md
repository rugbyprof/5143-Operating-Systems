Here is a list of **typical terminal escape sequences** for key presses like arrows, backspace, and control keys. These sequences are captured when interacting with terminal-based applications (e.g., text editors, shell scripts).

### Arrow Keys

- **Up Arrow**: `\033[A` (or `\x1b[A`)
- **Down Arrow**: `\033[B` (or `\x1b[B`)
- **Right Arrow**: `\033[C` (or `\x1b[C`)
- **Left Arrow**: `\033[D` (or `\x1b[D`)

### Backspace

- **Backspace**: `\x7f` (common) or `\x08` (sometimes used)

### Control Keys

- **Ctrl + C**: `\003` (or `\x03`) – Interrupt signal (SIGINT)
- **Ctrl + D**: `\004` (or `\x04`) – End of transmission (EOF)
- **Ctrl + Z**: `\032` (or `\x1A`) – Suspend (SIGTSTP)
- **Ctrl + A**: `\001` (or `\x01`) – Move to beginning of the line
- **Ctrl + E**: `\005` (or `\x05`) – Move to end of the line
- **Ctrl + L**: `\014` (or `\x0C`) – Clear screen

### Enter/Return Key

- **Enter/Return**: `\r` or `\n`, often both `\r\n` (depending on the system).

### Escape Key

- **Escape**: `\033` (or `\x1b`)

### Tab Key

- **Tab**: `\011` (or `\x09`)

### Function Keys (F1–F12)

- **F1**: `\033[OP`
- **F2**: `\033[OQ`
- **F3**: `\033[OR`
- **F4**: `\033[OS`
- **F5**: `\033[15~`
- **F6**: `\033[17~`
- **F7**: `\033[18~`
- **F8**: `\033[19~`
- **F9**: `\033[20~`
- **F10**: `\033[21~`
- **F11**: `\033[23~`
- **F12**: `\033[24~`

### Home, End, Page Up, Page Down

- **Home**: `\033[H` (or `\x1b[H`)
- **End**: `\033[F` (or `\x1b[F`)
- **Page Up**: `\033[5~`
- **Page Down**: `\033[6~`

### Summary:

- `\033` (or `\x1b`) represents the **escape character**, and is often the beginning of escape sequences.
- **Arrow keys** and **function keys** usually follow the pattern `\033[` or `\033O`.
- **Control characters** typically start with `\x` followed by a specific value, representing the binary value of the control key.

These escape sequences are often used when writing terminal-based applications or scripts that process keyboard inputs in the terminal.

Let me know if you need more information!
