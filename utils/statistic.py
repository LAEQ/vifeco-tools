from utils.model import Graph, Video
from datetime import timedelta


class Statistic:
    """
    Display result from 2 couting files from vifeco
    """
    def __init__(self, video1: Video, video2: Video):
        self.video1 = video1
        self.video2 = video2
        self.video_ids = [self.video1.id(), self.video2.id()]
        self.graph = Graph(video1, video2)

    def summary(self):
        """
        Display a summarized counts between 2 files
        :return: None
        """
        data = []

        for key, value in self.video1.totals().items():
            tmp = [key, value, 0]
            data.append(tmp)

        for key, value in self.video2.totals().items():
            for row in data:
                if row[0] == key:
                    row[2] = value

        for row in data:
            id = row[0]
            row.insert(1, self.video1.catDict[id].strip())

        columns = ("id", "Name", "File 1", "File 2")
        output = ['{:>20}'.format(item) for item in columns]
        print("|".join(output))

        for row in data:
            output = ['{:20}'.format(row[0]), '{:20.20}'.format(row[1]), '{:>20}'.format(row[2]),
                      '{:>20}'.format(row[3])]

            print("|".join(output))

        # Matplot lib version to de continue.
        # fig = plt.figure(dpi=80)
        # ax = fig.add_subplot(1, 1, 1)
        # table = ax.table(cellText=data, loc='center', colLabels=columns)
        # table.auto_set_font_size(False)
        # table.set_fontsize(12)
        # ax.axis('off')
        # plt.show()

    def parse(self, items):
        tmp = {id: 0 for id in self.video_ids}

        for item in items:
            tmp[item.videoId] += 1

        min_value = min(tmp.values())

        return [min_value] + [max(0, item - min_value) for item in tmp.values()]

    def show_category(self, cat_id: int):
        """
        Show a table of grouped points following tarjan algorithm
        :param cat_id:
        :return: None
        """
        tj_cat = self.graph.tj_by_category(cat_id)

        if len(tj_cat) > 0:
            columns = ("time", "Both", 'Video 1', 'Video 2')
            output = ['{:>10}'.format(item) for item in columns]
            print("|".join(output))
            for group in tj_cat:
                pt = group[0]
                start = timedelta(milliseconds=pt.start)
                start = str(start).split(".")[0]

                row = ['{:10s}'.format(start)]
                parsed = self.parse(group)
                row.append('{:10d}'.format(parsed[0]))
                row.append('{:10d}'.format(parsed[1]))
                row.append('{:10d}'.format(parsed[2]))
                print("|".join(row))
