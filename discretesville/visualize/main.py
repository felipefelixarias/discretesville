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
    parser.add_argument('--alg', metavar='Search Algorithm', help='Name of the search algorithm you wish to use', default="SIPPAStar")
    parser.add_argument('--ville', metavar='Environment', help='Path to environment json',default="visualize/villes/sippville.json")
    parser.add_argument('--rows', metavar="Number of Rows", help = "Number of Rows for grid",default=0)
    parser.add_argument('--cols', metavar="Number of Columns", help = "Number of Columns for grid", default=0)

    args = parser.parse_args()
    app = QApplication([])

    if args.mode == "UX":
        numRows = int(args.rows)
        numCols = int(args.cols)
        window = MainWindow(numRows=numRows, numCols=numCols, searchAlg=args.alg)

    if args.mode == "load":
        with open(args.ville, 'r') as f:
            villeDic = load(f)
        window = MainWindow(villeDic=villeDic, searchAlg=args.alg)
    
    if args.mode == "save":
        pass
  
    app.exec_()