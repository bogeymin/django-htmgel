#! /usr/bin/env python

# Imports

import os

# Helpers


def get_comments(path):
    """Get comments from a file.

    :param path: Path to the file.
    :type path: str

    :rtype: str

    """
    with open(path, "rb") as f:
        content = f.read()
        f.close()

        inner = False
        output = list()
        for line in content.split("\n"):
            if line == '{% comment %}':
                inner = True
                continue
            elif line == '{% endcomment %}':
                inner = False
                break
            else:
                pass

            if inner:
                output.append(line)

        return "\n".join(output)


# This is the path to the templates.
INPUT_PATH = "../htmgel/templates/htmgel"

# Get entries on the input path.
entries = os.listdir(INPUT_PATH)
templates = list()
for e in entries:
    path = os.path.join(INPUT_PATH, e)
    if os.path.isfile(path):
        templates.append(path)

# Start output for the documentation file.
output = list()
output.append(".. Generated by extract_template_comments.py")
output.append("")
output.append("*********")
output.append("Templates")
output.append("*********")
output.append("")

# Load each template and extract the comments.
for t in templates:
    comment = get_comments(t)
    output.append(comment)
    output.append("")

# Write the templates documentation.
OUTPUT_PATH = "source/templates.rst"
with open(OUTPUT_PATH, "wb") as f:
    f.write("\n".join(output))
    f.close()
