# sqlQueries.py

import random
import sqlite3

# generate userids, bookingids
def generateid():
    id = random.randint(11111, 99999)
    return id

# retrieve the number of passengers from a particular booking
def book_passengers(bookid):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT passengers FROM booking WHERE booking_id = ?", (bookid,))
    seats = cursor.fetchone()[0]
    conn.close()
    return seats

# update the number of seats left after booking
def update_bus_passengers(busid, newpass):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE bus SET capacity = capacity - ? WHERE busid = ?", (newpass, busid,))
    conn.commit()
    conn.close()

# fetch all the buses from a location to_ to from_
def allbus(to_, from_):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE to_ = ? AND from_ = ?", (to_, from_,))
    myresult = cursor.fetchall()
    conn.close()
    return myresult

# fetch all the details of a bus (eg. rating, time, seats_left, etc)
def busdetails(busid):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE busid = ?", (busid,))
    myresult = cursor.fetchall()
    conn.close()
    return myresult

# add a new user to the users table
def userinsert(det):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    sql = "INSERT INTO user (userid, username, phone, email, bookid) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, det)
    conn.commit()
    conn.close()

# add a new booking to the booking table
def bookinginsert(det):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    sql = "INSERT INTO booking (booking_id, userid, busid, passengers) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, det)
    conn.commit()
    conn.close()

# retrieve the booking details of a particular booking
def booking_details(id):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (id,))
    result1 = cursor.fetchall()
    cursor.execute("SELECT * FROM user WHERE userid IN (SELECT userid FROM booking WHERE booking_id = ?)", (id,))
    result2 = cursor.fetchall()
    cursor.execute("SELECT * FROM bus WHERE busid IN (SELECT busid FROM booking WHERE booking_id = ?)", (id,))
    result3 = cursor.fetchall()
    conn.close()
    return result1 + result2 + result3

# delete a particular reservation
def delete(bookid):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    det = booking_details(bookid)
    userid = det[0][1]
    cursor.execute("DELETE FROM booking WHERE booking_id = ?", (bookid,))
    cursor.execute("DELETE FROM user WHERE userid = ?", (userid,))
    conn.commit()
    conn.close()

# update the details of booking of user [name, email, number, seats]
def updatebookuser(user, book, bookid):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT userid FROM booking WHERE booking_id = ?", (bookid,))
    userid = cursor.fetchone()[0]
    pas = book
    updatebookingpassengers(bookid, pas)
    name, phno, email = user
    cursor.execute("UPDATE user SET username = ?, phone = ?, email = ? WHERE userid = ?", (name, phno, email, userid,))
    conn.commit()
    conn.close()

# update the number of passengers in a booking
def updatebookingpassengers(bookid, pas):
    conn = sqlite3.connect('projectdb.sqlite')
    cursor = conn.cursor()
    pas = pas[0]
    cursor.execute("UPDATE booking SET passengers = ? WHERE booking_id = ?", (pas, bookid,))
    conn.commit()
    conn.close()
