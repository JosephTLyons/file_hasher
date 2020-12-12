#!/usr/bin/env python3

import sys

from hashlib import sha256
from pathlib import Path


def get_file_path_to_sha256_dictionary(directory_path, file_path_to_sha256_dictionary):
    for item in directory_path.iterdir():
        if item.is_file():
            with open(item, "rb") as file:
                bytes_string = file.read()
                sha256_string = sha256(bytes_string).hexdigest()
                file_path_to_sha256_dictionary[item] = sha256_string
        elif item.is_dir():
            get_file_path_to_sha256_dictionary(item, file_path_to_sha256_dictionary)

    return file_path_to_sha256_dictionary


def get_sha_lines(file_path_to_sha256_dictionary):
    longest_path_length = len(
        str(
            max(
                file_path_to_sha256_dictionary.keys(), key=lambda path_object: len(str(path_object))
            )
        )
    )

    number_of_items_in_dictionary = len(file_path_to_sha256_dictionary)
    index_padding_length = len(str(number_of_items_in_dictionary))

    sha_lines = []

    for index, (file_path, sha256) in enumerate(file_path_to_sha256_dictionary.items()):
        padded_index = str(index + 1).rjust(index_padding_length)
        padded_file_name = str(file_path).ljust(longest_path_length)

        sha_line = f"{padded_index} | {padded_file_name} | {sha256}"
        sha_lines.append(sha_line)

    return sha_lines


def print_sha_lines_to_console(sha_lines):
    for sha_line in sha_lines:
        print(sha_line)


def print_sha_lines_to_file(sha_lines, directory_path):
    with open(directory_path / "file_hashes.txt", "w") as output_file:
        for sha_line in sha_lines:
            output_file.write(sha_line + "\n")


def main():
    if len(sys.argv) != 2:
        print("Must provide a directory path as input")
        sys.exit()

    directory_path = Path(sys.argv[1])

    if not directory_path.exists():
        print("Argument must be a directory path")
        sys.exit()

    file_path_to_sha256_dictionary = get_file_path_to_sha256_dictionary(directory_path, {})

    sha_lines = get_sha_lines(file_path_to_sha256_dictionary)

    print_sha_lines_to_console(sha_lines)
    print_sha_lines_to_file(sha_lines, directory_path)


if __name__ == "__main__":
    main()

# Add option to only show relative file paths
# Add option to SHA main file produced?
# Potentially swap out the custom recursion function for the directory iterator stuff in python
