let canSelectSeat = true;
let selectedGameId = null;

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

                    const buyTicketButton = document.createElement('button');
                    buyTicketButton.textContent = 'К покупке билетов';
                    buyTicketButton.addEventListener('click', () => {
                        openModal(game.id);
                    });

                    // Append button to list item
                    listItem.appendChild(buyTicketButton);

                    gamesList.appendChild(listItem);
                });
            } else {
                gamesList.innerHTML = '<li>Нет доступных игр</li>';
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

function openModal(gameId) {
    selectedGameId = gameId;
    const modal = document.getElementById('ticketModal');
    const stadium = document.getElementById('stadium');
    stadium.innerHTML = '';
    fetchPurchasedSeats(gameId).then(purchasedSeats => {
        for (let i = 0; i < 4; i++) {
            const seat = document.createElement('div');
            seat.className = 'seat left';
            if (purchasedSeats.includes(`left-${i}`)) {
                seat.classList.add('purchased');
            }
            seat.dataset.seatId = `left-${i}`;
            seat.onclick = () => toggleSeatColor(seat);
            stadium.appendChild(seat);
        }
        for (let i = 0; i < 4; i++) {
            const seat = document.createElement('div');
            seat.className = 'seat right';
            if (purchasedSeats.includes(`right-${i}`)) {
                seat.classList.add('purchased');
            }
            seat.dataset.seatId = `right-${i}`;
            seat.onclick = () => toggleSeatColor(seat);
            stadium.appendChild(seat);
        }
    });
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('ticketModal');
    modal.style.display = 'none';
}

function fetchPurchasedSeats(gameId) {
    return fetch('/get_purchased_seats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ game_id: gameId })
    })
    .then(response => response.json())
    .then(data => data.seats || [])
    .catch(error => {
        console.error('Ошибка:', error);
        return [];
    });
}

function toggleSeatColor(seat) {
    if (!canSelectSeat) {
        showMessage('Вы не можете выбрать два места одновременно.');
        return;
    }
    if (seat.classList.contains('purchased')) {
        showMessage('Это место уже куплено!');
        return;
    }
    const redSeats = document.querySelectorAll('.seat.red');
    if (redSeats.length >= 1) {
        canSelectSeat = false;
        setTimeout(() => {
            canSelectSeat = true;
        }, 2000);
        showMessage('Вы не можете выбрать два места одновременно.');
        return;
    }
    seat.classList.toggle('red');
}

function buyTicket() {
    const selectedSeat = document.querySelector('.seat.red');
    if (!selectedSeat) {
        showMessage('Пожалуйста, выберите место перед покупкой.');
        return;
    }
    fetch('/buy_seat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: selectedGameId,
            seat: selectedSeat.dataset.seatId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Билет успешно куплен') {
            selectedSeat.classList.add('purchased');
            selectedSeat.classList.remove('red');
            showMessage('Билет куплен!');
        } else {
            showMessage('Ошибка покупки билета: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showMessage('Ошибка покупки билета');
    });
}

function showMessage(text) {
    const message = document.getElementById('message');
    message.textContent = text;
    message.style.display = 'block';
    setTimeout(() => {
        message.style.display = 'none';
    }, 2000);
}
