import argparse
import os

from utils.model import Video
from utils.reconcile import parseFile, parseJsonFile

# Arguments
from utils.statistic import Statistic
from utils.tools import files_not_valid

parser = argparse.ArgumentParser(description='Match counter video features')
parser.add_argument("--file1", "-f1", type=str, required=True, help="vifeco json files")
parser.add_argument("--file2", "-f2", type=str, required=True, help="vifeco json files")
parser.add_argument("--delta", "-d", type=int, default=5000, help="Default delta time in milliseconds")

args = vars(parser.parse_args())

file1 = args['file1']
file2 = args['file2']
delta = args['delta']


def menu():
    if file1 == file2:
        print("It is useless to compare the same files. They match at 100%")
        exit(0)

    print("Select an operation or quit.")
    print("1. Show all")
    print("2. Show one category")
    print("0. Quit")

    is_not_valid = True

    while is_not_valid:
        try:
            choice = int(input())
        except:
            print("Not valid")

        if choice not in [1, 2, 0]:
            print("Not valid")
        else:
            return choice


def menu_category(categories):
    print("Select a category: ")
    for key, value in categories.items():
        print("{} - {}".format(key, value))

    while True:
        try:
            choice = int(input())
            if choice not in categories.keys():
                raise Exception
            else:
                return choice
        except:
            print("invalid")


if __name__ == '__main__':
    if files_not_valid(file1, file2):
        print("One of the files path is not valid")
        exit(1)

    # Convert categories ids
    json_1 = parseJsonFile(file1)
    json_2 = parseFile(file2, file1)

    videoIds = [json_1['uuid'], json_2['uuid']]

    video1 = Video(json_1)
    stat = Statistic(video1, Video(json_2), delta)

    while True:
        choice = menu()
        if choice == 0:
            print("Bye")
            exit(0)
        elif choice == 1:
            stat.summary()
        elif choice == 2:
            choice = menu_category(video1.catDict)
            stat.show_category(choice)



