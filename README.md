# Pacman-AI-agent-for-stochastic-environment
A Markov Decision Process (MDP) based implementation of a Pacman agent, to survive and battle through a handicapped stochastic environment

### Instructions for running the project:
```
python pacman.py -q -n 1 -p MDPAgent -l <grid name>

# example
python pacman.py -q -n 1 -p MDPAgent -l mediumClassic
```

### Handicap on AI
If AI chooses to move to a particular direction:
* It moves to the direction intended 80% of the time
* However, in 20% of the time, it may move to a direction which is perpendicular to the original intended direction.

For instance, if PACMAN chooses to move UP, there is a 80% chance it will do so, however, a 10% chance it may move left, and 10% to the right (not originally intended).

### AI decision process: Value Iteration Algorithm
The [Value Iteration](https://artint.info/html/ArtInt_227.html#:~:text=Value%20iteration%20is%20a%20method,MDP%20policy%20and%20its%20value.&text=%3D%20maxa%20Qk(s,a)%20for%20k>0.&text=Saving%20the%20V%20array%20results,results%20in%20the%20greatest%20value.) algorithm is used in each time step of the game to calculate the max expected utility of all possible action.It uses the bellman equation to calculate utility of each possible action from a given state, by taking into account non‐determinism of the game and outputs the actions which yields maximum expected utility along with its value. Once this is computed, the action with the max value is chosen.

## Evaluation of the AI Agent
> Tests were done on intel core i7‐1770 3.6 GHz

### Discount factor

Discount factor represents to what degree of importance the AI places on the future for each decision it makes

 ![Evaluating different values of discount factor](https://github.com/Naharul98/Pacman-AI-agent-for-stochastic-environment/blob/master/Discount_Factor_Evaluation_Chart.jpg?raw=true)
 

### Reward values
Blank states represents blank cells within the board (have neither of the following: capsule, food, ghost, wall, ghost). Assigning a very small negative reward to such a state may incentivize the Pacman agent to pursue its goal quicker and discourage it from lingering around blank cells which do not have any reward.

The chart below demonstrates different reward values of blank states,tested against win percentages.
 ![Evaluating different reward values of blank state](https://github.com/Naharul98/Pacman-AI-agent-for-stochastic-environment/blob/master/BlankState_Reward_Evaluation_Chart.jpg?raw=true)


### Number of iterations in the Algorithm 
![Evaluating impact of number of iteration](https://github.com/Naharul98/Pacman-AI-agent-for-stochastic-environment/blob/master/Iteration_Evaluation_Chart.jpg?raw=true)
It can be noticed that iterations as small as 100 is good enough for small grid, however for larger layouts such as ‘mediumClassic’, it can be noticed that there is a lot to gain from a higher number of iterations, as increasing iterations from 1000 to 2000 results in dramatic increase of about 15% win.

However, there is a trade‐off with the time required to complete the game. I have chosen to go with 500 iterations for tests, as the percentage increase of winnings from 500 to 1000 isn’t quite significant as observed from the data, however if the time for marking was unlimited, the performance of the MDP solver dramatically rises.
 


