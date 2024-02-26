document.addEventListener('DOMContentLoaded', function() {
    // Existing code for nav menu interactions
    var hamburgerMenu = document.querySelector('.hamburger-menu');
    var navMenu = document.querySelector('.nav-menu');

    hamburgerMenu.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    var navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });

    document.addEventListener('click', function(e) {
        if (!navMenu.contains(e.target) && !hamburgerMenu.contains(e.target)) {
            navMenu.classList.remove('active');
        }
    });

    // floating button and popup interactions
    const recommendationBtn = document.getElementById('teamrecommendationBtn');
    const teamRecommendationPopup = document.getElementById('teamRecommendationPopup');
    const closeBtn = document.querySelector('.close-btn');
    const teammateIcons = document.querySelectorAll('.teammate-icon');

    recommendationBtn.onclick = function() {
        teamRecommendationPopup.style.display = 'block';
    };

    closeBtn.onclick = function() {
        teamRecommendationPopup.style.display = 'none';
    };

    teammateIcons.forEach(icon => {
        icon.onclick = function() {
            const member = this.getAttribute('data-member');
            const memberName = document.getElementById('memberName');
        };
    });

    window.onclick = function(event) {
        if (event.target === teamRecommendationPopup) {
            teamRecommendationPopup.style.display = 'none';
        }
    };
});

//Recommendation Table
const buttonItems = document.querySelectorAll('.btn-list')
const buttonListTables = document.querySelectorAll('.table-list');
//select table content
function selectTable(e) {
    removeTable();
    //grab table from DOM
    const buttonListTable = document.querySelector(`#table-${this.id}`);
    //add table class
    buttonListTable.classList.add('show-table');
}
function removeTable() {
    buttonListTables.forEach(item => item.classList.remove('show-table'))
}
//listen for button click
buttonItems.forEach(item => item.addEventListener('click', selectTable))

