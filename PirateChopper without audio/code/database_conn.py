import pymongo, json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["gamedata"]
mycol = mydb["Users"]

def scores():
    x = mycol.find().sort("coins",-1).limit(5)
    ans = []
    for i in x:
        ans.append(i)
    return ans
def register(name, pwd=""):
    if(len(name)>0):
        mydata = {"name": name, "password": pwd, "max_level":0, "health": 100, "coins": 0, "music":0, "jump_key":0, "right_key":0, "left_key":0}
        x = mycol.insert_one(mydata)
        return True
    else:
        return False
def login(name, pwd):
    data = mycol.find_one({"name": name})
    if(data == None):
        return False
    if(pwd == data["password"]):
        with open("dataset.json", "w") as f:
            data = {"name":name,
                    "start_game": 0, 
                    "max_level": data["max_level"], 
                    "health": data["health"], 
                    "coins": data["coins"],
                    "music": data["music"],
                    "jump_key": data["jump_key"],
                    "right_key": data["right_key"],
                    "left_key": data["left_key"]}
            json.dump(data, f)
        return True
    return False

def update(name, max_level, health, coins):
    myquery = {"name": name}
    newvalues = {"$set": {"max_level":max_level, "health": health, "coins": coins}}
    if(mycol.update_one(myquery, newvalues)):
        return True
    return False

def update_controls(name, jump_key, left_key, right_key):
    myquery = {"name":name}
    newvalues = {"$set":{"jump_key":jump_key, "left_key":left_key, "right_key":right_key}}
    if(mycol.update_one(myquery, newvalues)):
        return jump_key