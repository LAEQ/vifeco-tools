from matplotlib import pyplot as plt
import numpy as np

plt.style.use('ggplot')


class Display:
    def __init__(self, categories, video_ids, datas):
        self.categories = categories
        self.video_ids = video_ids
        self.datas = self.parse_data(datas)

        index, jndex = self.plot_indexes()

        fig, axs = plt.subplots(index, jndex, squeeze=False)
        plt.title('video name')

        print(index, jndex)

        x = 0
        y = 0

        for cat, values in self.datas:
            print('cat')
            totals = np.array([self.total(item) for item in values])
            both = totals[:, 0]
            file_1 = totals[:, 1]
            file_2 = totals[:, 2]

            ind = [x for x, _ in enumerate(totals)]

            axs[x, y].bar(ind, both, width=0.8, label='both', color='gold', bottom=file_1+file_2)
            axs[x, y].bar(ind, file_1, width=0.8, label='file_1', color='silver', bottom=file_2)
            axs[x, y].bar(ind, file_2, width=0.8, label='file_2', color='#CD853F')
            axs[x, y].set_title(cat['name'], fontsize=10)

            axs[x, y].legend(loc="upper right")
            #
            y += 1
            if y >= jndex:
                y = 0
                x +=1

    def plot_indexes(self):
        i = int(len(self.datas) / 2)
        j = int(len(self.datas) / i) + 1
        return  i, j

    def parse_data(self, datas):
        result = []
        for index, category in enumerate(self.categories, 1):
            filter_list = list(filter(lambda d: d[0].catgory_id == category['id'], datas))
            filter_list.sort(key=lambda x: x[0].start)

            if len(filter_list) > 0:
                del(category['icon'])
                del(category['shortcut'])
                del(category['color'])
                result.append((category, filter_list))

        return result

    def get_plots(self):
        return plt.subplots(self.i, self.j)

    def show(self):
        plt.show()

    def total(self, items):
        tmp = {id: 0 for id in self.video_ids}

        for item in items:
            tmp[item.videoId] += 1

        min_value = min(tmp.values())

        return [min_value] + [max(0, item - min_value) for item in tmp.values()]
