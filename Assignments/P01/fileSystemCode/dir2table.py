import os
import sys


def generate_markdown(directory):
    markdown = "| File/Folder | Path |\n| --- | --- |\n"

    for root, dirs, files in os.walk(directory):
        for name in dirs + files:
            if name.startswith("."):
                continue
            path = os.path.join(root, name)
            relative_path = os.path.relpath(path, directory)
            markdown += f"| {name} | [{relative_path}]({relative_path}) |\n"

    return markdown


if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."  # Replace with your desired path

    markdown = generate_markdown(directory)

    with open("README.md", "a") as readme_file:
        readme_file.write(markdown)
