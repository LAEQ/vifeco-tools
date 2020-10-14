import os
import json
import glob
import argparse

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


def reconcile(_category, models):
    """
    Return id from model for a category if names are equals
    :param _category: cat to reconcile
    :param models: List of categories from the model
    :return: int|None
    """
    try:
        return models[_category['name']]
    except KeyError:
        print("'{}' not found.".format(_category['name']))
        print("Model list: {}".format([item for item in models.keys()]))
        return None


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

    with open(MODEL_FILE, 'r') as f:
        model = json.load(f)

    modelSet = {item['name']: item['id'] for item in model['collection']['categorySet']}

    # List of files
    files = glob.glob(SOURCE_FILES)

    for src_file in files:
        src_name = os.path.basename(src_file)

        with open(src_file, 'r', encoding='utf8') as reader:
            print("Converting: {}".format(src_name))
            src_json = json.load(reader)

            categorySet = src_json['collection']['categorySet']
            pointSet = src_json['pointSet']

            # Validation: model and target must have same categories (number and names)
            if len(modelSet) != len(categorySet):
                print("{}'s collection has %d categories but the model has %d.".format(src_name, len(categorySet),
                                                                                       len(modelSet)))
            reconcile_ids = [None] * (max(categorySet, key=lambda x: x['id'])['id'] + 1)
            for category in categorySet:
                identifier = reconcile(category, modelSet)
                # Error category names are not strictly equals: spaces, (upper|lower)case, encoding, accents, ...
                if identifier is None:
                    exit(1)

                reconcile_ids[category['id']] = identifier
                category['id'] = identifier

            for point in pointSet:
                try:
                    id = reconcile_ids[point['categoryId']]
                    point['categoryId'] = id
                except:
                    print("point: %s (file: %s) does not match a category of the model %s".format(
                        point, src_name, args['model']
                    ))
                    exit(1)

            with open(os.path.join(TARGET_PATH, src_name), 'w', encoding='utf8') as writer:
                json.dump(src_json, writer, ensure_ascii=False)

    print(" ----> Reconciliation completed with success.")
