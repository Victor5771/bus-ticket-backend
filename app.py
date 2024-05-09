from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlQueries import update_bus_passengers, delete, booking_details, updatebookuser, generateid, userinsert, bookinginsert

app = Flask(__name__)

# Connection to SQLite database
def connect_db():
    conn = sqlite3.connect('projectdb.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# Create the tables in SQLite database
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Create bus table
    cursor.execute('''CREATE TABLE IF NOT EXISTS bus (
                        busid INTEGER PRIMARY KEY,
                        to_ TEXT,
                        from_ TEXT,
                        capacity INTEGER
                    )''')

    # Create user table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                        userid INTEGER PRIMARY KEY,
                        username TEXT,
                        phone TEXT,
                        email TEXT,
                        bookid INTEGER
                    )''')

    # Create booking table
    cursor.execute('''CREATE TABLE IF NOT EXISTS booking (
                        booking_id INTEGER PRIMARY KEY,
                        userid INTEGER,
                        busid INTEGER,
                        passengers INTEGER,
                        FOREIGN KEY (userid) REFERENCES user(userid),
                        FOREIGN KEY (busid) REFERENCES bus(busid)
                    )''')

    conn.commit()
    conn.close()

# Custom error handler for when origin and destination are the same
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Search Page
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from12 = request.form['from']
        to12 = request.form['to']
        if from12 == to12:
            return render_template('404.html'), 404
        else:
            return redirect(f"/search/{from12}/{to12}")
    return render_template('index.html')

# Search bar for updating
@app.route('/update', methods=["GET", "POST"])
def update():
    if request.method == "POST":
        id = request.form['id']
        return redirect(f"/change/{id}")
    return render_template('update.html')

# Update Page
@app.route('/change/<id>')
def change(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (id,))
    busd = cursor.fetchall()
    conn.close()
    if not busd:
        return render_template('404.html'), 404
    return render_template('change.html', busd=busd)

# Booking details page,  options for update or delete
@app.route('/updel/<int:bookid>', methods=["GET", "POST"])
def updel(bookid):
    if request.method == "POST":
        req = request.form['op']
        if req == "update":
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (bookid,))
            busd = cursor.fetchall()
            seat = busd[0]['passengers']
            seats = [i for i in range(1, seat + 1)]
            conn.close()
            return render_template("updateBooking.html", busd=busd, seats=seats)
        else:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (bookid,))
            busd = cursor.fetchall()
            busid = busd[0]['busid']
            passengers = busd[0]['passengers']
            update_bus_passengers(busid, -passengers)
            delete(bookid)
            conn.close()
            return render_template("deleted.html")

# Booking update page
@app.route('/updatebook/<int:bookid>', methods=["GET", "POST"])
def updatebook(bookid):
    if request.method == "POST":
        name = request.form['name']
        phno = request.form['phno']
        email = request.form['email']
        passengers = request.form['passengers']
        user_new_details = [name, phno, email]
        booking_new_details = [passengers]
        busd = booking_details(bookid)
        busid = busd[0]['busid']
        oldpassengers = busd[0]['passengers']
        updatebookuser(user_new_details, booking_new_details, bookid)
        new_passengers = int(passengers) - oldpassengers
        update_bus_passengers(busid, new_passengers)
    return render_template("updated.html")

# Returns all bus details
@app.route('/search/<from12>/<to12>')
def search(from12, to12):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE to_ = ? AND from_ = ?", (to12, from12,))
    details = cursor.fetchall()
    conn.close()
    return render_template('search.html', det=details)

# Page for booking
@app.route('/book/<int:busid>')
def book(busid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE busid = ?", (busid,))
    busd = cursor.fetchall()
    seat = busd[0]['capacity']
    seats = [i for i in range(1, seat + 1)]
    conn.close()
    return render_template('book.html', busd=busd, seats=seats)

# Booking a ticket
@app.route('/booked/<int:busid>', methods=["GET", "POST"])
def booked(busid):
    if request.method == "POST":
        name = request.form['name']
        phno = request.form['phno']
        email = request.form['email']
        passengers = request.form['passengers']
        userid = generateid()
        bookingid = generateid()
        update_bus_passengers(busid, passengers)
        user_details = [userid, name, phno, email, bookingid]
        booking_details = [bookingid, userid, busid, passengers]
        userinsert(user_details)
        bookinginsert(booking_details)
    return render_template('booked.html', id=bookingid)

if __name__ == '__main__':
    create_tables()  
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlQueries import update_bus_passengers, delete, booking_details, updatebookuser, generateid, userinsert, bookinginsert

app = Flask(__name__)

# Connection to SQLite database
def connect_db():
    conn = sqlite3.connect('projectdb.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# Create the tables in SQLite database
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Create bus table
    cursor.execute('''CREATE TABLE IF NOT EXISTS bus (
                        busid INTEGER PRIMARY KEY,
                        to_ TEXT,
                        from_ TEXT,
                        capacity INTEGER
                    )''')

    # Create user table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                        userid INTEGER PRIMARY KEY,
                        username TEXT,
                        phone TEXT,
                        email TEXT,
                        bookid INTEGER
                    )''')

    # Create booking table
    cursor.execute('''CREATE TABLE IF NOT EXISTS booking (
                        booking_id INTEGER PRIMARY KEY,
                        userid INTEGER,
                        busid INTEGER,
                        passengers INTEGER,
                        FOREIGN KEY (userid) REFERENCES user(userid),
                        FOREIGN KEY (busid) REFERENCES bus(busid)
                    )''')

    conn.commit()
    conn.close()

