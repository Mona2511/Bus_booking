from flask import Flask, render_template, redirect, request

app = Flask(__name__, template_folder="../templates")
app.secret_key = "secret123"

users = []

buses = [
    {"id": 1, "name": "Express", "price": 500, "time": "10:00 AM", "from": "Ahmedabad", "to": "Surat"},
    {"id": 2, "name": "Super Fast", "price": 300, "time": "2:00 PM", "from": "Ahmedabad", "to": "Vadodara"},
    {"id": 3, "name": "Luxury", "price": 800, "time": "6:00 PM", "from": "Ahmedabad", "to": "Rajkot"}
]

seats = [[0 for _ in range(4)] for _ in range(5)]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users.append({
            "username": request.form['username'],
            "password": request.form['password']
        })
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        for user in users:
            if user['username'] == request.form['username'] and user['password'] == request.form['password']:
                return redirect('/dashboard')
        return "Invalid login"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/buses')
def buses_page():
    return render_template('buses.html', buses=buses)

@app.route('/seats', methods=['GET', 'POST'])
def seats_page():
    global seats
    if request.method == 'POST':
        r = int(request.form['row'])
        c = int(request.form['col'])

        if seats[r][c] == 0:
            seats[r][c] = 1
            return "Seat booked"
        else:
            return "Already booked"

    return render_template('seats.html', seats=seats)

# ✅ REQUIRED for Vercel
app.debug = False
