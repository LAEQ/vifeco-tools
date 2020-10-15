from unittest import TestCase

from utils.model import Point


class TestPoint(TestCase):
    @staticmethod
    def get_point_1():
        return Point({
              "id": 17,
              "x": 0.3701188455008489,
              "y": 0.46934540652707035,
              "categoryId": 12,
              "startDouble": 10000.0,
              "videoId": "8ce5818b-5975-4d97-9df6-548f9376b5f0"
            })

    @staticmethod
    def get_point_2():
        return Point({
              "id": 17,
              "x": 0.3701188455008489,
              "y": 0.46934540652707035,
              "categoryId": 12,
              "startDouble": 15000.0,
              "videoId": "8ce5818b-5975-4d97-9df6-548f9376b5f0"
            })

    @staticmethod
    def get_point_3():
        return Point({
              "id": 17,
              "x": 0.3701188455008489,
              "y": 0.46934540652707035,
              "categoryId": 11,
              "startDouble": 15000.0,
              "videoId": "8ce5818b-5975-4d97-9df6-548f9376b5f0"
            })

    @staticmethod
    def get_point_4():
        return Point({
              "id": 17,
              "x": 0.3701188455008489,
              "y": 0.46934540652707035,
              "categoryId": 12,
              "startDouble": 15000.00000000001,
              "videoId": "8ce5818b-5975-4d97-9df6-548f9376b5f0"
            })

    def test_constructor(self):
        pt1 = self.get_point_1()
        self.assertIsInstance(pt1, Point)

    def test_match(self):
        pt1 = self.get_point_1()
        pt2 = self.get_point_2()

        self.assertTrue(pt1.match(pt2))

    def test_not_match_category(self):
        pt1 = self.get_point_1()
        pt3 = self.get_point_3()

        self.assertFalse(pt1.match(pt3))

    def test_not_match_delta(self):
        pt1 = self.get_point_1()
        pt4 = self.get_point_4()

        self.assertFalse(pt1.match(pt4))