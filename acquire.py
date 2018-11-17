import ccxt
import time
import datetime
import pickle
import copy
import json

import base
import get_size

# Order inside bids and asks: (price, amount)

#print (ccxt.exchanges)
exchange = ccxt.bitstamp ({'enableRateLimit': True})

books = []
oldTimeStamp = 0
nrOfOrderBooksPerFile = 8

newTime = datetime.datetime.now ()
# asciiOrderBook = None

while True:
    pickleFileName = f'orderbooks_y{newTime.year%100:02}m{newTime.month:02}d{newTime.day:02}h{newTime.hour:02}m{newTime.minute:02}s{newTime.second:02}.ord'
    print ('File:', pickleFileName)
    
    pickleFilePath = f'{base.orderDir}/{pickleFileName}'
    
    with open (pickleFilePath, 'wb') as pickleFile:
        binaryOrderBooks = []
        
        while True:
            oldTime = newTime
            newTime = datetime.datetime.now ()
            deltaTime = newTime - oldTime
            deltaSeconds = deltaTime.total_seconds ()

            if deltaSeconds:
                print (round (deltaSeconds, 2))      
                if deltaSeconds > 2:
                    print ('Timeout!!!')
            
            try:    
                # oldAsciiOrderBook = copy.deepcopy (asciiOrderBook)
                
                asciiOrderBook = exchange.fetch_order_book ('EUR/USD')
                
                '''
                if json.dumps (asciiOrderBook) == json.dumps (oldAsciiOrderBook):
                    print (json.dumps (asciiOrderBook))
                    print ('Seen before')
                '''
                
                # print (orderBook.keys ())
                # print (get_size.get_size (orderBook))
                # print (orderBook)
                
                timeStamp = asciiOrderBook ['timestamp']
                
                if timeStamp != oldTimeStamp:
                    oldTimeStamp = timeStamp
                    
                    orderBookSubIndex = len (binaryOrderBooks)
                    
                    if orderBookSubIndex < nrOfOrderBooksPerFile:
                        print ('Orderbook subindex', orderBookSubIndex)
                        
                        binaryOrderBooks.append ([
                            orderBookSubIndex,
                            timeStamp,
                            asciiOrderBook ['datetime'],
                            asciiOrderBook ['nonce'],
                            [(float (bid [0]), float (bid [1])) for bid in asciiOrderBook ['bids']],
                            [(float (ask [0]), float (ask [1])) for ask in asciiOrderBook ['asks']]
                        ])
                    else:
                        break;
            except Exception as exception:
                print (exception)
                
            time.sleep (0.1)
            
        pickle.dump (binaryOrderBooks, pickleFile)
