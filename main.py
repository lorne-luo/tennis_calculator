import os
import re
import sys

from models.tournament import Tournament


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
    tournament = Tournament()
    current_match = None
    match_number = None
    player1 = player2 = None
    try:
        with open(filepath) as file_handler:
            for line in read_line(file_handler):
                # process line
                line = line.strip()
                if not line:
                    continue

                _match_number = search_match(line)
                if _match_number:
                    # new match start
                    current_match = None
                    match_number = _match_number
                    continue

                players = search_player(line)
                if players:
                    # read player
                    player1, player2 = players
                    continue

                if line in ["1", "0"]:
                    # score start, skip invalid score
                    if not current_match:
                        current_match = tournament.create_match(
                            match_number, player1, player2
                        )

                    current_match.add_point(int(line))
    except Exception as ex:
        print(f"Error: {ex}")

    return tournament


def search_match(line):
    p = re.compile("match: ([0-9]*)", re.IGNORECASE)
    result = p.search(line)
    if result and result.group():
        try:
            return int(result.group(1))
        except:
            pass
    return None


def search_player(line):
    p = re.compile("(.*) vs (.*)", re.IGNORECASE)
    result = p.search(line)
    if result and result.group():
        return result.group(1), result.group(2)
    return None


def capture_input(line):
    """capture user query input"""
    # Score Match 01
    # Games Player Person A
    # exit
    if line.lower() == "exit":
        return "exit", None

    match_reg = re.compile("Score Match ([0-9]*)", re.IGNORECASE)
    player_reg = re.compile("Games Player (.*)", re.IGNORECASE)

    result = match_reg.search(line)
    if result and result.group(1):
        return "match", int(result.group(1))
    result = player_reg.search(line)
    if result and result.group(1):
        return "player", result.group(1)

    return None, None


def print_command():
    """print command instructions"""
    print("\nCommand instructions:")
    print("    1. Query match result: `Score Match <id>`")
    print("    2. Query games for player: `Games Player <Player Name>`")
    print("    3. Exit: `exit`")
    print("Please input commandt >>")


if __name__ == "__main__":
    filepath = validate_input(sys.argv)
    if not filepath:
        print("Please input a valid file.")
        exit(1)

    tournament = parse_file(filepath)

    print(f"{filepath} load succeed.")
    print_command()
    while True:
        input_line = input()
        command, param = capture_input(input_line)

        if not command:
            print("Invalid command, please input a valid command >>")
            continue
        if command.lower() == "exit":
            exit(0)

        elif command.lower() == "match":
            match = tournament.get_match(param)
            if not match:
                print(f"Can't found match with number {param}.")
            else:
                match.print()
        elif command.lower() == "player":
            win, lose = tournament.get_player_point(param)
            print(win, lose)

        print_command()
