from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# ---------------- DATA STRUCTURES ----------------

# 🚌 Bus Data (List of Dictionaries)
buses = [
    {"id": 1, "name": "Express", "price": 500, "time": "10:00 AM", "from": "Ahmedabad", "to": "Surat"},
    {"id": 2, "name": "Super Fast", "price": 300, "time": "2:00 PM", "from": "Ahmedabad", "to": "Vadodara"},
    {"id": 3, "name": "Luxury", "price": 800, "time": "6:00 PM", "from": "Ahmedabad", "to": "Rajkot"}
]

# 💺 Seat Matrix (2D Array)
seats = [[0 for _ in range(4)] for _ in range(5)]

# ---------------- ROUTES ----------------

# 🏠 Home
@app.route('/')
def home():
    return render_template('index.html')


# 📝 Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            return "User already exists!"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')


# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid username or password!"

    return render_template('login.html')


# 📊 Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# 🚌 View Buses
@app.route('/buses')
def buses_page():
    return render_template('buses.html', buses=buses)


# 💺 Seat Booking Page
@app.route('/seats', methods=['GET', 'POST'])
def seats_page():
    global seats

    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])

        if seats[row][col] == 0:
            seats[row][col] = 1
            return "✅ Seat Booked Successfully"
        else:
            return "❌ Seat Already Booked"

    return render_template('seats.html', seats=seats)


# ▶️ RUN APP
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # create database tables

    app.run(debug=True)