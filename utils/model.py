from uuid import uuid4
from typing import List
from tarjan import tarjan
import numpy as np

class Point:
    def __init__(self, args):
        self.catgory_id = args['categoryId']
        self.start = args['startDouble']
        self.videoId = args['videoId']
        self.uuid = uuid4()

    def match(self, other, delta=5000):
        if isinstance(other, Point):
            return self.catgory_id == other.catgory_id and abs(self.start - other.start) <= delta

        return False

    def __repr__(self):
        return "{%s: %s}" % (self.catgory_id, self.start)


class Graph:
    """
    Graph of points
    """
    def __init__(self, pts_1: List[Point], pts_2: List[Point], delta=5000):
        self.pts_1 = pts_1
        self.pts_2 = pts_2
        self.delta = delta

        self.graph = {p.uuid: [] for p in self.pts_1}
        self.graph.update({p.uuid: [] for p in self.pts_2})

        for pt1 in self.pts_1:
            for pt2 in self.pts_2:
                if pt1.match(pt2, self.delta):
                    self.graph[pt1.uuid].append(pt2.uuid)

        for pt2 in self.pts_2:
            for pt1 in self.pts_1:
                if pt2.match(pt1, self.delta):
                    self.graph[pt2.uuid].append(pt1.uuid)

        self.tj = tarjan(self.graph)

    def plot(self):
        pts = self.pts_1 + self.pts_2

        result = []

        for l in self.tj:
            tmp = []
            for uid in l:
                tmp.append(next(pt for pt in pts if pt.uuid == uid))

            result.append(tmp)

        return result