import sys

from t64 import T64ImageReader


with T64ImageReader(sys.argv[1]) as t:
    for line in t.directory('ascii'):
        print(line)
