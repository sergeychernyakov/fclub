from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
from flask_session import Session

app = Flask(App)
app.secret_key = os.urandom(24)

# Configuration for Flask-Session
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = 'sqlite:///db/session.db'
Session(app)

DATABASE_PATH = 'db/football_club.db'

def record_score(team1: str, team2: str, score1: int, score2: int) -> None:
    """
    Record the score of a game and update team points.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO teams (name) VALUES (?)", (team1,))
    cursor.execute("INSERT OR IGNORE INTO teams (name) VALUES (?)", (team2,))

    if score1 > score2:
        cursor.execute("UPDATE teams SET points = points + 3 WHERE name = ?", (team1,))
    elif score1 < score2:
        cursor.execute("UPDATE teams SET points = points + 3 WHERE name = ?", (team2,))
    else:
        cursor.execute("UPDATE teams SET points = points + 1 WHERE name = ?", (team1,))
        cursor.execute("UPDATE teams SET points = points + 1 WHERE name = ?", (team2,))

    conn.commit()
    conn.close()

def get_teams() -> list:
    """
    Retrieve a list of teams ordered by points.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teams ORDER BY points DESC")
    teams = cursor.fetchall()
    conn.close()
    return teams

def add_game(team1: str, team2: str, date: str, time: str) -> None:
    """
    Add a game to the games table.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (team1, team2, date, time) VALUES (?, ?, ?, ?)", (team1, team2, date, time))
    conn.commit()
    conn.close()

def get_games() -> list:
    """
    Retrieve a list of all games.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    conn.close()
    return games

def add_seat(game_id: int, seat: str) -> None:
    """
    Add a purchased seat to the seats table.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO seats (game_id, seat, purchased) VALUES (?, ?, 1)", (game_id, seat))
    conn.commit()
    conn.close()

def get_purchased_seats(game_id: int) -> list:
    """
    Retrieve a list of purchased seats for a given game.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT seat FROM seats WHERE game_id=? AND purchased=1", (game_id,))
    seats = [row[0] for row in cursor.fetchall()]
    conn.close()
    return seats

def authenticate_user(email: str, password: str) -> tuple:
    """
    Authenticate a user by email and password.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate_admin(email: str, password: str) -> tuple:
    """
    Authenticate an admin by email and password.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE email=? AND password=?", (email, password))
    admin = cursor.fetchone()
    conn.close()
    return admin

def buy_seat(game_id: int, sector: str, row: int, seat: int, price: float) -> None:
    """
    Register the purchase of a seat for a game.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO seats (game_id, sector, row, seat, price) VALUES (?, ?, ?, ?, ?)",
                   (game_id, sector, row, seat, price))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)
        if user:
            session['email'] = email
            return redirect('/users')
        else:
            admin = authenticate_admin(email, password)
            if admin:
                session['email'] = email
                return redirect('/admin')
            else:
                return render_template('login.html', message='Неверный адрес электронной почты или пароль')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return redirect('/')
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', message='Пользователь с таким адресом электронной почты уже существует')
    return render_template('register.html')

@app.route('/admin')
def admin():
    if 'email' in session:
        return render_template('admin.html')
    return redirect('/')

@app.route('/users')
def users():
    if 'email' in session:
        return render_template('users.html')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

@app.route('/add_game', methods=['POST'])
def add_game_route():
    if 'email' in session:
        if request.method == 'POST':
            data = request.json
            team1 = data.get('team1')
            team2 = data.get('team2')
            date = data.get('date')
            time = data.get('time')
            if team1 and team2 and date and time:
                add_game(team1, team2, date, time)
                return jsonify({'message': 'Игра была добавлена'}), 200
            else:
                return jsonify({'message': 'Отсутствующие данные'}), 400
    return jsonify({'message': 'Неавторизован'}), 401

@app.route('/get_games')
def get_games_route():
    if 'email' in session:
        games = get_games()
        games_list = []
        for game in games:
            games_list.append({
                'id': game[0],
                'team1': game[1],
                'team2': game[2],
                'date': game[3],
                'time': game[4]
            })
        return jsonify({'games': games_list}), 200
    return jsonify({'message': 'Неавторизован'}), 401

@app.route('/get_purchased_seats', methods=['POST'])
def get_purchased_seats_route():
    if 'email' in session:
        if request.method == 'POST':
            game_id = request.json.get('game_id')
            if game_id:
                seats = get_purchased_seats(game_id)
                return jsonify({'seats': seats}), 200
            else:
                return jsonify({'message': 'Отсутствующие данные'}), 400
    return jsonify({'message': 'Неавторизован'}), 401

@app.route('/buy_seat', methods=['POST'])
def buy_seat_route():
    if 'email' in session:
        if request.method == 'POST':
            data = request.json
            game_id = data.get('game_id')
            sector = data.get('sector')
            row = data.get('row')
            seat = data.get('seat')
            price = data.get('price')
            if game_id and sector and row and seat and price:
                buy_seat(game_id, sector, row, seat, price)
                return jsonify({'message': 'Билет успешно куплен'}), 200
            else:
                return jsonify({'message': 'Отсутствующие данные'}), 400
    return jsonify({'message': 'Неавторизован'}), 401

@app.route('/get_admin')
def get_admin_route():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM admins")
    admin_count = cursor.fetchone()[0]
    conn.close()
    return jsonify({'adminExists': admin_count > 0})

if __name__ == '__main__':
    app.run(debug=True)
