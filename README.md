# Pacman-AI-agent-for-stochastic-environment
A Markov Decision Process (MDP) based implementation of a Pacman agent, to survive and battle through a handicapped stochastic environment

> The code of the PACMAN AI agent implemented by myself is located in the MDPAgents.py file. The rest of the code (consisting of the actual implementation of the game, GUI, Ghost AI) was taken from the following link - http://ai.berkeley.edu/project_overview.html

Evaluation of the AI Agent is discussed further down the line in the readme.

### Instructions for running the project:
```
python pacman.py -q -n 1 -p MDPAgent -l <grid name>

# example
python pacman.py -q -n 1 -p MDPAgent -l mediumClassic
```

### Handicap of PACMAN Agent
If Pacman chooses to move to a particular direction, it moves to the direction intended 80% of the time, however, in 20% of the time, it may move to a direction which is perpendicular to the original intended direction.

For instance, if PACMAN chooses to move UP, there is a 80% chance it will do so, however, a 10% chance it may move left, and 10% to the right (not originally intended).

### Description of the Markov Decision Process based PACMAN Agent
#### Defining reward of each coordinate in a given state of the game 
The instance variables of the ‘MDPAgent’ class contains all the parameters of the MDP solver. This includes reward values of the ghost/food/capsule states or coordinates in the game board. 

I have modelled the states around the ghost as ‘danger zones’, as its risky for PACMAN to be in those areas. The coordinates of those areas have a negative reward, however, This negative reward is larger than the reward of the actual coordinate the ghost is in, because the exact ghost position is worse than the coordinates around it, but nevertheless, the reward value of both the danger zone and the actual position of the ghost is negative (to represent that being in one of those state is undesireable). The computation of danger zones around the ghost also depends on walls around the ghost, to account for circumstances in which the agent does not have to fear ghosts because of walls in between.

The reward value of each coordinate is updated on each time step of the game, so the AI agent is up to date with the current state of the game.

#### Value Iteration Algorithm
The [Value Iteration](https://artint.info/html/ArtInt_227.html#:~:text=Value%20iteration%20is%20a%20method,MDP%20policy%20and%20its%20value.&text=%3D%20maxa%20Qk(s,a)%20for%20k>0.&text=Saving%20the%20V%20array%20results,results%20in%20the%20greatest%20value.) algorithm is used in each time step of the game to calculate the max expected utility of all possible action. This is implemented in the function named 'bellman' in the class. It uses the bellman equation to calculate utility of each possible action from a given state, by taking into account non‐determinism of the game and outputs the actions which yields maximum expected utility along with its value. Once this is computed, the action with the max value is chosen.

## Evaluation of the AI Agent
