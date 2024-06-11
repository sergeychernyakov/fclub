document.addEventListener('DOMContentLoaded', () => {
    fetchGamesList();

    const addGameForm = document.getElementById('addGameForm');
    addGameForm.addEventListener('submit', function(event) {
        event.preventDefault();
        addNewGame();
    });
});

function fetchGamesList() {
    const gamesList = document.getElementById('gamesList');
    fetch('/get_games_with_tickets')
        .then(response => response.json())
        .then(data => {
            gamesList.innerHTML = '';
            if (data.games.length > 0) {
                data.games.forEach(game => {
                    const listItem = document.createElement('li');

                    // Create a container for the game info
                    const gameInfoContainer = document.createElement('div');
                    gameInfoContainer.className = 'game-info';
                    gameInfoContainer.innerHTML = `
                        <div>
                            <strong>${game.team1} - ${game.team2}</strong>
                            <br>
                            Дата: ${game.date}, Время: ${game.time}
                            <br>
                            Продано билетов: ${game.sold_tickets}
                        </div>
                    `;
                    listItem.appendChild(gameInfoContainer);

                    // Create simulate button
                    const simulateButton = document.createElement('button');
                    simulateButton.className = 'simulate-button';
                    simulateButton.textContent = 'Симулировать матч';
                    simulateButton.addEventListener('click', () => {
                        simulateGame(game.id);
                    });
                    listItem.appendChild(simulateButton);

                    gamesList.appendChild(listItem);
                });
            } else {
                gamesList.innerHTML = '<li>Нет доступных игр</li>';
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

function addNewGame() {
    const team1 = document.getElementById('team1').value;
    const team2 = document.getElementById('team2').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    fetch('/add_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ team1, team2, date, time })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Игра была добавлена') {
            alert('Игра добавлена успешно');
            fetchGamesList();
        } else {
            alert('Ошибка при добавлении игры: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при добавлении игры');
    });
}

function simulateGame(gameId) {
    fetch('/simulate_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ game_id: gameId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Матч успешно симулирован') {
            alert('Матч успешно симулирован');
            fetchGamesList();
        } else {
            alert('Ошибка симуляции матча: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка симуляции матча');
    });
}
