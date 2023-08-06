import argparse
import string
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Assign seats to students automatically.")

    parser.add_argument("student", help="CSV file containing student list")
    parser.add_argument("seats", help="Yaml file containing room seating info")

    parser.add_argument("--partner", help="CSV file student partner history")
    parser.add_argument("--out", help="Output file", default="chart.txt")
    parser.add_argument("--fmt", help="Output format string", default="{sid}")
    parser.add_argument("--g_chart", help="Output pdf file for student chart", default="chart.pdf")
    parser.add_argument("--stdt_sort", help="Sort the output chart by student key intead of by seating key", action='store_true')
    parser.add_argument("--g_chart_size", help="Image size of output chart", nargs=2, type=int, default=[1000,1400])
    parser.add_argument("--g_room", help="Output image file for room image", default="room.jpg")
    parser.add_argument("--g_room_size", help="Image size of output room", nargs=2, type=int, default=[1400,1000])
    parser.add_argument("--seed", help="Seed", default=int(time.time()))
    parser.add_argument("--algorithm", help="Choose algorithm to use", default="ConsecDivide")
    parser.add_argument("--eval", help="Evaluate algorithm", action='store_true')
    parser.add_argument("--nosave", help="Don't save results to files", action='store_true')
    return parser.parse_args()

class SliceFormatter(string.Formatter):
    def get_value(self, key, args, kwds):
        if '|' in key:
            try:
                key, indexes = key.split('|')
                split_indexes = indexes.split(',')

                if len(split_indexes) == 1:
                    # For singular slice
                    index_itr = map(int, [int(split_indexes[0]), int(split_indexes[0])+1])
                elif len(split_indexes) == 2:
                    # For dual ended slice
                    index_itr = map(int, split_indexes)
                else:
                    raise Exception("Slice format incorrect {}".format(key))

                return kwds[key][slice(*index_itr)]
            except KeyError:
                return kwds.get(key, 'Missing')
        return super(SliceFormatter, self).get_value(key, args, kwds)
