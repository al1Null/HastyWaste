import serial
import time
import datetime
from pymongo import MongoClient


# Configuration
serial_port = '/dev/cu.wchusbserial1410'
mongodb_host = 'mongodb+srv://hastyUser2:trashPass123321@hastydb-9azwl.gcp.mongodb.net/admin?retryWrites=true&w=majority'

# Connect to Serial Port for communication
ser = serial.Serial(serial_port, 9600, timeout=0)

# Connect to MongoDB
client = MongoClient(mongodb_host)
db = client['history']
collection = db['bin01']

# for doc in collection.find({}):
#     print(doc)

# Setup a loop to send values at fixed intervals in seconds
fixed_interval = 1
while 1:
    try:
        # Getting data from serial port of arduino
        raw = ser.readline()
        while len(raw) == 0 or "," not in str(raw):
            raw = ser.readline()

        print(raw)

        dist = ""
        moi = ""
        raw = str(raw)
        for char in raw.split(",")[0]:
            if char.isdigit():
                dist += char
        for char in raw.split(",")[1]:
            if char.isdigit():
                moi += char

        if dist == "": dist = None
        else: distance = int(dist)
        if moi == "": moist = None
        else: moist = int(moi)
        now = datetime.datetime.now()

        currentFilled = int( ((33 - distance) / 33) * 100 )
        if currentFilled < 0: currentFilled = 0
        today = now 
        amount = 10
        totalDifference = 0
        size = collection.count_documents({})
        if size <= 10:
            amount = size
        docs = [doc for doc in list(collection.find({}))[ -1 * (amount+1):]]
        for i in range(amount - 1):
            firstDoc = docs[i].get('current_filled')
            secondDoc = docs[i+1].get('current_filled')
            if firstDoc is None or secondDoc is None:
                percentDifference = 0
            else:
                
                percentDifference = secondDoc - firstDoc
            if percentDifference <  0:
                percentDifference = secondDoc
            totalDifference += percentDifference
        averageChange = totalDifference / amount

        # 100% - (currentPercentFull + averageChange * times) = 0
        # (100% - currentPercentFull) / averageChange = times
        if averageChange > 0:
            averageTimesToChange = (100 - currentFilled) / averageChange
            # 10sec ;; times * 10 / 3600 
            timeInSeconds = averageTimesToChange / 1
            expected = datetime.datetime.now() + datetime.timedelta(seconds=timeInSeconds)
            nextCollection = expected
        else:
            nextCollection = None
        isFull = True if distance < 4 else False
        hasLeak = True if moist > 600 else False

        doc = {
            'current_filled': currentFilled, 
            'next_collection_time': nextCollection,
            'current_time': today,
            'is_full': isFull,
            'has_leak': hasLeak,
        }
        collection.insert_one(doc)
        print(doc)


    except serial.SerialTimeoutException:
        print('Error! Could not read the distance from unit')
    except ValueError:
        print('Error! Could not convert distance to float')
    finally:
        time.sleep(fixed_interval)