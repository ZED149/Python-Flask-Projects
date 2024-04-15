

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.ZED_Blog
entries = db.blogs
my_dict = {
    "content": "Today after a very long time I have comeback to my university. My university is FAST NUCES. For now I am in my library and learning new technologies like Flask in Python etc. This has been a very challenging decision for me to come back to FAST. But now I have decided that I will come here daily and will be using library enviournment to learn new things and complete my goals before my sister marriage. Thanks.",
    "date": "Apr 2024",
    "date_datetime": "15-04-2024"
}

entries.insert_one(my_dict)

for e in entries.find():
    print(e)
