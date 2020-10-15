import json


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


def getCategorySet(file):
    video = parseJsonFile(file)

    return {item['name']: item['id'] for item in video['collection']['categorySet']}


def parseJsonFile(file):
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)


def parseFile(source_file, model_file):
    model = parseJsonFile(model_file)

    model_set = {item['name']: item['id'] for item in model['collection']['categorySet']}

    source_json = parseJsonFile(source_file)
    category_set = source_json['collection']['categorySet']
    point_set = source_json['pointSet']

    # Validation: model and target must have same categories (number and names)
    if len(model_set) != len(category_set):
        print("Collection has %d categories but the model has %d.".format(len(category_set), len(model_set)))

    reconcile_ids = [None] * (max(category_set, key=lambda x: x['id'])['id'] + 1)
    for category in category_set:
        identifier = reconcile(category, model_set)
        # Error category names are not strictly equals: spaces, (upper|lower)case, encoding, accents, ...
        if identifier is None:
            exit(1)

        reconcile_ids[category['id']] = identifier
        category['id'] = identifier

    for point in point_set:
        try:
            id = reconcile_ids[point['categoryId']]
            point['categoryId'] = id
        except:
            print("point: %s does not match a category of the model ".format(point))
            exit(1)

    source_json['collection'] = model['collection']

    return source_json
