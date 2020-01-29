from PyQt5.QtWidgets import QApplication

from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from visualize.cell import Cell
from visualize.mainwindow import MainWindow

from json import load
from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser(description="Select Mode, Search Algorithm, and Environment (depenging on mode)")
    parser.add_argument('--mode', metavar="Discretesville Mode", help="Mode for the UI", default="UX")
    parser.add_argument('--alg', metavar='Search Algorithm', help='Name of the search algorithm you wish to use', default="dynamicA*")
    parser.add_argument('--ville', metavar='Environment', help='Path to environment json',default="visualize/villes/testville.json")
    parser.add_argument('--rows', metavar="Number of Rows", help = "Number of Rows for grid",default=0)
    parser.add_argument('--cols', metavar="Number of Columns", help = "Number of Columns for grid", default=0)

    args = parser.parse_args()
    app = QApplication([])

    if args.mode == "UX" or args.mode == "save":
        numRows = int(args.rows)
        numCols = int(args.cols)
    else:
        numRows = 0
        numCols = 0

    if args.mode == "load" or args.mode == "research":
        with open(args.ville, 'r') as f:
            villeDic = load(f)
    else:
        villeDic = None

    window = MainWindow(numRows=numRows, numCols=numCols, villeDic=villeDic, mode=args.mode, searchAlg=args.alg, filename=args.ville)

    app.exec_()