# Standard
import sys
import time
import pickle
import json

# Installed
import pysher

# Custom
import base
import datetime

# Order inside bids and asks: (price, amount)

appkey = 'de504dc5763aeef9ff52'
nrOfOrderBooksPerFile = 8
orderBookIndex = nrOfOrderBooksPerFile
pickleFile = None
binaryOrderBooks = None

def handleOrderBook (jsonOrderBook):
    global orderBookIndex
    global pickleFile
    global binaryOrderBooks

    asciiOrderBook = json.loads (jsonOrderBook)
    
    if orderBookIndex == nrOfOrderBooksPerFile:
        try:
            pickle.dump (binaryOrderBooks, pickleFile)
            pickleFile.close ()
        except:
            pass
        
        orderBookIndex = 0
        binaryOrderBooks = []
        
        aNow = datetime.datetime.now ()
        pickleFileName = f'orderbooks_y{aNow.year%100:02}m{aNow.month:02}d{aNow.day:02}_h{aNow.hour:02}m{aNow.minute:02}s{aNow.second:02}.ord'
        pickleFilePath = f'{base.orderDir}/{pickleFileName}'
        pickleFile = open (pickleFilePath, 'wb')
        print ('\nFile:', pickleFileName)
    
    binaryOrderBooks.append ([
        orderBookIndex,
        datetime.datetime.now (),
        asciiOrderBook ['timestamp'],
        [(float (bid [0]), float (bid [1])) for bid in asciiOrderBook ['bids']],
        [(float (ask [0]), float (ask [1])) for ask in asciiOrderBook ['asks']]
    ])
        
    print ('Orderbook:', orderBookIndex)     
    orderBookIndex += 1
                
def handleConnection (dummyData):
    channel = pusher.subscribe ('order_book_eurusd')
    channel.bind ('data', handleOrderBook)

pusher = pysher.Pusher (appkey)
pusher.connection.bind ('pusher:connection_established', handleConnection)
pusher.connect ()

while True:
    time.sleep(0.5)
    