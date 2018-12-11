import pymysql as mariadb
import pymongo as mongo
import random, string
from datetime import datetime, timedelta
import numpy as np
import time

def execute():
    password = "a981212"
    connect = mariadb.connect("localhost", "root", password, "hotel")
    cursor = connect.cursor()
    client = mongo.MongoClient("localhost")
    db = client.hotel
    temperature = db.room_temperature
    positiondb = db.employee_position
    cursor.execute("select room_number, state_in_room from room_information where state_transaction = 2")
    rooms = cursor.fetchall()
    for room in random.sample(rooms, len(rooms) // 3):
        if room[1] == 1:
            cursor.execute("update room_information set state_in_room = 0 where room_number = " + str(room[0]))
        else:
            cursor.execute("update room_information set state_in_room = 1 where room_number = " + str(room[0]))
    connect.commit()
    var = [-0.5 , -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
    for x in range(1, 16):
        for y in range(1, 11):
            room_num = x * 100 + y
            room_temp = temperature.find_one({"room" : room_num})["temperature"]
            room_humi = temperature.find_one({"room" : room_num})["humidity"]
            var_temp = random.sample(var, 1)[0]
            var_humi = random.sample(var, 1)[0]
            temperature.update_one({"room" : room_num}, {"$set" :{"temperature" : room_temp + var_temp, "humidity" : room_humi + var_humi}} ,True)
    for x in range(50):
        positiondb.update_one({"id" : x}, {"$set": {"position": random.randint(0, 15)}}, True)
execute()
    
