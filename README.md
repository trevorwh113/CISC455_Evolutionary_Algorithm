# CISC455_Evolutionary_Algorithm
Group 2 - Evolutionary Ops
Claire Whelan, Nicole Hernandez, Trevor White, Emma Leitch-Blais, Maria Kobilaski

## Description
This EA is designed to evolve trash can placement for a generated 2D city map. Fitness of solutions are calculated by assigning a score to each coordinate on the map, this score indicates how far that coordinate is from a trash can. The lower the fitness score of a solution, the more optimal. Each additional trashcan placed negatively impacts the fitness. 

## Purpose
The purpose of this algorithm is to minimize the walking distance from a trash can to any point on the map while minimizing the amount of trash cans used. 

### Input Map
The generated starting map uses the following values to designate obstacles:
- `0`: free space
- `-1`: road
- `-2`: building

### Dependencies
- python3
- NumPy
- pytest for mutation testing

### Executing Program
```
python3 main.py
```

## Options for Input Maps
- **Default:** automatically generates map using generate_map()
- **Loading from CSV file:** uncomment out option and specify file location
```
map = load_map_from_csv("map_test_easy.csv", "./saved_maps")
N, M = map.shape
```

## Configuration Values
- `N` - number of rows/columns in the map
- `gen_limit` - number of generations before termination condition is reached
- `ideal_steps_from_trashcan` - the ideal number of steps from a trash can to any given coordinate on the map
- **Fitness penalties:**
    - `nonePenalty`
    - `canOverPenalty`
    - `overStepPenalty`

## Output
Every 10 generations, the best solution is printed to the console. The final solution is also printed to the console at the end of the run. The HTML output is by default saved in the `saved_maps` folder.

