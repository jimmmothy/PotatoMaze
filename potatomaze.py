#!/usr/bin/python3

# Solve maze generated @ https://keesiemeijer.github.io/maze-generator/
#
# Dependencies- PIL, numpy
#
# to do-
# differant path finding algorithms
# arguments


import PIL
from PIL import Image
import numpy as np

######################################################
# Implements actual path finding algorithms
# Accepts numpy array of maze, returns solution path
######################################################
class pathFinder:

    def __init__(self, maze, height, width, entries):

        self.mazec = (255, 255, 255, 255)
        self.wallc = (0, 0, 0, 255)
        self.solc = (255, 0, 0, 255)

        self.mcd = 0
        self.wcd = 1
        self.scd = 3

        self.mazeData = maze
        self.entries = entries
        self.height = height
        self.width = width



    #################
    # Need to call the shortestPath recursively
    # this sets it up
    #################
    def doTheNeedfull(self):

        self.solution = []
        self.solution.append(self.entries[0])
        self.shortestPath(self.solution)
        return self.solution

    ##############
    # Is x,t a wall?
    ##############
    def isWall(self, x, y):

        if self.mazeData[x, y] != self.wcd:
                return False
        return True

    ######################
    # Actual path finding
    ######################
    def shortestPath(self, currentPath):

        # try to find path between self.entries[0] and self.entries[1]
        # call possibleMoves for head of currentPath
        # if no moves, end iteration/branch, if 1 move, look for exit/append and continue,
        # if more than 1 move, look for exit/then branch each possible path

        branchOrEnd = False
        while branchOrEnd == False:

            #print("\nNew loop\n")
            head = len(currentPath)-1
            possMoves = self.possibleMoves(currentPath[head])


            # remove existing head from possible moves
            if currentPath[head-1] in possMoves:
                possMoves.remove(currentPath[head-1])

            # check if exit is in possMoves
            if self.entries[1] in possMoves:
                print("Found exit")
                currentPath.append(possMoves[0])
                self.solution = currentPath
                branchOrEnd = True
                return True

            #print("cph: %s .. pm: %s" % (currentPath[head], possMoves))
            nPossMoves = len(possMoves)

            # dead end
            if nPossMoves == 0:
                branchOrEnd = True
                return False

            # multiple choices, branch
            elif nPossMoves > 1:
                #print("Found branch %s" % (possMoves))
                branchOrEnd = True

                for x in possMoves:
                    buffPath = currentPath.copy()
                    buffPath.append(x)
                    self.shortestPath(buffPath)

            # only 0 option
            elif nPossMoves == 1:
                currentPath.append(possMoves[0])

    def possibleMoves(self, cpos):

        newMoves = []
        x = cpos[0]
        y = cpos[1]

        # up
        if y > 0:
            if self.isWall(x, y-1) == False:
                newMoves.append([x, y-1])

        # down
        if y < self.height-1:
            if self.isWall(x, y+1) == False:
                newMoves.append([x, y+1])

        # left
        if x > 0:
            if self.isWall(x-1, y) == False:
                newMoves.append([x-1, y])

        # right
        if x < self.width-1:
            if self.isWall(x+1, y) == False:
                newMoves.append([x+1, y])

        return newMoves

##################################################
# Manages image import/export and data management
##################################################
class potatoMaze:

    ###################
    # Is this a wall?
    ###################
    def isWall(self, refpx):

        for x in range(0, 3):
            if refpx[x] != self.wallc[x]:
                return False
        return True

    ######################
    # Convert the RGBA file to a numpy array
    ######################
    def makeMaze(self):

        # reference for wall/maze in numpy array
        self.mcd = 0
        self.wcd = 1
        self.scd = 3

        # make array of 0s, then fill in walls w/ 1s
        self.mazeData = np.zeros((self.width, self.height))

        for y in range(0, self.height):
            for x in range(0, self.width):

                if self.isWall(self.px[x, y]):
                    self.mazeData[x, y] = self.wcd

        # search for entry points to maze
        self.entries = []

        for x in range(0, self.width):

            if self.isWall(self.px[x, 0]) == False:
                self.entries.append([x, 0])

            if self.isWall(self.px[x, self.height-1]) == False:
                self.entries.append([x, self.height-1])

        for y in range(0, self.height):

            if self.isWall(self.px[0, y]) == False:
                self.entries.append([0, y])

            if self.isWall(self.px[self.width-1, y]) == False:
                self.entries.append([self.width-1, y])

        print("Entries: %s" % self.entries)


    ######################
    # Update maze with solution path
    ######################
    def updateMazeWithSolution(self):

        for x in self.solution:
            self.mazeData[x[0], x[1]] = self.scd

    ########################
    # Create a new image with the solution included
    ########################
    def createSolutionImage(self, newName):

        # make a new PIl image based on solution
        solved = Image.new('RGB', (self.width, self.height), 'White')
        solvedpx = solved.load()

        for y in range(0, self.height):
            for x in range(0, self.width):

                z = self.mazeData[x, y]
                if z == self.wcd:
                    tmp = self.wallc
                elif z == self.mcd:
                    tmp = self.mazec
                elif z == self.scd:
                    tmp = self.solc

                solvedpx[x, y] = tmp

        solved.save(newName)
        print("Solution saved @ %s" % (newName))

    def __init__(self, imageLocation):

        # General assumptions
        self.width = 1
        self.border = False
        self.mazec = (255, 255, 255, 255)
        self.wallc = (0, 0, 0, 255)
        self.solc = (255, 0, 0, 255)

        # load image as RGBA
        self.imageLocation = imageLocation
        self.im = Image.open(imageLocation)
        if self.im.mode != 'RGBA':
            self.im = self.im.convert('RGBA')

        # load pixels
        self.px = self.im.load()

        # what do we know about image
        self.height = self.im.height
        self.width = self.im.width
        #print("Image %s loaded, H:%s W:%s" % (imageLocation, self.height, self.width))

        # generate maze data as an array
        self.makeMaze()
        self.solution = []

    ####################
    # Call a few functions to sort things out
    ####################
    def finalise(self):

        # update mazeData with solution path
        self.updateMazeWithSolution()

        # make solution into an image
        self.newName = self.imageLocation.split('.')[0] + "_solved." + self.imageLocation.split('.')[1]
        self.createSolutionImage(self.newName)



if __name__ == "__main__":

    maze = potatoMaze("maze200px.png")
    algo = pathFinder(maze.mazeData, maze.height, maze.width, maze.entries)
    maze.solution = algo.doTheNeedfull()
    maze.finalise()