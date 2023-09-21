// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  const professionalCards = document.querySelectorAll('.news-card'); // Update the selector to target the professional cards

  // Search functionality
  const searchInput = document.getElementById("search-input");
  const searchButton = document.getElementById("search-button");

  searchButton.addEventListener("click", function () {
    searchProfessionals();
  });

  searchInput.addEventListener("input", function (event) {
    if (event.inputType === "insertText" || event.inputType === "deleteContentBackward") {
      searchProfessionals();
    }
  });

  function searchProfessionals() {
    const searchQuery = searchInput.value.trim().toLowerCase();

    professionalCards.forEach((card) => {
      const professionalName = card.querySelector(".news-card__title").textContent.toLowerCase(); // Update the selector
      const serviceType = card.querySelector(".news-card__excerpt").textContent.toLowerCase(); // Update the selector
      const isVisible =
        professionalName.includes(searchQuery) || serviceType.includes(searchQuery);
      card.style.display = isVisible ? "block" : "none";
    });
  }

  // Rest of your existing code here
});