# Custom error handler for when origin and destination are the same
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Search Page
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from12 = request.form['from']
        to12 = request.form['to']
        if from12 == to12:
            return render_template('404.html'), 404
        else:
            return redirect(f"/search/{from12}/{to12}")
    return render_template('index.html')

# Search bar for updating
@app.route('/update', methods=["GET", "POST"])
def update():
    if request.method == "POST":
        id = request.form['id']
        return redirect(f"/change/{id}")
    return render_template('update.html')

# Update Page
@app.route('/change/<id>')
def change(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (id,))
    busd = cursor.fetchall()
    conn.close()
    if not busd:
        return render_template('404.html'), 404
    return render_template('change.html', busd=busd)

# Booking details page, here we got an option for update or delete
@app.route('/updel/<int:bookid>', methods=["GET", "POST"])
def updel(bookid):
    if request.method == "POST":
        req = request.form['op']
        if req == "update":
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (bookid,))
            busd = cursor.fetchall()
            seat = busd[0]['passengers']
            seats = [i for i in range(1, seat + 1)]
            conn.close()
            return render_template("updateBooking.html", busd=busd, seats=seats)
        else:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (bookid,))
            busd = cursor.fetchall()
            busid = busd[0]['busid']
            passengers = busd[0]['passengers']
            update_bus_passengers(busid, -passengers)
            delete(bookid)
            conn.close()
            return render_template("deleted.html")

# Booking update page
@app.route('/updatebook/<int:bookid>', methods=["GET", "POST"])
def updatebook(bookid):
    if request.method == "POST":
        name = request.form['name']
        phno = request.form['phno']
        email = request.form['email']
        passengers = request.form['passengers']
        user_new_details = [name, phno, email]
        booking_new_details = [passengers]
        busd = booking_details(bookid)
        busid = busd[0]['busid']
        oldpassengers = busd[0]['passengers']
        updatebookuser(user_new_details, booking_new_details, bookid)
        new_passengers = int(passengers) - oldpassengers
        update_bus_passengers(busid, new_passengers)
    return render_template("updated.html")

# Returns all bus details
@app.route('/search/<from12>/<to12>')
def search(from12, to12):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE to_ = ? AND from_ = ?", (to12, from12,))
    details = cursor.fetchall()
    conn.close()
    return render_template('search.html', det=details)

# Page for booking
@app.route('/book/<int:busid>')
def book(busid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE busid = ?", (busid,))
    busd = cursor.fetchall()
    seat = busd[0]['capacity']
    seats = [i for i in range(1, seat + 1)]
    conn.close()
    return render_template('book.html', busd=busd, seats=seats)

# Booking a ticket
@app.route('/booked/<int:busid>', methods=["GET", "POST"])
def booked(busid):
    if request.method == "POST":
        name = request.form['name']
        phno = request.form['phno']
        email = request.form['email']
        passengers = request.form['passengers']
        userid = generateid()
        bookingid = generateid()
        update_bus_passengers(busid, passengers)
        user_details = [userid, name, phno, email, bookingid]
        booking_details = [bookingid, userid, busid, passengers]
        userinsert(user_details)
        bookinginsert(booking_details)
    return render_template('booked.html', id=bookingid)

if __name__ == '__main__':
    create_tables()  
    app.run(debug=True)
