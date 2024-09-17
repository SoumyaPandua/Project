document.addEventListener('DOMContentLoaded', function () {
    const table = document.getElementById('productTable');
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const rowsPerPage = 5;
    let currentPage = 1;

    function displayRows(page) {
      const start = (page - 1) * rowsPerPage;
      const end = start + rowsPerPage;

      rows.forEach((row, index) => {
        row.style.display = index >= start && index < end ? '' : 'none';
      });
    }

    function updatePaginationControls() {
      const totalPages = Math.ceil(rows.length / rowsPerPage);
      document.getElementById('firstPage').disabled = currentPage === 1;
      document.getElementById('prevPage').disabled = currentPage === 1;
      document.getElementById('nextPage').disabled = currentPage === totalPages;
      document.getElementById('lastPage').disabled = currentPage === totalPages;
    }

    document.getElementById('firstPage').addEventListener('click', () => {
      currentPage = 1;
      displayRows(currentPage);
      updatePaginationControls();
    });

    document.getElementById('prevPage').addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage--;
        displayRows(currentPage);
        updatePaginationControls();
      }
    });

    document.getElementById('nextPage').addEventListener('click', () => {
      const totalPages = Math.ceil(rows.length / rowsPerPage);
      if (currentPage < totalPages) {
        currentPage++;
        displayRows(currentPage);
        updatePaginationControls();
      }
    });

    document.getElementById('lastPage').addEventListener('click', () => {
      currentPage = Math.ceil(rows.length / rowsPerPage);
      displayRows(currentPage);
      updatePaginationControls();
    });

    displayRows(currentPage);
    updatePaginationControls();
  });

  const hamBurger = document.querySelector(".toggle-btn");
    hamBurger.addEventListener("click", function () {
        document.querySelector("#sidebar").classList.toggle("expand");
    });