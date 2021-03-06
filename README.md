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

### Handicap Inflicted on the AI Agent to make its task more difficult
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
> Tests were done on intel core i7‐1770 3.6 GHz

### Evaluating different values of discount factor
 ![Evaluating different values of discount factor](https://github.com/Naharul98/Pacman-AI-agent-for-stochastic-environment/blob/master/Discount_Factor_Evaluation_Chart.jpg?raw=true)
 
The chart above shows the evaluation results. As it can be observed for discount factors, a value of 0 in discount factor always yielded no wins at all. In addition, it can also be observed that there is a correlation of high discount factor value with higher number of wins in both layouts. However, in mediumClassic layout, discount factor of 0.8 yielded below expected result in the first experiment, however, I concluded it was because of the non‐determinism (Handicap) aspect of the agent after doing the
experiment twice again for that discount value, in similar condition.

### Evaluating different reward values of blank state
Blank states in the game are states/coordinates which have/are neither of the following: capsule, food, ghost, wall, ghost, danger location. Assigning a very small negative reward to such a state may incentivize the Pacman agent to pursue its goal quicker and discourage it from lingering around blank state which do not have any reward.

The chart below demonstrates different reward values of blank states,tested against win percentages.
 ![Evaluating different reward values of blank state](https://github.com/Naharul98/Pacman-AI-agent-for-stochastic-environment/blob/master/BlankState_Reward_Evaluation_Chart.jpg?raw=true)
 
From the data above, it can be concluded that generally having a value closer to 0 corresponds with higher win percentage. During the experiment, it was observed that if the negative reward is very high and if there is lots of blank states nearby, Pacman often commits suicide by charging to ghosts himself.

The data suggests that having a slight negative reward for non‐terminal state yields favourable result for
‘smallGrid’, however, it is offset by the results for ‘mediumClassic’ layout, hence I have chosen a value of 0 for the
reward of non‐terminal states

### Evaluating if number of iterations in the algorithm has any notable effect on win percentage
![Evaluating impact of number of iteration](https://github.com/Naharul98/Pacman-AI-agent-for-stochastic-environment/blob/master/Iteration_Evaluation_Chart.jpg?raw=true)
It is evident from the graph that a higher number of iterations yield better result and this is in alignment with the theory. It can be noticed that iterations as small as 100 is good enough for small grid, however for larger layouts such as ‘mediumClassic’, it can be noticed that there is a lot to gain from a higher number of iterations, as increasing iterations from 1000 to 2000 results in dramatic increase of about 15% win.

However, there is a trade‐off with the time required to complete the game. I have chosen to go with 500 iterations for further tests, as the percentage increase of winnings from 500 to 1000 isn’t quite significant as observed from the data, however if the time for marking was unlimited, the performance of the MDP solver dramatically rises.
 
### Experimenting with reward values of danger zone around ghost
I have experimented setting the parameter for the reward of danger location the same as the reward of the actual location of the ghost. Upon first thought, I had the expectation that this would make the Pacman play safer, however, this didn’t necessarily yield better results, as I observed situations when it made sense for Pacman to move to a particular direction to grab food/capsule, however it didn’t. It did play safer, however, playing too much safe, coupled with non‐determinism (stochastic handicap) aspect of the game, failed to yield better results.

