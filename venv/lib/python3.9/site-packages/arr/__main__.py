import argparse
from arr.star import Star
import pickle
import sys
import subprocess

def main(args = None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()

    parser.add_argument("target", help="Target to resolve refrences. Must be a name that is resolvable by "
                                       "Simbad.", type=str)

    args = parser.parse_args(args)
    print("Collecting data ... ")
    s = Star(args.target)
    print("Starting shell ... ")
    pickle.dump(s, open("i_obj.arr", "wb"))
    cmd = ["ipython", "-i", "-c",
           "from arr import Star,Gaia,Tess,Simbad,Reference;import pickle;star : Star = pickle.load(open('i_obj.arr', 'rb'));import os;os.remove('i_obj.arr');import matplotlib.pyplot as pl;pl.ion()"]
    subprocess.call(cmd)

if __name__ == "__main__":
    main()