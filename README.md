# Maze-solver
This project solves a maze using the A* algorithm. 

## Usage

1. **Prepare the Maze Image**:
   - Place the maze image in the same directory as the script and name it `maze.png`.
   - Ensure the maze has white paths and black walls for proper detection.
   - under the (crop the additional layers) crop the additional outer pixels beyond the walls.

2. **Customize Start and End Points** (Optional):
   - By default, the script automatically detects the entrance and exit of the maze.
   - To manually specify start and end points, uncomment the following lines in the script and set your desired coordinates:
     ```python
     START_TILE = (row, column)
     END_TILE = (row, column)
     ```

3. **Path Visualization**:
   - The solution is displayed as a green path. Press any key in the image window to close it.
   - If no solution is found, the program will display a message: "No path found."

