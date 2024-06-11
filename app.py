from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE_PATH = 'db/football_club.db'

def get_sold_tickets_count(game_id: int) -> int:
    """
    Retrieve the count of sold tickets for a given game.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM seats WHERE game_id=? AND purchased=1", (game_id,))
    sold_tickets = cursor.fetchone()[0]
    conn.close()
    return sold_tickets

def get_game_details() -> list:
    """
    Retrieve a list of games with the count of sold tickets.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, team1, team2, date, time FROM games")
    games = cursor.fetchall()
    game_details = []
    for game in games:
        game_id, team1, team2, date, time = game
        sold_tickets = get_sold_tickets_count(game_id)
        game_details.append({
            'id': game_id,
            'team1': team1,
            'team2': team2,
            'date': date,
            'time': time,
            'sold_tickets': sold_tickets
        })
    conn.close()
    return game_details

def get_teams_sorted_by_points() -> list:
    """
    Retrieve a list of teams sorted by points.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, points FROM teams ORDER BY points DESC")
    teams = cursor.fetchall()
    conn.close()
    return teams

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

def get_purchased_seats(game_id: int, sector: str) -> list:
    """
    Retrieve a list of purchased seats for a given game and sector.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT row, seat FROM seats WHERE game_id=? AND sector=? AND purchased=1", (game_id, sector))
    seats = [{'row': row, 'seat': seat} for row, seat in cursor.fetchall()]
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
    cursor.execute("INSERT INTO seats (game_id, sector, row, seat, price, purchased) VALUES (?, ?, ?, ?, ?, 1)",
                   (game_id, sector, row, seat, price))
    conn.commit()
    conn.close()

def simulate_game(game_id: int) -> None:
    """
    Simulate a game by randomly generating scores and updating team points.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT team1, team2 FROM games WHERE id=?", (game_id,))
    game = cursor.fetchone()
    if not game:
        conn.close()
        return
    
    team1, team2 = game
    score1 = random.randint(0, 5)
    score2 = random.randint(0, 5)
    
    record_score(team1, team2, score1, score2)
    
    cursor.execute("UPDATE games SET score1=?, score2=? WHERE id=?", (score1, score2, game_id))
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

@app.route('/get_games_with_tickets')
def get_games_with_tickets():
    if 'email' in session:
        games = get_game_details()
        return jsonify({'games': games}), 200
    return jsonify({'message': 'Неавторизован'}), 401

@app.route('/tournament')
def tournament():
    if 'email' in session:
        return render_template('tournament.html')
    return redirect('/')

@app.route('/get_teams')
def get_teams():
    if 'email' in session:
        teams = get_teams_sorted_by_points()
        return jsonify({'teams': teams}), 200
    return jsonify({'message': 'Неавторизован'}), 401

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
            sector = request.json.get('sector')
            if game_id and sector:
                seats = get_purchased_seats(game_id, sector)
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
                try:
                    buy_seat(game_id, sector, row, seat, price)
                    return jsonify({'message': 'Билет успешно куплен'}), 200
                except sqlite3.OperationalError as e:
                    return jsonify({'message': 'Ошибка базы данных: ' + str(e)}), 500
            else:
                return jsonify({'message': 'Отсутствующие данные'}), 400
    return jsonify({'message': 'Неавторизован'}), 401

@app.route('/simulate_game', methods=['POST'])
def simulate_game_route():
    if 'email' in session:
        game_id = request.json.get('game_id')
        if game_id:
            simulate_game(game_id)
            return jsonify({'message': 'Матч успешно симулирован'}), 200
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
