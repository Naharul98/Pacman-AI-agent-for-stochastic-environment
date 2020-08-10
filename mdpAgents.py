# The agent here is was written by A K M Naharul Hayat, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
import itertools
import time

class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        self.foodReward = 0.3  # reward of coordinates which have food
        self.capsuleReward = 0.5  # reward of coordinates which have capsule
        self.blankStateReward = 0  # reward of coordinates which are blank
        self.ghostsReward = -3  # reward of coordinates which have ghost in them
        self.wallReward = 'W'  # 'W' marks coordinates which are walls
        # Reward of locations which aren't ghost but within danger zone perimeter of ghost
        self.dangerLocationReward = -2
        # the following dictionary has key as coordinates and values as their utility
        self.rewardDictionary = dict()
        self.width = 0  # width of the board
        self.height = 0  # height of the board
        # the following set contains danger locations around/including ghosts at 1 step before
        # danger zones are considered as no-go zones
        self.previousGhostLocation = set()
        self.foodLocations = list()  # coordinates which have food at current time
        self.capsuleLocations = list()  # coordinates which have capsules at current time
        self.blankStates = set()  # coordinates which are blank at current time
        # probability that we go to the direction we want. example - if we go up, we actually go up
        self.probabilityRightDirection = 0.8
        # probability that we go to the direction we don't want want. example - if we go up, we actually go left
        self.probabilityWrongDirection = 0.1


    # this function returns list of tuples containing coordinates
    # which are classified as danger zones around and including ghost position
    # at a given time
    # parameters: point = ghost location. utilMap = map containing utility
    def getGhostPerimeter(self, point, utilMap, width, height):
        dangerCoordinates = set()
        bigLayout = (width >=7 or height >=7)  # layout is classified as big if either of its dimension >8
        # the ghost location is converted to tuple of int
        coordinate = (int(point[0]), int(point[1]))
        # the ghost location is added to danger zone
        dangerCoordinates.add(coordinate)
        # if ghost can go up, then its classified as danger zone as well
        if ('W' != utilMap[(coordinate[0], coordinate[1] + 1)]):
            dangerCoordinates.add((coordinate[0], coordinate[1] + 1))
            # if board size not too much, disregard danger zone perimeter calculation
            try:
                # if ghost can go up,its right is added to danger zone as well if its valid and not a wall
                if ('W' != utilMap[(coordinate[0] + 1, coordinate[1] + 1)]):
                    dangerCoordinates.add((coordinate[0] + 1, coordinate[1] + 1))
            except:
                pass
            try:
                # if ghost can go up,its left is added to danger zone as well if its valid and not a wall
                if ('W' != utilMap[(coordinate[0] - 1, coordinate[1] + 1)]):
                    dangerCoordinates.add((coordinate[0] - 1, coordinate[1] + 1))
            except:
                pass
            try:
                # if ghost can go up,its double right is added to danger zone as well if its valid and not a wall
                # only calculated if layout is bit
                if ('W' != utilMap[(coordinate[0] + 2, coordinate[1] + 1)] and bigLayout):
                    dangerCoordinates.add((coordinate[0] + 2, coordinate[1] + 1))

            except:
                pass
            try:
                # if ghost can go up,its double left is added to danger zone as well if its valid and not a wall
                # only calculated if layout is bit
                if ('W' != utilMap[(coordinate[0] - 2, coordinate[1] + 1)] and bigLayout):
                    dangerCoordinates.add((coordinate[0] - 2, coordinate[1] + 1))
            except:
                pass
            try:
                # if a valid coordinate & not a wall, then ghosts's 2 step up is added to danger zone as well
                # only calculated if layout is bit
                if ('W' != utilMap[(coordinate[0], coordinate[1] + 2)] and bigLayout):
                    dangerCoordinates.add((coordinate[0], coordinate[1] + 2))
                    try:
                        # if ghost can go two step up, then its right is added to danger location
                        if ('W' != utilMap[(coordinate[0] + 1, coordinate[1] + 2)]):
                            dangerCoordinates.add((coordinate[0] + 1, coordinate[1] + 2))
                    except:
                        pass
                    try:
                        # if ghost can go two step up, then its left is added to danger location
                        if ('W' != utilMap[(coordinate[0] - 1, coordinate[1] + 2)]):
                            dangerCoordinates.add((coordinate[0] - 1, coordinate[1] + 2))
                    except:
                        pass
            except:
                pass

        # if ghost can go down, then its classified as danger zone as well
        if ('W' != utilMap[(coordinate[0], coordinate[1] - 1)]):
            dangerCoordinates.add((coordinate[0], coordinate[1] - 1))
            try:
                # if ghost can go down, then its right is classified as danger zone, if its a valid position & not a wall
                if ('W' != utilMap[(coordinate[0] + 1, coordinate[1] - 1)]):
                    dangerCoordinates.add((coordinate[0] + 1, coordinate[1] - 1))
            except:
                pass
            try:
                # if ghost can go down, then its double right is classified as danger zone, if its a valid position & not a wall
                # only calculated if layout is bit
                if ('W' != utilMap[(coordinate[0] + 2, coordinate[1] - 1)] and bigLayout):
                    dangerCoordinates.add((coordinate[0] + 2, coordinate[1] - 1))
            except:
                pass
            try:
                # if ghost can go down, then its double left is classified as danger zone, if its a valid position & not a wall
                # only calculated if layout is bit
                if ('W' != utilMap[(coordinate[0] - 2, coordinate[1] - 1)] and bigLayout):
                    dangerCoordinates.add((coordinate[0] - 2, coordinate[1] - 1))
            except:
                pass
            try:
                # if ghost can go down, then its left is classified as danger zone, if its a valid position & not a wall
                if ('W' != utilMap[(coordinate[0] - 1, coordinate[1] - 1)]):
                    dangerCoordinates.add((coordinate[0] - 1, coordinate[1] - 1))
            except:
                pass
            try:
                # if ghost can go down, then 2 steps down from current position is
                # considered as danger zone if its valid and not a wall
                # only calculated if layout is bit
                if ('W' != utilMap[(coordinate[0], coordinate[1] - 2)] and bigLayout):
                    dangerCoordinates.add((coordinate[0], coordinate[1] - 2))
                    try:
                        # if ghost can go two step down, then its right is added to danger location if its valid
                        if ('W' != utilMap[(coordinate[0] + 1, coordinate[1] - 2)]):
                                dangerCoordinates.add((coordinate[0] + 1, coordinate[1] - 2))
                    except:
                        pass
                    try:
                        # if ghost can go two step down, then its left is added to danger location if its valid
                        if ('W' != utilMap[(coordinate[0] - 1, coordinate[1] - 2)]):
                                dangerCoordinates.add((coordinate[0] - 1, coordinate[1] - 2))
                    except:
                        pass
            except:
                pass

        # if ghost can go right, then its considered as danger zone if its not a wall
        if ('W' != utilMap[(coordinate[0] + 1, coordinate[1])]):
            dangerCoordinates.add((coordinate[0] + 1, coordinate[1]))
            try:
                 # 2 steps right of ghost considered a danger zone if its valid + not a wall + it can go right in first place
                if ('W' != utilMap[(coordinate[0] + 2, coordinate[1])]):
                    dangerCoordinates.add((coordinate[0] + 2, coordinate[1]))
            except:
                pass
            try:
                # 1 step right and one step above considered a danger zone if its not a wall
                if ('W' != utilMap[(coordinate[0] + 1, coordinate[1] +1)]):
                    dangerCoordinates.add((coordinate[0] + 1, coordinate[1] +1))
            except:
                pass
            try:
                # 1 step right and one step down considered a danger zone if its not a wall
                if ('W' != utilMap[(coordinate[0] + 1, coordinate[1] -1)]):
                    dangerCoordinates.add((coordinate[0] + 1, coordinate[1] -1))
            except:
                pass
        # if ghost can go left, then its considered as danger zone if its not a wall
        if ('W' != utilMap[(coordinate[0] - 1, coordinate[1])]):
            dangerCoordinates.add((coordinate[0] - 1, coordinate[1]))
            try:
            # 2 steps left of ghost considered a danger zone if its valid + not a wall + it can go left in first place
                if ('W' != utilMap[(coordinate[0] - 2, coordinate[1])]):
                    dangerCoordinates.add((coordinate[0] - 2, coordinate[1]))
            except:
                pass

            try:
                # 1 step left and one step up considered a danger zone if its not a wall
                if ('W' != utilMap[(coordinate[0] - 1, coordinate[1] +1)]):
                    dangerCoordinates.add((coordinate[0] - 1, coordinate[1] +1))
            except:
                pass
            try:
                # 1 step right and one step down considered a danger zone if its not a wall
                if ('W' != utilMap[(coordinate[0] - 1, coordinate[1] -1)]):
                    dangerCoordinates.add((coordinate[0] - 1, coordinate[1] -1))
            except:
                pass

        # returns compiled list of coordinates considered as danger zones
        return dangerCoordinates

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    # parameter = state
    def registerInitialState(self, state):
        # gets width and height of layout
        self.width = sorted(api.corners(state), key=lambda tup: tup[0], reverse=True)[0][0]
        self.height = sorted(api.corners(state), key=lambda tup: tup[1], reverse=True)[0][1]

    ############################### CONSTRUCTING THE MAP ##############################################
        # populates food location initially
        self.foodLocations = api.food(state)
        self.capsuleLocations = api.capsules(state)
        # does an initial iteration of the entire layout and populates reward/utility map/dictionary
        for i in range(self.width + 1):
            for j in range(self.height+1):
                # populates food coordinates in map according to reward
                if((i,j) in api.food(state)):
                    self.rewardDictionary[(i,j)] = self.foodReward
                # populates wall coordinates in map
                elif((i,j) in api.walls(state)):
                    self.rewardDictionary[(i, j)] = self.wallReward
                # populates capsule coordinates in map
                elif((i,j) in api.capsules(state)):
                    self.rewardDictionary[(i, j)] = self.capsuleReward
                # all others assigned as blank initially and added to blankState list
                else:
                    self.rewardDictionary[(i, j)] = self.blankStateReward
                    self.blankStates.add((i, j))
        ################### RECORDING PREVIOUS GHOST LOCATIONS ##############################
        # for each ghost's current position
        for f in api.ghosts(state):
            # get the danger zones of that ghost
            dangerZones = self.getGhostPerimeter(f, self.rewardDictionary, self.width,self.height)
            # add it to previous ghost locations as danger zone.
            # Note - considered as no-go zones similar to ghost
            self.previousGhostLocation = self.previousGhostLocation.union(dangerZones)
        #################### POPULATING NO_GO COORDINATES IN THE MAP #########################
        for tup in self.previousGhostLocation:
            self.rewardDictionary[(int(tup[0]), int(tup[1]))] = self.ghostsReward
            if ((int(tup[0]), int(tup[1])) in self.blankStates):
                self.blankStates.remove((int(tup[0]), int(tup[1])))
        
    # This is what gets run in between multiple games
    # This function resets all variables used during the game
    # To do a fresh restart in the next game
    def final(self, state):
        print "Looks like the game just ended!"
        self.rewardDictionary = dict()
        self.width = 0
        self.height = 0
        self.previousGhostLocation = set()
        self.foodLocations = list()
        self.capsuleLocations = list()
        self.blankStates = set()

    # this function takes the a coordinate and the map and outputs a dictionary
    # which says if the position above/below/right/left of the coordinate is a wall
    # parameter - utilmap = the utility map, coordinate = tuple containing coordinate for query
    def constructWallDictionaryBasedOnCoordinates(self, utilMap, coordinate):
        wallDict = dict()

        wallDict['up'] = True if ('W' == utilMap[(coordinate[0],coordinate[1]+1)]) else False
        wallDict['down'] = True if ('W' == utilMap[(coordinate[0], coordinate[1]-1)]) else False
        wallDict['east'] = True if ('W' == utilMap[(coordinate[0]+1, coordinate[1])]) else False
        wallDict['west'] = True if ('W' == utilMap[(coordinate[0]-1, coordinate[1])]) else False
        return wallDict

    # this function takes the a coordinate and returns, the action out of all possible action from that state
    # which yields the max utility from the given coordinate. This is a helper function for the bellman equation
    # it returns a tuple of the action name and its expected utility
    # parameter - utilmap = the utility map, coordinate = tuple containing coordinate for query
    def bellman(self,utilMap,coordinate):
        # gets wall map of the coordinate to judge whether we can actually go in the direction because of walls
        wallDict = self.constructWallDictionaryBasedOnCoordinates(utilMap, coordinate)
        # probability that we go to the direction we want. example - if we go up, we actually go up
        prollyRightDirection = self.probabilityRightDirection
        # probability that we go to the direction we dont want want. example - if we go up, we actually go left
        prollyWrongDirection = self.probabilityWrongDirection

        ############# COMPUTE EXPECTED UTILITY OF GOING UP #######################
        forUp = 0
        forUp = (forUp + (prollyRightDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['up'] == True) else (forUp + (prollyRightDirection*utilMap[(coordinate[0],coordinate[1] +1)]))
        forUp = (forUp + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['east'] == True) else (forUp + (prollyWrongDirection*utilMap[(coordinate[0]+1, coordinate[1])]))
        forUp = (forUp + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['west'] == True) else (forUp + (prollyWrongDirection*utilMap[(coordinate[0]-1, coordinate[1])]))

        ############# COMPUTE EXPECTED UTILITY OF GOING DOWN #######################
        forDown = 0
        forDown = (forDown + (prollyRightDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['down'] == True) else (forDown + (prollyRightDirection*utilMap[(coordinate[0], coordinate[1]- 1)]))
        forDown = (forDown + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['east'] == True) else (forDown + (prollyWrongDirection*utilMap[(coordinate[0]+1, coordinate[1])]))
        forDown = (forDown + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['west'] == True) else (forDown + (prollyWrongDirection*utilMap[(coordinate[0]-1, coordinate[1])]))

        ############# COMPUTE EXPECTED UTILITY OF GOING EAST #######################
        forEast = 0
        forEast = (forEast + (prollyRightDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['east'] == True) else (forEast + (prollyRightDirection*utilMap[(coordinate[0]+1, coordinate[1])]))
        forEast = (forEast + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['up'] == True) else (forEast + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1] +1)]))
        forEast = (forEast + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['down'] == True) else (forEast + (prollyWrongDirection*utilMap[(coordinate[0], coordinate[1]- 1)]))

        ############# COMPUTE EXPECTED UTILITY OF GOING WEST #######################
        forWest = 0
        forWest = (forWest + (prollyRightDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['west'] == True) else (forWest + (prollyRightDirection*utilMap[(coordinate[0] -1, coordinate[1])]))
        forWest = (forWest + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['up'] == True) else (forWest + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1] +1)]))
        forWest = (forWest + (prollyWrongDirection*utilMap[(coordinate[0],coordinate[1])])) if (wallDict['down'] == True) else (forWest + (prollyWrongDirection*utilMap[(coordinate[0], coordinate[1]- 1)]))

        # Form a dictionary withe key as action and value as the value computed for that action
        toReturn = {(Directions.NORTH):forUp, (Directions.SOUTH):forDown, (Directions.EAST): forEast, (Directions.WEST): forWest}
        # returns tuple of the action name which yields the max expected utility + the value for that action
        return max(toReturn.items(), key=lambda k: k[1])

    # this function is called in each step of the game and has to invoke the action that
    # PACMAN chooses to take
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        # Because we dont want PACMAN to sit idle
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        currentLocation = api.whereAmI(state)  # Current PACMAN location

        # if pacman is currently in a state which has food i.e He has eaten it
        # then update it in map as blank. Remove it from foodlocations and
        # add to blank state list
        if(currentLocation in self.foodLocations):
            self.rewardDictionary[(currentLocation[0], currentLocation[1])] = self.blankStateReward
            self.foodLocations.remove(currentLocation)
            self.blankStates.add(currentLocation)
        # if pacman is currently in a state which has capsule i.e He has eaten it
        # then update it in map as blank. Remove it from capsulelocation and
        # add to blank state list
        elif(currentLocation in self.capsuleLocations):
            self.rewardDictionary[(currentLocation[0], currentLocation[1])] =  self.blankStateReward
            self.capsuleLocations.remove(currentLocation)
            self.blankStates.add(currentLocation)

        # since danger zone has changed from previously
        # amend previous danger zone in map
        # to food/capsule/blank in map accordingly
        # if state is blank, then add to blank state record list
        for t in self.previousGhostLocation:
            # if previous danger location is food, amend coordinate in utility map to food
            if(t in api.food(state)):
                self.rewardDictionary[(int(t[0]), int(t[1]))] = self.foodReward
            # if previous danger location is capsule, amend coordinate in utility map to capsule
            elif(t in api.capsules(state)):
                self.rewardDictionary[(int(t[0]), int(t[1]))] = self.capsuleReward
            # if previous danger location is none of the above, set it as blank state in map
            else:
                self.rewardDictionary[(t[0], t[1])] = self.blankStateReward
                self.blankStates.add((int(t[0]), int(t[1])))

        ################## UPDATE NEW GHOST/DANGER ZONE IN MAP #############################
        # the following dictionary contains ghost location as key and value as timer
        # until its edible state ends
        edibleTimerDictionary = dict(api.ghostStatesWithTimes(state))

        # reset previous danger location list
        # note - danger locations are considered ghost location as well for safety
        self.previousGhostLocation = set()

        # for each ghost location
        for tup in api.ghosts(state):
            # get its danger locations
            dangerLocations = self.getGhostPerimeter(tup, self.rewardDictionary, self.width,self.height)
            # add danger location to previous danger location list
            # note - danger locations are considered ghost location as well for safety
            self.previousGhostLocation = self.previousGhostLocation.union(dangerLocations)

            # if ghost is edible and has only more than 4 steps left until it becomes terrifying again
            if(edibleTimerDictionary[tup] >=4):
                # do nothing
                pass
            else:
                # ghost is in eat mode or has only 4 second until it gets to eat mode

                # update danger locations in utility map to negative reward.
                for t in dangerLocations:
                    if(t == tup):
                        # if location exactly as ghost location update utility accordingly
                        self.rewardDictionary[(int(t[0]), int(t[1]))] = self.ghostsReward
                    else:
                        # if location within ghost danger zone perimeter, update utility accordingly
                        self.rewardDictionary[(int(t[0]), int(t[1]))] = self.dangerLocationReward
                    # remove danger location from blank state
                    if (t in self.blankStates):
                        self.blankStates.remove((int(t[0]), int(t[1])))

    ######################### VALUE ITERATION #####################################

        discountFactor = 0.95  # discount factor
        rewardOfBlankState = 0  # reward of states which is neither food/capsule/danger/wall

        for i in range(200):
            # copy utility map
            Ucopy = dict(self.rewardDictionary)
            # apply value iteration for states which are blanks - i.e - no walls, danger location, food, capsule
            for tup in self.blankStates:
                self.rewardDictionary[(tup[0],tup[1])] = rewardOfBlankState + (discountFactor * self.bellman(Ucopy,(tup[0],tup[1]))[1])

    ########################### RETRIEVING POLICY FOR CURRENT PACMAN LOCATION ######################################
        # use current PACMAN location to get
        expectedUtilityMap = self.bellman(self.rewardDictionary, api.whereAmI(state))

    ############################ INVOKE MOVE BASED ON POLICY RETRIEVED ###################################
        # uncomment the following to print the policy action for current step in the game
        # print(expectedUtilityMap[0])
        # invokes the move based on retrieved policy
        return api.makeMove(expectedUtilityMap[0], legal)