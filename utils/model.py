from uuid import uuid1


class Point:
    def __init__(self, args):
        self.catgory_id = args['categoryId']
        self.start = args['startDouble']
        self.videoId = args['videoId']
        self.uuid = uuid1()

    def match(self, other, delta=5000):
        if isinstance(other, Point):
            return self.catgory_id == other.catgory_id and abs(self.start - other.start) <= delta

        return False
