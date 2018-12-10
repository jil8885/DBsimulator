import pymysql as mariadb
import pymongo as mongo
import random, string
from datetime import datetime, timedelta
import numpy as np

def initialize():
    password = "a981212"
    connect = mariadb.connect("localhost", "root", password, "hotel")
    cursor = connect.cursor()
    client = mongo.MongoClient("localhost")
    db = client.hotel
    for collection in db.list_collection_names():
        db.drop_collection(collection)
    db.create_collection("room_temperature")
    db.create_collection("employee_position")
    temperature = db.room_temperature
    positiondb = db.employee_position
    create_table = []
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'hotel'")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute("drop table if exists " + table[0])
        connect.commit()
    create_table.append("create table room_information (room_number int primary key , type_id int, floor int, state_in_room boolean, state_cleaned boolean, state_transaction int, target_temperature double, target_humidity double)")
    create_table.append("create table room_type (id int(11) primary key, name varchar(11), capacity int(11), smoking boolean, price int)")
    create_table.append("create table complain (id int(11) primary key, manager_id int, guest_id int, type_id int, contents varchar(20), completed boolean)")
    create_table.append("create table complain_type (id int(11) primary key, name varchar(20))")
    create_table.append("create table employee_information (id int(11) primary key, name varchar(20), sex varchar(20), date_of_birth date, date_of_join date, date_of_leave date, contact_phone varchar(20), contact_email varchar(40), address varchar(20), type_id int, position_id int, area varchar(20), salary int, language varchar(20))")
    create_table.append("create table employee_type (id int primary key, name varchar(20))")
    # create_table.append("create table employee_position (id int primary key, name varchar(20))")
    create_table.append("create table guest_information (id int primary key,  name varchar(20),  sex varchar(20),  date_of_birth date,  contact_phone varchar(20),  contact_email varchar(40),  address varchar(20),  country varchar(20),  language varchar(20),  belong varchar(20),  type_id int,  smoking boolean,  memo varchar(20))")
    create_table.append("create table guest_type (id int primary key,  name varchar(20))")
    create_table.append("create table membership (guest_id int,  type_id int,  start date,  end date,  point int)")
    create_table.append("create table membership_type (id int primary key,  name varchar(20))")
    create_table.append("create table reservation_type (id int primary key,  name varchar(20))")
    create_table.append("create table keycard (id int primary key,  type_id int,  room_number int,  guest_id int)")
    create_table.append("create table keycard_type (id int primary key,  name varchar(20))")
    create_table.append("create table reservation (id int primary key,  time date,  type_id int,  room_number int,  manager_id int,  guest_id int,  num_of_guest int,  check_in date,  check_out date,  payment_id int,  state int,  memo varchar(20),  successful int)")
    create_table.append("create table reservation_log (id int primary key,  time date,  type_id int,  room_number int,  manager_id int,  guest_id int,  num_of_guest int,  check_in date,  check_out date,  price int,  state int,  memo varchar(20),  successful int)")
    create_table.append("create table room_equipment (room_number int primary key,  equipment_id int,  base_count int,  count int)")
    create_table.append("create table equipment (id int primary key,  name varchar(20),  type int,  count int,  seller varchar(20))")
    create_table.append("create table equipment_log (id int primary key,  time date,  room_number int,  equipment_id int,  count int,  type int,  reason varchar(20))")
    create_table.append("create table room_temperature_log (id int primary key,  time date,  room_number int,  temperature float, humidity float )")
    create_table.append("create table attendance (id int primary key,  employee_id int,  work_start_time date,  work_end_time date)")
    create_table.append("create table payment (id int primary key,  type_id int,  base_price int,  price int)")
    create_table.append("create table payment_type (id int primary key,  name varchar(20))")
    create_table.append("create table payment_details (payment_id int,  contents varchar(20),  item_price int)")
    for sql in create_table:
        cursor.execute(sql)
    connect.commit()

    insert = []
    temp_list = np.arange(-10.0, 30.0, 0.1)
    humi_list = np.arange(0.0, 100.0, 0.1)
    for floor in range(1, 16):
        for roomNum in range(1, 11):
            insert.append((int(str(floor) + str(roomNum).zfill(2)), random.randint(0, 4), floor, False, True, 0, 0.0, 0.0))
            temperature.insert_one({"room": (int(str(floor) + str(roomNum).zfill(2))), "temperature": round(temp_list[random.randrange(len(temp_list))], 1), "humidity": round(humi_list[random.randrange(len(humi_list))], 1)})
    sql = "insert into room_information(room_number, type_id, floor, state_in_room, state_cleaned, state_transaction, target_temperature, target_humidity) values "
    for room in insert:
        sql += str(room) + ", "
    cursor.execute(sql[:-2])
    connect.commit()

    sql = "insert into guest_information (id, name, sex, date_of_birth, contact_phone, contact_email, address, country, language, belong,  type_id, smoking, memo) values "
    id = 0
    insert = []
    while id < 5000:
        birth = random_date()
        name = random_name()
        contact = random_contact()
        sex = random.sample(["Male", "Female"], 1)[0]
        country = random.sample(["USA", "Germany", "France", "Korea", "China", "Japan", "Spain", "Saudi", "Russia", "Space"], 1)[0]
        language = random_language()
        insert.append((id + 1, name, sex, birth.strftime("%Y-%m-%d"), contact, random_email(name), "Null", country, language, "Null",  0, random.sample([True, False], 1)[0], "Customer" + str(id)))
        id += 1
    for customer in insert:
        sql += str(customer) + ", "
    cursor.execute(sql[:-2])
    connect.commit()

    sql = "insert into employee_information (id, name, sex, date_of_birth, date_of_join, date_of_leave, contact_phone, contact_email, address, type_id, position_id, area, salary, language) values "
    id = 0
    insert = []
    floor_list = list(range(0, 16))
    while id < 50:
        birth = random_date()
        name = random_name()
        contact = random_contact()
        start = random_date2(birth + timedelta(days=20 * 365), datetime.now())
        if start is not None:
            end = random_date2(start, datetime.now())
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
        else:
            start = datetime.now().strftime("%Y-%m-%d")
            end = datetime.now().strftime("%Y-%m-%d")
        sex = random.sample(["Male", "Female"], 1)[0]
        language = random_language()
        type = random.randrange(1, 4)
        level = random.randrange(1, 10)
        salary = random_salary(type, level)
        insert.append((id + 1, name, sex, birth.strftime("%Y-%m-%d"), start, end, contact, random_email_employee(name), "Null", type, level, str(random.randrange(5) + 1) + "F", salary, language))
        positiondb.insert_one({"id": id + 1, "position" : random.sample(floor_list,1)[0]})
        id += 1
    for customer in insert:
        sql += str(customer) + ", "
    cursor.execute(sql[:-2])
    connect.commit()
    connect.close()


def random_salary(type, level):
    type_percent = [0.85, 1, 1.2]
    level_percent = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6]
    return type_percent[type - 1] * level_percent[level - 1] * 10000


def random_date():
    delta = datetime.now() - datetime(1950, 1, 1)
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return datetime(1950, 1, 1) + timedelta(seconds=random_second)


def random_date2(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    if int_delta < 0:
        return None
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_name():
    name = ""
    for x in range(4, 9):
        name += string.ascii_lowercase[random.randrange(26)]
    return name


def random_contact():
    return str(random.randrange(999)).zfill(3) + "-" + str(random.randrange(9999)).zfill(4) + "-" + str(random.randrange(999)).zfill(3)


def random_email(name):
    return name + str(random.randrange(9999)) + "@" + random.sample(["gmail.com", "naver.com", "daum.net", "hanyang.ac.kr"], 1)[0]


def random_email_employee(name):
    return name + str(random.randrange(9999)) + "@hotel.net"


def random_language():
    return random.sample(["English", "Dutch", "French", "Korean", "Chinese", "Japanese", "Spanish", "Arab", "Wakanda", "Russian", "Alien", "C", "Python", "Java", "Ruby", "C++", "C#", "Php", "JavaScript"], 1)[0]


initialize()
