let canSelectSeat = true;
let selectedGameId = null;
let selectedSeat = null; // Variable to keep track of the currently selected seat

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
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('ticketModal');
    modal.style.display = 'none';
}

function fetchPurchasedSeats(gameId, sector) {
    return fetch('/get_purchased_seats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ game_id: gameId, sector: sector })
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

function buyTicket(event) {
    event.preventDefault();
    const sector = document.getElementById('sector').value;
    const row = document.getElementById('row').value;
    const seat = document.getElementById('seat').value;
    const price = document.getElementById('price').value;

    if (!sector || !row || !seat || !price) {
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
            sector: sector,
            row: row,
            seat: seat,
            price: price
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Билет успешно куплен') {
            const selectedSeatDiv = document.querySelector(`.seat[data-row="${row}"][data-seat="${seat}"]`);
            if (selectedSeatDiv) {
                selectedSeatDiv.classList.add('purchased');
                selectedSeatDiv.classList.remove('red');
            }
            alert(`Билет куплен! Сектор: ${sector}, Ряд: ${row}, Место: ${seat}`);
            closeModal();
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

function showOverlay(sector, price) {
    document.getElementById('overlay' + sector).style.display = 'block';
    document.getElementById('price').innerText = 'Цена билета: ' + price + ' рублей';
}

function hideOverlay(sector) {
    document.getElementById('overlay' + sector).style.display = 'none';
}

function showSeats(sector, price) {
    fetchPurchasedSeats(selectedGameId, sector).then(purchasedSeats => {
        const seatsContainer = document.getElementById('seatsContainer');
        const selectedSectorDisplay = document.getElementById('selectedSectorDisplay');
        seatsContainer.innerHTML = ''; // Очистить текущие места
        selectedSectorDisplay.innerHTML = `<h3>Выбранный сектор: ${sector}</h3>`;
        document.getElementById('sector').value = sector;
        document.getElementById('price').value = price;

        for (let row = 1; row <= 7; row++) {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'seat-row';

            const rowLabelLeft = document.createElement('div');
            rowLabelLeft.className = 'row-label';
            rowLabelLeft.innerText = row;
            rowDiv.appendChild(rowLabelLeft);

            for (let seat = 1; seat <= 10; seat++) {
                const seatDiv = document.createElement('div');
                seatDiv.className = 'seat';
                seatDiv.innerText = seat;
                seatDiv.dataset.row = row;
                seatDiv.dataset.seat = seat;

                if (purchasedSeats.some(s => s.row === row && s.seat === seat)) {
                    seatDiv.classList.add('purchased');
                    seatDiv.onclick = null;
                } else {
                    seatDiv.onclick = () => selectSeat(row, seat);
                }

                rowDiv.appendChild(seatDiv);
            }

            const rowLabelRight = document.createElement('div');
            rowLabelRight.className = 'row-label';
            rowLabelRight.innerText = row;
            rowDiv.appendChild(rowLabelRight);

            seatsContainer.appendChild(rowDiv);
        }
    });
}

function selectSeat(row, seatNumber) {
    if (selectedSeat) {
        selectedSeat.classList.remove('selected');
    }
    selectedSeat = document.querySelector(`.seat[data-row="${row}"][data-seat="${seatNumber}"]`);
    selectedSeat.classList.add('selected');
    document.getElementById('row').value = row;
    document.getElementById('seat').value = seatNumber;
}
