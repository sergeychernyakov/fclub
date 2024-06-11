# FClub


## Description
сайт на flask

Веб-приложение для футбольного клуба с применением СУБД Mysql
Ннужно реализовать функцию покупки билетов на матчи и функцию симуляции (проигрывания) футбольных матчей с последующим обновлением турнирной таблицы с сортировкой по набранным очкам команд
там что- то начато, но на сайте пока все что есть: окна регистрации и авторизации, страница администратора где можно добавлять новые матчи и страница пользователя где можно только смотреть расписание матчей, которые администратор опубликовал

### Features

## Technologies Used
- **Python 3**: Core programming language.
- **Flask**: Web framework used to create the web application.

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
    export FLASK_RUN_PORT=5002
    export FLASK_ENV=development
    ```
### Configuratio
copy .env.example to .env
set OPENAI_API_KEY

### Running the App
    To run the application, execute:
    ```sh
    flask run
    ```

### Author
Sergey Chernyakov

### Ngrok
ngrok http 5002
