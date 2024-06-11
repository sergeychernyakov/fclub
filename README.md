# FClub

## Description
Веб-приложение для футбольного клуба с применением СУБД SQLite. Приложение включает в себя функции регистрации и авторизации пользователей, страницу администратора для управления матчами, функцию покупки билетов на матчи, симуляцию матчей с последующим обновлением турнирной таблицы, а также страницу пользователя для просмотра расписания матчей.

### Features
- Регистрация и авторизация пользователей
- Страница администратора для добавления новых матчей и симуляции матчей
- Страница пользователя для просмотра расписания матчей
- Покупка билетов на матчи
- Обновление турнирной таблицы на основе результатов матчей

## Technologies Used
- **Python 3**: Core programming language.
- **Flask**: Web framework used to create the web application.
- **SQLite**: Database management system used for storing data.

## Setup
To set up the app locally, follow these steps:

1. Clone the repository to your local machine.
    ```sh
    git clone git@github.com:sergeychernyakov/fclub.git
    ```
2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```
3. Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```
4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
5. Set environment variables:
    ```sh
    export FLASK_APP=run.py
    export FLASK_ENV=development
    ```

### Running the App
To run the application, execute:
    ```sh
    flask run
    ```

### Author
Sergey Chernyakov
