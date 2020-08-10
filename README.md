# Pacman-AI-agent-for-stochastic-environment
A Markov Decision Process (MDP) based implementation of a Pacman agent, to survive and battle through a handicapped stochastic environment

> The code of the PACMAN AI agent implemented by myself is located in the MDPAgents.py file. The rest of the code (consisting of the actual implementation of the game, GUI, Ghost AI) was taken from the following link - http://ai.berkeley.edu/project_overview.html

### Instructions for running the project:
```
# run in small grid layout
python pacman.py -q -n 1 -p MDPAgent -l smallGrid 

# run in mediumClassic grid layout
python pacman.py -q -n 1 -p MDPAgent -l mediumClassic
```

### Handicap of PACMAN Agent
If Pacman chooses to move to a particular direction, it moves to the direction intended 80% of the time, however, in 20% of the time, it may move to a direction which is perpendicular to the original intended direction.

For instance, if PACMAN chooses to move UP, there is a 80% chance it will do so, however, a 10% chance it may move left, and 10% to the right (not originally intended).

### Description of the Markov Decision Process based PACMAN Agent
