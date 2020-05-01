# Agent-Maze-Solver

A project developed by WPS Lakerbotics Programming to further practice our understanding of
2d arrays, and manipulating agents.

Required python libraries:
  * Numpy
  * Pygame

HOW TO USE:
1. Creating a map
   - Run ```builder.py```
   - When finished, press the "enter" key to save map to 'map.pkl'
2. Running the map
   - Run ```environment.py```
   - Instructions within ```environment.py``` on how to implement agent code.
   - See the agent do its work
   
Optional
   - Environment by default loads from map.pkl, but it can be reconfigured to load just the grid
   from map.txt (non-existant by default)
   - To enable direct user input, go to ```settings.py``` and set DEV_MODE to True.
