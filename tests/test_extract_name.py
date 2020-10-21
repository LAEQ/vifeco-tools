from unittest import TestCase

from utils.tools import extract_name, get_matching_file


class TestGraph(TestCase):
    def test_extract_name(self):
        path = 'report/jode/ID1_PA_2019-09-10_TRAJET04.mp4-1603230567330.json'

        result = extract_name(path)
        expected = 'ID1_PA_2019-09-10_TRAJET04.mp4'

        self.assertEqual(expected, result)

    def test_extract_name(self):
        path = 'report/jode/ID1_PA_2019-09-10_TRAJET04.mp4.json'

        result = extract_name(path)
        expected = 'ID1_PA_2019-09-10_TRAJET04.mp4'

        self.assertIsNone(result)

    def test_matching_file(self):
        list = [
            'report/orane/ID1_PA_2019-09-10_TRAJET04.mp4-1603230567330.json',
            'report/orane/ID1_PA_2019-09-10_TRAJET03.mp4-1603230567330.json',
            'report/orane/ID1_PA_2019-09-10_TRAJET01.mp4-1603230567330.json'
        ]

        file = 'report/jode/ID1_PA_2019-09-10_TRAJET01.mp4-1603230567330.json'

        result = get_matching_file(file, list)
        expected = 'report/orane/ID1_PA_2019-09-10_TRAJET01.mp4-1603230567330.json'
        self.assertEqual(result, expected)

    def test_matching_file_none(self):
        list = [
            'report/orane/ID1_PA_2019-09-10_TRAJET04.mp4-1603230567330.json',
            'report/orane/ID1_PA_2019-09-10_TRAJET03.mp4-1603230567330.json',
            'report/orane/ID1_PA_2019-09-10_TRAJET01.mp4-1603230567330.json'
        ]

        file = 'report/jode/ID1_PA_2019-09-10_TRAJET05.mp4-1603230567330.json'

        result = get_matching_file(file, list)
        self.assertIsNone(result)