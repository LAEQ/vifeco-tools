import os
import json
import glob
import argparse

from utils.reconcile import parseFile

# Globals
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(BASE_PATH, "source")
SOURCE_FILES = os.path.join(SOURCE_PATH, "*.json")
TARGET_PATH = os.path.join(BASE_PATH, "target")

# Arguments
parser = argparse.ArgumentParser(description='Reconcile category ids between different vifeco databases')
parser.add_argument("--model", "-m", default="model.json", help="Model to use to reconcile with.")
parser.add_argument("--source", "-s", default=SOURCE_PATH, help="Source folder for json files to convert")
parser.add_argument("--target", "-t", default=TARGET_PATH,
                    help="Folder where the converted json will be saved on success")
args = vars(parser.parse_args())

# Paths from arguments
MODEL_FILE = os.path.join(BASE_PATH, args['model'])
SOURCE_PATH = args['source']
TARGET_PATH = args['target']


if __name__ == "__main__":
    print(" ----> Reconciliation: ...")

    # Validation paths
    if os.path.exists(MODEL_FILE) is False:
        print("You must provide a valid model.json file - File {} not found".format(MODEL_FILE))
        exit(1)

    if os.path.exists(SOURCE_PATH) is False:
        print("Source path is not valid: {}".format(SOURCE_PATH))
        exit(1)

    if os.path.exists(TARGET_PATH) is False:
        print("Target path is not valid: {}".format(TARGET_PATH))
        exit(1)

    for src_file in glob.glob(SOURCE_FILES):
        source_filename = os.path.basename(src_file)
        print("Converting: {}".format(source_filename))
        src_json = parseFile(src_file, MODEL_FILE)

        with open(os.path.join(TARGET_PATH, source_filename), 'w', encoding='utf8') as writer:
            json.dump(src_json, writer, ensure_ascii=False)

    print(" ----> Reconciliation completed with success.")
