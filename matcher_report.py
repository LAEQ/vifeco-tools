import argparse
import glob
import os

from utils.model import Video
from utils.reconcile import parseJsonFile, parseFile
from utils.statistic import Statistic
from utils.tools import files_not_valid, get_matching_file, extract_name

parser = argparse.ArgumentParser(description='Match counter video features')
parser.add_argument("--folder1", "-f1", type=str, required=True, help="vifeco json folder 1")
parser.add_argument("--folder2", "-f2", type=str, required=True, help="vifeco json folder 2")
parser.add_argument("--delta", "-d", type=int, default=5000, help="Default delta time in milliseconds")


args = vars(parser.parse_args())
folder1 = args['folder1']
folder2 = args['folder2']
delta = args['delta']


if __name__ == '__main__':
    if files_not_valid(folder1, folder2):
        print("One of the files path is not valid")
        exit(1)

    index = 1
    files1 = glob.glob(os.path.join(folder1, "*.json"), recursive=False)
    files2 = glob.glob(os.path.join(folder2,  "*.json"), recursive=False)

    for file1 in files1:
        file2 = get_matching_file(file1, files2)

        if file1 is not None and file2 is not None:
            json_1 = parseJsonFile(file1)
            json_2 = parseFile(file2, file1)

            videoIds = [json_1['uuid'], json_2['uuid']]

            video1 = Video(json_1)
            stat = Statistic(video1, Video(json_2), delta)
            print("Report {}: File pattern: {}".format(index, extract_name(file1)))
            print(file1)
            print(file2)
            stat.summary()
            print("-------------------------------------")
            print("")

            index += 1
        else:
            print("-------------------------------------")
            print("No match for: {}".format(file1))
            print("-------------------------------------")