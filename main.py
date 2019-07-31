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


def read_line(file):
    """Generator to read a large file lazily"""
    while True:
        line = file.readline()
        if not line:
            break
        yield line


def parse_file(filepath):
    """top entry read filepath,return all tournament, set, game, score"""
    try:
        with open(filepath) as file_handler:
            for line in read_line(file_handler):
                # process line
                line = line.strip()
                if line:
                    print(line)
    except Exception as ex:
        print("Error: {ex}")


if __name__ == '__main__':
    filepath = validate_input(sys.argv)
    if not filepath:
        print('Please input a valid file.')
        exit(1)

    print(f'{filepath} loaded.')

    tournament = parse_file(filepath)

    print(tournament)
    # todo user input query
