"""Main module of the third task."""
import hashlib
import os
import re
import sys
from logger_setup import logger


def split_line_if_valid(line, line_number):
    items = line.split()
    if len(items) != 3:
        logger.warning("Skipping line {}: wrong file information. Should be <file name> <md5|sha1|sha256> <checksum>."
                       .format(line_number))
        return None
    elif not re.match(r'^([^/><|:&]+)', items[0]):
        logger.warning("Skipping line {}: filename contains illegal symbols: {}.".format(line_number, items[0]))
        return None
    elif not re.match(r'(sha(?:1|256)|md5)', items[1]):
        logger.warning("Skipping line {}: Unknown hashing algorithm: {}.".format(line_number, items[1]))
        return None
    elif not re.match(r'([a-fA-F0-9]+)', items[2]):
        logger.warning("Skipping line {}: checksum contains illegal symbols: {}.".format(line_number, items[2]))
        return None
    else:
        return items


def get_checksum(algorithm, file_name):
    """Gets checksum for the specified file file_name by using the specified algorithm.

    Args:
      algorithm: string representing the algorithm
      file_name: file to calculate checksum for

    Returns:
      file's checksum
    """
    hash_algorithm = getattr(hashlib, algorithm)()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_algorithm.update(chunk)
    return hash_algorithm.hexdigest()


def check_argv(argv):
    """Checks if all CLI arguments are present.

    Args:
      argv: sys.argv variable

    Raises:
        ValueError if Invalid file or directory path was passed.
        TypeError if something other than sys.argv was passed.
    """
    if type(argv) is list:
        if len(argv) != 3:
            raise ValueError('Program should be run with 2 arguments as {} <path to file> <path to directory>'
                             .format(__file__))
        if not os.path.isfile(argv[1]):
            raise ValueError('Invalid file path.')
        if not os.path.isdir(sys.argv[2]):
            raise ValueError('Invalid directory path.')
    else:
        raise TypeError("sys.argv must be list.")


def check_checksum_correctness_for_file(file_info_items):
    """Calculates checksum for the file from the files list (if the file is present in the directory)
    and defines if the checksum from the text file is the same as the calculated value by creating a log record.

    Args:
      file_info_items: a list with file name, algorithm type and checksum to be compared with the calculated one
    """
    file_name, algorithm, checksum = file_info_items
    if os.path.isfile(os.path.join(dir_path, file_name)):
        calc_checksum = get_checksum(algorithm, os.path.join(dir_path, file_name))
        if calc_checksum == checksum:
            logger.info('{} OK'.format(file_name))
        else:
            logger.info('{} FAIL'.format(file_name))
    else:
        logger.info('{} NOT FOUND'.format(file_name))


if __name__ == "__main__":
    check_argv(sys.argv)
    file_path = sys.argv[1]
    dir_path = sys.argv[2]
    with open(file_path, 'r') as input_file:
        # Serial computing of each file's checksum is more effective than using multiprocessing.Pool
        for line_number, line in enumerate(input_file):
            file_info_items = split_line_if_valid(line, line_number)
            if file_info_items is None:
                continue
            check_checksum_correctness_for_file(file_info_items)




