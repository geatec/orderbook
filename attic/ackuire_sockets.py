'''
            pusher = new Pusher('de504dc5763aeef9ff52'),
            orderBookChannel = pusher.subscribe('order_book'),
            i = 0;

        orderBookChannel.bind('data', function (data) {
            bidsPlaceholder.innerHTML = '';
            asksPlaceholder.innerHTML = '';

            for(i = 0; i < data.bids.length; i += 1) {
                bidsPlaceholder.innerHTML = bidsPlaceholder.innerHTML + data.bids[i][1] + ' BTC @ ' + data.bids[i][0] + ' USD' + '<br />';
            }
            for(i = 0; i < data.asks.length; i += 1) {
                asksPlaceholder.innerHTML = asksPlaceholder.innerHTML + data.asks[i][1] + ' BTC @ ' + data.asks[i][0] + ' USD' + '<br />';
            }
        });
'''

import pysher
import sys
import time



# Add a logging handler so we can see the raw communication data

'''
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)
'''

appkey = 'de504dc5763aeef9ff52'

pusher = pysher.Pusher(appkey)

counter = 0

def  my_func(*args, **kwargs):
    global counter
    counter += 1
    print (counter)
    
    # print("processing Args:", args)
    # print("processing Kwargs:", kwargs)

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = pusher.subscribe('order_book')
    channel.bind('data', my_func)

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    # Do other things in the meantime here...
    time.sleep(0.5)
    
    