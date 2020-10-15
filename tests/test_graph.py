from unittest import TestCase

from utils.model import Point, Graph


class TestGraph(TestCase):
    @staticmethod
    def get_pts_1():
        return [Point({"id": 17,
                       "x": 0.3701188455008489,
                       "y": 0.46934540652707035,
                       "categoryId": 11,
                       "startDouble": 1000 * i,
                       "videoId": "1"
                       }) for i in range(0, 3)]

    @staticmethod
    def get_pts_2():
        return [Point({"id": 17,
                       "x": 0.3701188455008489,
                       "y": 0.46934540652707035,
                       "categoryId": 11,
                       "startDouble": 1000 * i,
                       "videoId": "2"
                       }) for i in range(0, 3)]

    @staticmethod
    def get_pts_2():
        return [Point({"id": 17,
                       "x": 0.3701188455008489,
                       "y": 0.46934540652707035,
                       "categoryId": 11,
                       "startDouble": 1000 * i,
                       "videoId": "2"
                       }) for i in range(0, 3)]

    def test_graph_init(self):
        graph = Graph(self.get_pts_1(), self.get_pts_2())

        self.assertEqual(len(graph.graph), 6)

    def test_tarjan_1(self):
        graph = Graph(self.get_pts_1(), self.get_pts_2())
        tj = graph.tj

        self.assertEqual(len(tj), 1)
        self.assertEqual(len(tj[0]), 6)

    def test_tarjan_2(self):
        graph = Graph(self.get_pts_1(), self.get_pts_2(), delta=100)
        result = [len(l) for l in graph.tj]

        self.assertListEqual([2, 2, 2], result)

        groups = graph.plot()
        print(groups)

    def test_plot(self):
        graph = Graph(self.get_pts_1(), self.get_pts_2())
        plot = graph.plot()

        print(plot)
