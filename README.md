# 2048-RL (Q-Learning and Approximate Q-Learning)

## Overview
Q-Learning is a model-free reinforcement learning algorithm that generates an optimal policy using a 
Markov decision process (MDP). The generated policy decides what action to take at a given game state by trying to maximize
the total reward over successive steps in the game.

Approximate Q-Learning uses a feature-based representation of the states instead of storing the Q-value for every game state 
the agent encounters. These Q-values are computed on demand, significantly reducing memory usage and time to train.

## Setup

### Prerequisites
* Python 3.5+
* numpy

### Training
*Trains until manually interrupted*

For Q-Learning: `python3 qlearning.py`

For Approximate Q-Learning: `python3 approxqlearning.py`

## Results
*Recorded the mean max-tile achieved for every 20 games played*

#### Q-Learning
* 1 minute of training
  * Average Max Tile: 115.2
  * Reached 2048: 0
* 1 hour of training
  * Average Max Tile: 137.8
  * Reached 2048: 0
* 1 day of training
  * Insufficient storage and computing power

#### Approximate Q-Learning
* 1 minute of training
  * Average Max Tile: 537.0
  * Reached 2048: 0
* 1 hour of training 
  * Average Max Tile: 602.8
  * Reached 2048: 0
* 1 day of training
  * Average Max Tile: 697.3
  * Reached 2048: 1

## Team
| **William Wang**</a> | **Albert Zhang**</a> | **Colton Nishida**</a> |
| :---: | :---: | :---: |
| [![William Wang](https://avatars1.githubusercontent.com/u/46856940?v=4&s=200)](https://github.com/williamwang0)  | [![Albert Zhang](https://avatars0.githubusercontent.com/u/31051641?v=4&s=200)](https://github.com/albertczhang) | [![Colton Nishida](https://avatars2.githubusercontent.com/u/46944125?v=4&s=200)](https://github.com/coltonnishida) |
| <a href="https://github.com/williamwang0" target="_blank">`github.com/williamwang0`</a> | <a href="https://github.com/albertczhang" target="_blank">`github.com/albertczhang`</a> | <a href="https://github.com/coltonnishida" target="_blank">`github.com/coltonnishida`</a> |
