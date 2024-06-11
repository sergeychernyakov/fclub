// Specific code related to stadium operations

document.addEventListener('DOMContentLoaded', () => {
    fetchGamesList();
});

function selectSector(sector, price) {
  document.getElementById('price').textContent = `Цена билета: ${price} руб.`;
  document.getElementById('selectedSector').value = sector;
}

function closeModal() {
  const modal = document.getElementById('ticketModal');
  modal.style.display = 'none';
}
