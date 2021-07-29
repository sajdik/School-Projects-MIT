# FLP(2021) logical project - Rubik's Cube
## Author: 
Ondrej Sajdik (xsajdi01)

## Build:
make

## Run:
./flp20-log < test/input2.txt

## Implementation:
Program is using IDS (iterative deepening search) to find solution. Starting with depth limit 1 for optimal results. As actions are implemented 6 operations, which rotate one face of cube. Algorithm has exponential time complexity so inputs that take more then 6 moves to solve takes a long time.

## Input files:
in folder test/ are example input files. 
Number in their names says how many moves are needed to solve. Execution times are:
moves 0-5 finish in <1 second
6 finishes in ETA 15 secs
