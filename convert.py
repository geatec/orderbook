'''
REQUIREMENTS
============

for each row:
    general info, timestamp etc.
    .
    best bid (highest value)
    best ask (lowest value)
    .
    amount best bid
    amount best ask
    .
    .
    worst bid (lowest value)
    amount worst bid (lowest value)
    .
    ... 
    best bid (highest value)
    amount best bid (highest value)
    .
    .
    best ask (lowest value)
    amount best ask (lowest value)
    .
    ...
    worst ask(highest value)
    amount worst ask(highest value)
'''

import os
import pickle

import base

maxNrOfBids = maxNrOfAsks = 500

value, amount = 0, 1

oldDay = 0

for ordFileName in os.listdir (base.orderDir):
    ordFileName = ordFileName.replace ('\\', '/');  # Make portable for Windows, Linux and OsX
    ordFilePath = f'{base.orderDir}/{ordFileName}'
    
    pickleFileName = ordFileName.replace ('.ord', '.csv')
    pickleFilePath = f'{base.csvDir}/{pickleFileName}'
    
    # Close previous csv file and open new one
    dayPos = ordFileName.index ('_') + 8
    newDay = ordFileName [dayPos : dayPos + 2]
    if newDay != oldDay:
        oldDay = newDay
        try:
            csvFile.close ()
        except:
            pass
        csvFile = open (pickleFilePath, 'w')
        
    # Open, use and close ord file
    with open (ordFilePath, 'rb') as ordFile:
        orderBooks = pickle.load (ordFile)
        
        for orderBook in orderBooks:
            csvFile.write (f'{ordFileName}, {orderBook [0]}, {orderBook [1]}, {orderBook [2]}, , ')
            
            bids = sorted (orderBook [3], key = lambda element: element [0])
            asks = sorted (orderBook [4], key = lambda element: element [0])
            
            lowest = 0
            highest = -1
            
            csvFile.write (f'{bids [highest][value]}, {asks [lowest][value]}, , ')
            csvFile.write (f'{bids [highest][amount]}, {asks [lowest][amount]}, , , ')

            csvFile.write ('bids:, ')
            for bidIndex in range (len (bids), maxNrOfBids):
                bids.append ((0, 0))
            for bid in bids:
                csvFile.write (f'{bid [value]}, {bid [amount]}, , ')
            
            csvFile.write ('asks:, ')
            for askIndex in range (len (asks), maxNrOfAsks):
                asks.append ((0,0))
            for ask in asks:
                csvFile.write (f'{ask [value]}, {ask [amount]}, , ')
                
            csvFile.write ('\n')
            
try:
    csvFile.close ()
except:
    print ('Done nothing useful')
            
            
        
    
    