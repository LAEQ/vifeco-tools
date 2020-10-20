from uuid import uuid4
from typing import List, OrderedDict
from tarjan import tarjan
import collections
from datetime import timedelta

class Point:
    def __init__(self, args):
        self.catgory_id = args['categoryId']
        self.start = args['startDouble']
        self.videoId = args['videoId']
        self.uuid = uuid4()

    def match(self, other, delta):
        if isinstance(other, Point):
            return self.catgory_id == other.catgory_id and abs(self.start - other.start) <= delta

        return False

    def __repr__(self):
        start = timedelta(milliseconds=self.start)
        start = str(start).split(".")[0]

        start = '{:10s}'.format(start)

        return "{%s:%s:%s}" % (self.catgory_id, self.videoId[0:5], start)


class Video:
    def __init__(self, json):
        self.json = json
        self.catDict = {k['id']: k['name'] for k in self.json['collection']['categorySet']}

    def name(self):
        return self.json['path']

    def points(self) -> List[Point]:
        return [Point(params) for params in self.json['pointSet']]

    def category(self, identifier: int) -> str:
        return self.catDict[identifier]

    def totals(self) -> OrderedDict:
        result = {k['id']: 0 for k in self.json['collection']['categorySet']}

        for point in self.points():
            result[point.catgory_id] += 1

        return collections.OrderedDict(sorted(result.items()))

    def id(self):
        return self.json['uuid']

class Graph:
    """
    Graph of points
    """

    def __init__(self, video1: Video, video2: Video, delta=5000):
        self.pts_1 = video1.points()
        self.pts_2 = video2.points()
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
        self.tj_pts = self.tj_to_points()

    def tj_to_points(self):
        pts = self.pts_1 + self.pts_2

        result = []

        for l in self.tj:
            tmp = []
            for uid in l:
                tmp.append(next(pt for pt in pts if pt.uuid == uid))

            result.append(tmp)

        return result

    def tj_by_category(self, catId: int):
        filter_list = list(filter(lambda d: d[0].catgory_id == catId, self.tj_to_points()))
        filter_list.sort(key=lambda x: x[0].start)

        return filter_list
