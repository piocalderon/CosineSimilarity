# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 01:11:47 2014

@author: Pio Calderon
"""

from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

def plot_cosine_similarity(arr,imgPath):
    """
    Plots to a png file and records to a csv file the cosine similarity of an image
    as a function of the frameLength.
    """
    left2right, up2down = int(arr.shape[1]),int(arr.shape[0])
    ratio= np.linspace(0.01,0.5,50)
    frameLengths= np.array(ratio*left2right, dtype="int")
    
    similarityList = []
    for frameLength in frameLengths:
        #print list(frameLengths).index(frameLength)
        numCol = left2right - frameLength + 1#int(math.ceil(1.0*left2right/frameLength))
        numRow = up2down - frameLength + 1
        #arrCopy=np.copy(arr)
        #arrCopy.resize(frameLength*numCol, frameLength*numCol, 4)
        #arrCopy= np.copy(arrCopy)
        count = []
        similarity = 0

        for i in xrange(numRow):
            for j in xrange(numCol):
                rowIndex1, rowIndex2 = i, i+frameLength
                colIndex1, colIndex2 = j, j+frameLength

                if i == 0 and j == 0:
                    frame = arr[rowIndex1:rowIndex2, colIndex1: colIndex2]
                    colors = np.array([0,0])
                    for row in frame:
                        row = [list(x) for x in row]
                        numBlack = row.count([0,0,0,255])
                        numWhite = row.count([255,255,255,255])
                        colors[0] += numBlack #black
                        colors[1] += numWhite #white
                    base = colors
                    topRow = [list(x) for x in frame[0]]
                    numBlack = topRow.count([0,0,0,255])
                    numWhite = topRow.count([255,255,255,255])
                    topRowCount = np.array([numBlack, numWhite])
                elif i != 0 and j == 0:
                    bottomRow = arr[rowIndex2-1, colIndex1:colIndex2]
                    bottomRow = [list(x) for x in bottomRow]
                    numBlack = bottomRow.count([0,0,0,255])
                    numWhite = bottomRow.count([255,255,255,255])      
                    bottomRowCount = np.array([numBlack, numWhite])
                    colors = np.array(base) - topRowCount + bottomRowCount 
                elif j != 0:
                    rightColumn = arr[rowIndex1: rowIndex2, colIndex2-1]
                    rightColumn = [list(x) for x in rightColumn]
                    numBlack = rightColumn.count([0,0,0,255])
                    numWhite = rightColumn.count([255,255,255,255])
                    rightColumnCount = np.array([numBlack, numWhite])
                    leftColumn = arr[rowIndex1: rowIndex2, colIndex1-1]
                    leftColumn = [list(x) for x in leftColumn]
                    numBlack = leftColumn.count([0,0,0,255])
                    numWhite = leftColumn.count([255,255,255,255])
                    leftColumnCount = np.array([numBlack, numWhite])
                    colors = np.array(count[-1]) - leftColumnCount + rightColumnCount

                if len(count) > 0:
                    if sum(count[-1]) != 0:
                        count[-1] = 1.0*count[-1]/sum(count[-1])
                        normalization = np.sqrt(count[-1][0]**2 + count[-1][1]**2)
                    else:
                        normalization = 1
                    count[-1] =count[-1]/normalization
                count.append(colors)

                if i == numRow-1 and j == numCol-1:
                    if sum(count[-1]) != 0:
                        count[-1] = 1.0*count[-1]/sum(count[-1])
                        normalization = np.sqrt(count[-1][0]**2 + count[-1][1]**2)
                    else:
                        normalization = 1
                    count[-1] =count[-1]/normalization 

        counter = 0
        for i in range(numRow):
            for j in range(numCol):
                if i == numRow-1 and j == numCol-1: #last entry
                    continue
                elif j!= 0 and j % (numCol - 1) == 0 and numCol - (j+1) >= frameLength: # nasa last columnnn
                    toCompareIndex = (i*numRow + j) + frameLength*numCol
                    counter += 1
                    similarity += sum(count[i*numRow+j]* count[toCompareIndex])
                    #print count[i*numRow + j], count[toCompareIndex]
                elif ((i* numRow+ j) / numRow) + 1 >= numRow and numRow - (i+1) >= frameLength: # nasa last row
                    toCompareIndex = (i*numRow + j) + frameLength*1
                    counter += 1
                    similarity += sum(count[i*numRow + j] * count[toCompareIndex])
                    #print count[i*numRow + j],count[toCompareIndex]
                else:
                    toCompareIndexList = []
                    if numCol - (j+1) >= frameLength:
                        toCompareIndexList.append(i*numRow + j + 1*frameLength)
                    if numRow - (i+1) >= frameLength:    
                        toCompareIndexList.append(i*numRow + j + frameLength*numCol)
                    for toCompareIndex in toCompareIndexList:
                        counter += 1
                        similarity += sum(count[i*numRow + j] * count[toCompareIndex])            
                        #print count[i*numRow + j],count[neighborIndex]

        similarityList.append(similarity/counter)

    cosfig = plt.figure()
    ax= cosfig.add_subplot(111)
    ax.plot(ratio, similarityList)
    plt.xlabel('frame length / image dimension')
    plt.ylabel('average cosine similarity')
    plt.savefig('cosinesimilarity_{0}.png'.format(imgPath))
    
    g=open('cosinesimilarity_{0}.csv'.format(imgPath[:-4]), 'w')
    g.write('framelength,similarity\n')
    for index in xrange(len(frameLengths)):
        g.write("{0},{1}\n".format(ratio[index],similarityList[index]))
    g.close()
    
    return ratio,similarityList
    
