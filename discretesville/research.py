from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from dcprm.dcprm import DCPRM


from json import load
from argparse import ArgumentParser
import os
from multiprocessing import Pool

if __name__ == '__main__':

    directory_in_str = '../scripts/envGeneration/jsons'
    directory = os.fsencode(directory_in_str)
    fileList = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        fileList.append(filename)

    p = Pool(22)
    p.map(DCPRM, fileList)