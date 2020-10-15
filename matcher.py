import argparse
import os
import json

from utils.reconcile import parseFile

# Arguments
parser = argparse.ArgumentParser(description='Match counter video features')
parser.add_argument("--file1", "-f1", required=True, help="vifeco json files")
parser.add_argument("--file2", "-f2",   required=True, help="vifeco json files")
parser.add_argument("--delta", "-d", default=5, help="Default delta time in seconds")

args = vars(parser.parse_args())

file1 = args['file1']
file2 = args['file2']


def files_not_valid(f1, f2):
    return (os.path.exists(f1) and os.path.exists(f2)) is False


if __name__ == '__main__':
    if files_not_valid(file1, file2):
        print("One of the files path is not valid")
        exit(1)

    # Convert categories ids
    json_2 = parseFile(file2, file1)

    graph = {}

