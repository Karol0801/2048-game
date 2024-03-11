# 2048 game
#### _Project in progress_

### Introduction
The main goal of the project is to develop an algorithm using reinforcement machine learning that efficiently plays the 2048 game.

Two approaches will be compared:
- alpha beta pruning
- expectimax 

which are described a little further.
The project also includes the implementation of the game itself, in which there is a move hint system. it will be based on the most effective version of the created algorithm.

The app allows gameplay in two modes:
- one player mode - _standard 2048 gameplay_
- two player mode - _the second player determines where the next tile appears_

<div style="text-align:center">
  <img src="README_files/gameplay.png" style="display:block; margin: 0 auto;">
</div>

Currently, the hint system is based on an alpha-beta pruning algorithm with manually selected parameters - the effectiveness of this algorithm is low, but it provides some starting point.
### Some key information about used algorithms
