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
For Q-Learning: `python3 qlearning.py`

For Approximate Q-Learning: `python3 approxqlearning.py`

## Results
*Recorded the mean max-tile achieved for every 20 games played*

#### Q-Learning
* 1 minute of training: ~115
* 1 hour of training: ~130
* 1 day of training: 

#### Approximate Q-Learning
* 1 minute of training: ~530
* 1 hour of training: ~600
* 1 day of training: 

## Acknowledgments
* Albert Zhang (@albertczhang)
* Colton Nishida (@coltonnishida)
