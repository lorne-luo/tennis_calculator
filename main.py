import sys
import os


def validate_input(argv):
    """validate input file existed"""
    if len(argv) < 2:
        return None

    filepath = argv[1]
    if not os.path.isfile(filepath):
        return None
    return filepath


def parse_file(filepath):
    """top entry read filepath,return all tournament, set, game, score"""

    # raise NotImplementedError


if __name__ == '__main__':
    filepath = validate_input(sys.argv)
    if not filepath:
        print('Please input a valid file.')
        exit(1)

    print(f'{filepath} loaded.')

    # todo user input query
