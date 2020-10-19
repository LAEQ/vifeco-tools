import argparse
import os
import json
from matplotlib import pyplot as plt
import numpy as np

from utils.display import Display
from utils.model import Point, Graph, Video
from utils.reconcile import parseFile, parseJsonFile, getCategorySet

# Arguments
from utils.statistic import Statistic

parser = argparse.ArgumentParser(description='Match counter video features')
parser.add_argument("--file1", "-f1", required=True, help="vifeco json files")
parser.add_argument("--file2", "-f2", required=True, help="vifeco json files")
parser.add_argument("--delta", "-d", default=5, help="Default delta time in seconds")

args = vars(parser.parse_args())

file1 = args['file1']
file2 = args['file2']


def files_not_valid(f1, f2):
    return (os.path.exists(f1) and os.path.exists(f2)) is False


def menu():
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
    stat = Statistic(video1, Video(json_2))

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



