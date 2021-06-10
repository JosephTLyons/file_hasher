#!/usr/bin/env python3

import json
import sys

from hashlib import sha256
from pathlib import Path


def get_file_path_to_sha_256_dictionary(
    directory_path, file_path_to_sha_256_dictionary, should_ignore_hidden_items=True
):
    for item in directory_path.iterdir():
        if should_ignore_hidden_items and item.name.startswith("."):
            continue

        if item.is_file():
            with open(item, "rb") as file:
                bytes_string = file.read()
                sha_256_string = sha256(bytes_string).hexdigest()
                file_path_to_sha_256_dictionary[str(item)] = sha_256_string
        elif item.is_dir():
            get_file_path_to_sha_256_dictionary(item, file_path_to_sha_256_dictionary)

    return file_path_to_sha_256_dictionary


def get_sha_lines(file_path_to_sha_256_dictionary):
    longest_path_length = len(
        str(
            max(
                file_path_to_sha_256_dictionary.keys(),
                key=lambda path_object: len(str(path_object)),
            )
        )
    )

    number_of_items_in_dictionary = len(file_path_to_sha_256_dictionary)
    index_padding_length = len(str(number_of_items_in_dictionary))

    sha_lines = []

    for index, (file_path, sha_256) in enumerate(file_path_to_sha_256_dictionary.items()):
        padded_index = str(index + 1).rjust(index_padding_length)
        padded_file_name = str(file_path).ljust(longest_path_length)

        sha_line = f"{padded_index} | {padded_file_name} | {sha_256}"
        sha_lines.append(sha_line)

    return sha_lines


def print_sha_lines_to_console(sha_lines):
    for sha_line in sha_lines:
        print(sha_line)


def serialize_file_path_to_sha_256_dictionary(file_path_to_sha_256_dictionary, output_file_path):
    with open(output_file_path, "w") as output_file:
        json.dump(file_path_to_sha_256_dictionary, output_file, indent=4)


def compare(new_file_path_to_sha_256_dictionary, output_file_path):
    with open(output_file_path, "r") as output_file:
        old_file_path_to_sha_256_dictionary = json.load(output_file)

        for new_file_path, new_sha_256 in new_file_path_to_sha_256_dictionary.items():
            if new_file_path in old_file_path_to_sha_256_dictionary:
                if new_sha_256 != old_file_path_to_sha_256_dictionary[new_file_path]:
                    print(f"{new_file_path} has changed")
            else:
                print(f"{new_file_path} has been added")


def main():
    if len(sys.argv) != 2:
        print("Must provide a directory path as input")
        sys.exit()

    directory_path = Path(sys.argv[1])

    if not directory_path.exists():
        print("Argument must be a directory path")
        sys.exit()

    file_path_to_sha_256_dictionary = get_file_path_to_sha_256_dictionary(directory_path, {})

    sha_lines = get_sha_lines(file_path_to_sha_256_dictionary)

    # print_sha_lines_to_console(sha_lines)

    output_file_path = directory_path / "file_hashes.txt"

    serialize_file_path_to_sha_256_dictionary(file_path_to_sha_256_dictionary, output_file_path)
    # compare(file_path_to_sha_256_dictionary, output_file_path)


if __name__ == "__main__":
    main()

# Add option to SHA main file produced?
# Potentially swap out the custom recursion function for the directory iterator stuff in python
