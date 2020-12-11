#!/usr/bin/env python3


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

    number_of_items_in_dictioary = len(file_path_to_sha256_dictionary)
    index_padding_length = len(str(number_of_items_in_dictioary))

    sha_lines = []

    for index, (file_path, sha256) in enumerate(file_path_to_sha256_dictionary.items()):
        padded_index = str(index + 1).rjust(index_padding_length)
        padded_file_name = str(file_path).ljust(longest_path_length)

        sha_line = f"{padded_index} | {padded_file_name} | {sha256}"
        sha_lines.append(sha_line)

    return sha_lines


def print_shas(file_path_to_sha256_dictionary):
    sha_lines = get_sha_lines(file_path_to_sha256_dictionary)

    for sha_line in sha_lines:
        print(sha_line)


def save_file_shas(file_path_to_sha256_dictionary):
    sha_lines = get_sha_lines(file_path_to_sha256_dictionary)

    # Open file and print to it


def main():
    directory_path = Path("/Users/josephlyons/Desktop/file_hasher")
    file_path_to_sha256_dictionary = get_file_path_to_sha256_dictionary(directory_path, {})
    print_shas(file_path_to_sha256_dictionary)


if __name__ == "__main__":
    main()

# Add option to only show relative file paths
# Add option to SHA main file produced?
# Allow user to input what directories they want to run it on, make sure it is a directory
# Potentially swap out the custom recursion function for the directory iterator stuff in python
