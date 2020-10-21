import os
import re


def files_not_valid(f1, f2):
    return (os.path.exists(f1) and os.path.exists(f2)) is False


def extract_name(path):
    name = os.path.basename(path)

    pattern = '^(.*)(-\d+)(.json)$'

    match = re.search(pattern, name)

    try:
        return match.group(1)
    except:
        return None


def get_matching_file(file, files):
    pattern_1 = extract_name(file)
    for file in files:
        pattern_2 = extract_name(file)
        if pattern_1 == pattern_2:
            return file

    return None
