# -*- coding: utf-8 -*
"""
Created on Sat Feb 22 11:09:57 2014

@author: Pio Calderon
"""

import numpy as np
from PIL import Image
from imageprocessing import plot_cosine_similarity
import matplotlib.pyplot as plt

def constructChessGrid(gridSize, sizeBox, probability, run, mutation):
    """
    Construct a chess grid with various input features.
    """

    grid = np.array([[[255,255,255,255]]*gridSize]*gridSize)
    numBox = gridSize/sizeBox   
    
    for i in xrange(numBox):
        for j in xrange(numBox):
            rowIndex1, rowIndex2 = i*sizeBox, (i+1)*sizeBox
            colIndex1, colIndex2 = j*sizeBox, (j+1)*sizeBox
            if np.random.uniform() < probability:
                grid[rowIndex1:rowIndex2, colIndex1: colIndex2] = [[[0,0,0,255]]*sizeBox]*sizeBox
    im = Image.fromarray(np.uint8(grid), mode="RGBA")
    im.save("grid_s{0}_sb{1}_p{2}_run{3}_m{4}.png".format(gridSize,sizeBox, probability, run,mutation))
    return grid

def main(sizeBoxList, probabilities, mutations, numRun, size):
    """
    Check cosine similarity for different chessgrids.
    """
    for sizeBox in sizeBoxList:
        for mutation in mutations:
            for probability in probabilities:
                g=open('RUNAVERAGED_size{0}sizebox{1}mutation{2}probability{3}.csv'.format(size,sizeBox, mutation, probability), 'w')
                g.write('framelength,similarity,std\n')
                runList = []
                for run in xrange(numRun):
                    print "start: sizeBox: ", sizeBox, " ;p: ", probability, "run: ", run
                    grid = constructChessGrid(size, sizeBox, probability, run, mutation)      
                    ratio,similarityList = plot_cosine_similarity(grid,r'grid_s{0}_sb{1}_p{2}_run{3}_m{4}.png'.format(size,sizeBox, probability, run, mutation))
                    runList.append(similarityList) 
                runList = zip(*runList)
                runMean = np.mean(runList,1)
                runErr = np.std(runList,1)/np.sqrt(numRun)
                    #        plt.plot(ratio, similarityList,label="p={0}".format(probability))
                plt.errorbar(ratio, runMean, yerr=runErr,label="p={0}".format(probability))
                for index in xrange(len(ratio)):
                    g.write("{0},{1},{2}\n".format(ratio[index],runMean[index],runErr[index]))
                g.close()
            plt.xlabel(r'relative frame length $k$')
            plt.ylabel(r'cos $\theta$')
            plt.ylim(ymin = 0.5, ymax=1)
            plt.legend(loc="lower right")
            plt.savefig("CS_grid_s{0}_sb{1}_m{2}.png".format(size,sizeBox,mutation),bbox_inches="tight")
            plt.close()
        
if __name__ == "__main__":
    sizeBoxList = [64,32,16,8,4,2,1]
    probabilities = [0.25,0.375,0.5]
    mutations = [0]
    numRun=10
    size = 128
    
    main(sizeBoxList, probabilities, mutations, numRun, size)
