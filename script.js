
const filterButtons = document.querySelectorAll(".filter-btn");
const projectCards = document.querySelectorAll(".project-card");

filterButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const selectedFilter = button.dataset.filter;

        filterButtons.forEach(function (btn) {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        projectCards.forEach(function (card) {
            const category = card.dataset.category;

            if (selectedFilter === "all" || category === selectedFilter) {
                card.hidden = false;
            } else {
                card.hidden = true;
            }
        });
    });
});
