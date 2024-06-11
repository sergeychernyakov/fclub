const addGameForm = document.getElementById("addGameForm");
const gamesList = document.getElementById("gamesList");
const adminSection = document.getElementById("adminSection");
const gameManagementSection = document.getElementById("gameManagementSection");

addGameForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch("/add_game", {
        method: "POST",
        body: JSON.stringify(Object.fromEntries(formData.entries())),
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((data) => {
        alert(data.message);
        this.reset();
        fetchGamesList();
    })
    .catch((error) => console.error("Ошибка:", error));
});

document.addEventListener('DOMContentLoaded', () => {
    fetchGamesList();
});

function fetchGamesList() {
    const gamesList = document.getElementById('gamesList');
    fetch('/get_games')
        .then(response => response.json())
        .then(data => {
            gamesList.innerHTML = '';
            if (data.games.length > 0) {
                data.games.forEach(game => {
                    const listItem = document.createElement('li');

                    // Create a container for the game info and button
                    const gameInfoContainer = document.createElement('div');
                    gameInfoContainer.textContent = `${game.team1} - ${game.team2}  (Дата: ${game.date}, Время: ${game.time})`;
                    listItem.appendChild(gameInfoContainer);

                    gamesList.appendChild(listItem);
                });
            } else {
                gamesList.innerHTML = '<li>Нет доступных игр</li>';
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

fetch("/get_admin")
    .then((response) => response.json())
    .then((data) => {
        if (data.adminExists) {
            adminSection.style.display = "block";
        } else {
            adminSection.style.display = "none";
        }
    })
    .catch((error) => console.error("Ошибка:", error));
