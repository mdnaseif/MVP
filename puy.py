from pymongo import MongoClient
import time
from datetime import datetime
from prophet.serialize import model_to_json
import json

client = MongoClient("mongodb+srv://MDNASEIF:1928qpwO@mlops.la0z4v1.mongodb.net/?retryWrites=true&w=majority")


acc = 0.9
db = client.assin

#collection name
collection = db["models"]

items = [
    "كاسكارا-",
    "بروتي-",
    "شاي مثلج - توت ورمان-",
    "شاي مثلج - يوسفي-",
    "كولد برو-",
]
count = 1

for item in items:
    file_name = item
    
    #Upload to mongo db
    with open(f"{file_name}.json") as f:
        model = json.load(f)
    collection.insert_one({"model":model, "date":str(datetime.date(datetime.now())), "item":item, "itemId":count})
    print("saved succesfully")
    count = count + 1