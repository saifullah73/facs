from shapely.geometry import MultiPolygon, Polygon, Point
import random
import glob
import os

def parse_poly(lines):
    """ Parse an Osmosis polygon filter file.

        Accept a sequence of lines from a polygon file, return a shapely.geometry.MultiPolygon object.

        http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Format
    """
    in_ring = False
    coords = []

    for (index, line) in enumerate(lines):
        if index == 0 or line.strip() == "":
            # first line is junk. Also skip any blank lines
            continue

        elif index == 1:
            # second line is the first polygon ring.
            coords.append([[], []])
            ring = coords[-1][0]
            in_ring = True

        elif in_ring and line.strip() == 'END':
            # we are at the end of a ring, perhaps with more to come.
            in_ring = False

        elif in_ring:
            # we are in a ring and picking up new coordinates.
            ring.append(list(map(float, line.split())))

        elif not in_ring and line.strip() == 'END':
            # we are at the end of the whole polygon.
            break

        elif not in_ring and line.startswith('!'):
            # we are at the start of a polygon part hole.
            coords[-1][1].append([])
            ring = coords[-1][1][-1]
            in_ring = True

        elif not in_ring:
            # we are at the start of a polygon part.
            coords.append([[], []])
            ring = coords[-1][0]
            in_ring = True
    #     print("coords" + str(coords), "ring  " +str(ring))
    # print("coords" + str(coords), "ring  " + str(ring))
    return MultiPolygon(coords)


def readPolyFiles(poly_directory):
    regions = {}
    os.chdir(poly_directory)
    myFiles = glob.glob('*.poly')
    for fileName in myFiles:
        file = open(fileName)
        multi_poly = parse_poly(file.readlines())
        regions[fileName[:-5]] = multi_poly
    os.chdir("../")
    return regions

# x = readPolyFiles()
# file = open("../poly_files/D12.3.poly")
# poly = parse_poly(file.readlines())
# print(poly)
# min_x, min_y, max_x, max_y = poly.bounds
# random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
# print(random_point)
# print(poly.contains(random_point))