document.addEventListener('DOMContentLoaded', () => {
  fetchTeamsList();
});

function fetchTeamsList() {
  const teamsList = document.getElementById('teamsList');
  fetch('/get_teams')
      .then(response => response.json())
      .then(data => {
          console.log(data); // Добавлено для отладки
          teamsList.innerHTML = ''; // Очистим текущий список
          if (data.teams.length > 0) {
              data.teams.forEach(team => {
                  const listItem = document.createElement('tr');

                  const teamName = document.createElement('td');
                  teamName.textContent = team[0]; // Изменено для обработки массива
                  listItem.appendChild(teamName);

                  const teamPoints = document.createElement('td');
                  teamPoints.textContent = team[1]; // Изменено для обработки массива
                  listItem.appendChild(teamPoints);

                  teamsList.appendChild(listItem);
              });
          } else {
              teamsList.innerHTML = '<tr><td colspan="2">Нет данных о командах</td></tr>';
          }
      })
      .catch(error => console.error('Ошибка:', error));
}
