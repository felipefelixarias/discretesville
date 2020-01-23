# discretesville

To use the GUI, run the main.py script in the visualize folder.

python visualize/main.py --help
usage: main.py [-h] [--mode Discretesville Mode] [--alg Search Algorithm]
               [--ville Environment] [--rows Number of Rows]
               [--cols Number of Columns]

Select Mode, Search Algorithm, and Environment (depenging on mode)

optional arguments:
  -h, --help            show this help message and exit
  --mode Discretesville Mode
                        Mode for the UI
  --alg Search Algorithm
                        Name of the search algorithm you wish to use
  --ville Environment   Path to environment json
  --rows Number of Rows
                        Number of Rows for grid
  --cols Number of Columns
                        Number of Columns for grid

Current modes implemented are: UX, load, and research.
Search algorithms supported are: dynamicA*, SIPPA*, A*, dijkstra, and critical.
Villes are saved as JSONs in the visualize/villes folder.
Rows and cols are used to determine size of the grid in UX mode.

In UX mode, first use left clicks to set static obstacles. Once done, use right clicks to define the start and end locations of the robot. Then, set dynamic obstacles by starting them with a right click and using left clicks to specify the full path. Every right click results in a new dynamic obstacle.

