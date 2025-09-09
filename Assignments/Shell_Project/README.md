---
title: "Shell Project"
description: "Implementation of a Basic Shell"
category: "assignment"
tags: ["python", "shell", "commands"]
slug: "Shell_Project"
order: 1
visibility: "public"
---

## Shell Project - Implementation of a Basic Shell

#### Due: 12-10-2024 (Final Exam Day)

**Parts Due Dates**: Dates will be specified as we proceed.

## Overview

In this project, you will implement a basic "shell". A shell is a command-line interface we often interact with, and you should already have a good understanding of its expected behavior. Below is an overview of the actions your shell should perform:

1. Print a prompt (`% `) to the user.
2. Read a command line from stdin.
3. Tokenize (lexically analyze) the command and create an array of command parts (tokens).
4. Parse the token array to identify the command and its arguments.
5. Execute the command:
   - If necessary, create a child process via `fork()`.
   - The child process receives any additional input (arguments) and executes the appropriate command.

## Requirements

- **Languages**: Python or C++
- **Threads (Optional)**:
  - Use threads to execute commands.
  - If no background execution (`&`), wait for the thread to complete before returning control to the shell.
- **Command Features**:
  - Each command returns a string.
  - Commands can accept input from other commands.

Your shell must support the following command types:

### 1. **Exit Command**

- **Command**: `exit`
- **Description**: Terminates the shell.
- **Concepts**: Exiting the shell with system calls like `exit()`.

### 2. **Command without Arguments**

- **Example**: `ls`
- **Description**: Executes a command without arguments and waits for it to complete.
- **Concepts**: Synchronous execution, process forking.

### 3. **Command with Arguments**

- **Example**: `ls -l`
- **Description**: Parses command-line arguments and executes the command.
- **Concepts**: Command-line parameters.

### 4. **Background Execution (`&`)**

- **Example**: `ls &`
- **Description**: Executes a command without blocking, allowing the shell to accept further input immediately.
- **Concepts**: Background execution, signals, asynchronous execution.

### 5. **Output Redirection**

- **Example**: `ls > output.txt`
- **Description**: Redirects the command output to a specified file.
- **Concepts**: File operations, output redirection.

### 6. **Input Redirection**

- **Example**: `sort < inputfile.txt`
- **Description**: Takes input from a file instead of the user’s input.
- **Concepts**: File operations, input redirection.

### 7. **Piping Commands**

- **Example**: `ls -l | more`
- **Description**: Passes the output of one command as input to another command.
- **Concepts**: Pipes, synchronous operations.

### Important Notes

- You must handle all return values correctly (e.g., check for errors when reading from files or executing commands).
- Avoid system calls to the existing shell. For example:
  ```python
  # Incorrect:
  from subprocess import call
  call(["ls", "-l"])
  ```
- Your implementation of commands (like `ls`) should be self-contained and not simply call existing system commands.

## Commands to Implement

| Command | Flags/Params       | Description                                              |
| ------- | ------------------ | -------------------------------------------------------- |
| `ls`    | `-a`               | List all files, including hidden ones.                   |
|         | `-l`               | Long listing format.                                     |
|         | `-h`               | Human-readable file sizes.                               |
| `mkdir` |                    | Create a directory.                                      |
| `cd`    | `directory`        | Change to a named directory.                             |
|         |                    | Change to the home directory if no argument is provided. |
| `pwd`   |                    | Print the current directory.                             |
| `cp`    | `file1 file2`      | Copy file1 to file2.                                     |
| `mv`    | `file1 file2`      | Move or rename file1 to file2.                           |
| `rm`    | `-r`               | Recursively delete a directory.                          |
| `cat`   | `file`             | Display contents of a file.                              |
| `head`  | `-n`               | Display the first `n` lines of a file.                   |
| `tail`  | `-n`               | Display the last `n` lines of a file.                    |
| `grep`  | `'pattern'` `file` | Search for a pattern in a file.                          |
| `wc`    | `-l`               | Count lines in a file.                                   |
|         | `-w`               | Count words in a file.                                   |
| `chmod` | `xxx`              | Change file permissions.                                 |

## Additional Features

### History

- **Command**: `history`
- **Description**: Show a history of all executed commands.
- **Command**: `!x`
- **Description**: Re-execute command `x` from history.

### Help

- Every command should print help information if the user passes `--help` as an argument. Use Python docstrings for this purpose.

## Deliverables

1. **Group Members**  
   List the names, emails, and GitHub usernames of all group members.

2. **Repository**

   - Create a private GitHub repository and invite `rugbyprof` as a collaborator.
   - Each group member must have a copy of the repository on their course repository (in the `assignments/p01` folder).

3. **shell.py**

   - Implement the shell in a modular format with thorough comments.
   - Cite any external resources used, ensuring that external code is properly credited both in the code and the README.

4. **README.md**
   - Include the following:
     - Project Title
     - Project Description
     - Commands Implemented (with the author for each command)
     - Non-working or incomplete features (clearly documented)
     - References for any external resources used
     - Instructions to run the shell

## Example README Structure

```
28 Sep 2023
5143 Shell Project
Group Members:
- Name 1
- Name 2
- Name 3

## Overview:
This project implements a basic shell in Python that supports a variety of commands.

## Instructions:
Run the `shell.py` file and use the following commands...

## Commands:
| Command  | Description                  | Author   |
|----------|------------------------------|----------|
| `ls`     | List files and directories    | Person 1 |
| `pwd`    | Print working directory       | Person 2 |

## Non-Working Components:
List any commands or features that are not fully implemented.

## References:
- Reference 1
- Reference 2
```
