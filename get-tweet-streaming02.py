import pymongo
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Setting mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
collection = mydb["tweet"]

# Set tokenize of twitter
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Get tweet streaming
twitter_stream = TwitterStream(auth=oauth)
iterator = twitter_stream.statuses.filter(track="Marvel", language="en") #searchคำ

# This function will insert tweet to mongodb
def getTweetToMongo(data, count):  
    collection.delete_many({}) #ลบข้อมูลในcollectionทั้งหมดก่อนที่จะrunใหม่
    for tweet in data:
        print('-------------------------')
        print(count) #นับจำนวนข้อความตามtweet_countจากมากไปน้อย
        print('-------------------------')
        count -= 1

        if "text"  in tweet:
            collection.insert_one(tweet) #นำtextใส่ไปยังcollection
        else:
            pass
        
        if count <= 0: 
            print('Complete')  #ถ้าข้อมูลน้อยกว่าหรือเท่ากับ 0 ให้ปริ้น Completeแล้ว breakออกมา
            break 
    return

# Call the function
tweet_count = 2000 #จำนวนข้อความที่ต้องการsearch
getTweetToMongo(iterator, tweet_count) #เรียกใช้method getTweetToMongo