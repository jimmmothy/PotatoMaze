#!/usr/bin/python3

# Solve maze generated @ https://keesiemeijer.github.io/maze-generator/
#
# Dependencies- PIL, numpy

import PIL
from PIL import Image
import numpy as np

class potatoMaze:

    def isWall(self, refpx):

        # use x,y .. everything else here uses y,x because PIL
        for x in range(0, 3):
            if refpx[x] != self.wallc[x]:
                return False
        return True

    def makeMaze(self):

        # reference for wall/maze in numpy array
        self.mcd = 0
        self.wcd = 1
        self.scd = 3

        # make array of 0s, then fill in walls w/ 1s
        self.mazeData = np.zeros((self.height, self.width))

        for y in range(0, self.height):
            for x in range(0, self.width):

                if self.isWall(self.px[x, y]):
                    self.mazeData[y, x] = self.wcd

        # search for entry points to maze
        entriesLimit = 2
        self.entries = []
        for x in range(0, self.width):

            if self.isWall(self.px[0, x]) == False:
                self.entries.append([x, 0])

            if self.isWall(self.px[self.height-1, x]) == False:
                self.entries.append([x, self.height-1])

        for y in range(0, self.height):

            if self.isWall(self.px[y, 0]) == False:
                self.entries.append([0, y])

            if self.isWall(self.px[y, self.width-1]) == False:
                self.entries.append([self.width-1, y])

        #print("Entries: %s\n" % self.entries)
        #print(self.mazeData)

    def possibleMoves(self, cpos):

        newMoves = []
        x = cpos[1]
        y = cpos[0]

        # up
        if y > 0:
            if self.isWall(self.px[x, y-1]) == False:
                newMoves.append([y-1, x])

        # down
        if y < self.height-1:
            if self.isWall(self.px[x, y+1]) == False:
                newMoves.append([y+1, x])

        # left
        if x > 0:
            if self.isWall(self.px[x-1, y]) == False:
                newMoves.append([y, x-1])

        # right
        if x < self.width-1:
            if self.isWall(self.px[x+1, y]) == False:
                newMoves.append([y, x+1])

        return newMoves

    def solveMaze(self, currentPath):

        # try to find path between self.entries[0] and self.entries[1]
        # call possibleMoves for head of currentPath
        # if no moves, end iteration, if 1 move, append and continue,
        # if more than 1 move, then branch each possible path

        branchOrEnd = False
        while branchOrEnd == False:

            #print("\nNew loop\n%s" % (currentPath))
            head = len(currentPath)-1
            possMoves = self.possibleMoves(currentPath[head])


            # remove existing head from possible moves
            if currentPath[head-1] in possMoves:
                possMoves.remove(currentPath[head-1])


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
                    self.solveMaze(buffPath)

            # only 0 option
            elif nPossMoves == 1:
                # check if we're at the end
                if self.entries[1][0] == possMoves[0][0] and \
                        self.entries[1][1] == possMoves[0][1]:
                            currentPath.append(possMoves[0])
                            self.solution = currentPath
                            return True
                # otherwise continue
                else:
                    currentPath.append(possMoves[0])

    def updateMazeWithSolution(self):

        for x in self.solution:
            self.mazeData[x[0], x[1]] = self.scd


    def createSolutionImage(self, newName):

        # make a new PIl image based on solution
        solved = Image.new('RGB', (self.width, self.height), 'White')
        solvedpx = solved.load()

        for y in range(0, self.height):
            for x in range(0, self.width):

                z = self.mazeData[y, x]
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

        # load image
        self.im = Image.open(imageLocation)

        # load pixels
        self.px = self.im.load()

        # what do we know about image
        self.height = self.im.height
        self.width = self.im.width
        print("Image %s loaded, H:%s W:%s" % (imageLocation, self.height, self.width))

        # generate maze data as an array
        self.makeMaze()

        self.solution = []
        self.solution.append(self.entries[0])
        self.solveMaze(self.solution)
        #print("Solution (y,x): %s" % (self.solution))

        self.updateMazeWithSolution()
        #print(self.mazeData)

        # make solution into an image
        self.newName = imageLocation.split('.')[0] + "_solved." + imageLocation.split('.')[1]
        self.createSolutionImage(self.newName)



if __name__ == "__main__":

    maze = potatoMaze("maze200px.png")
