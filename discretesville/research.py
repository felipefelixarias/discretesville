from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from dcprm.dcprm import DCPRM

from json import load
from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser(description="Select environment")
    parser.add_argument('--ville', metavar='Environment', help='Path to environment json',default="visualize/villes/testville.json")
    args = parser.parse_args()

    with open(args.ville, 'r') as f:
        villeDic = load(f)

    dcprm = DCPRM(villeDic=villeDic)
    print(dcprm.getOccupancyGrids(3))
