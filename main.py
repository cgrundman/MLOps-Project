import os
import sys


def path():
    print(os.path.dirname(sys.executable))


if __name__ == "__main__":
    path()
