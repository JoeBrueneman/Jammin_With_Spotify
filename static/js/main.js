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
    
    // Floating button and popup interactions
    const recommendationBtn = document.getElementById('teamrecommendationBtn');
    const teamRecommendationPopup = document.getElementById('teamRecommendationPopup');
    const closeBtn = document.querySelector('.close-btn');
    
    // Show the popup when the floating button is clicked
    recommendationBtn.onclick = function() {
        teamRecommendationPopup.style.display = 'block';
    };
    
    // Hide the popup when the close button is clicked
    closeBtn.onclick = function() {
        teamRecommendationPopup.style.display = 'none';
    };
    
    // Hide the popup when clicking outside of it
    window.onclick = function(event) {
        if (event.target === teamRecommendationPopup) {
            teamRecommendationPopup.style.display = 'none';
        }
    };
    
    // Recommendation Table interactions
    const buttonItems = document.querySelectorAll('.btn-list');
    const buttonListTables = document.querySelectorAll('.table-list');
    
    // Function to show the selected table and hide others
    function selectTable(e) {
    // First, remove 'show-table' class from all tables to hide them
    buttonListTables.forEach(item => {
        item.style.display = 'none'; // Use display:none to hide
        });
    
    // Add 'show-table' class to the clicked member's table to show it
    const buttonListTable = document.querySelector(`#table-${this.id}`);
        buttonListTable.style.display = 'block'; // Use display:block to show
    }
    
    // Add click event listener to each team member's button
    buttonItems.forEach(item => {
        item.addEventListener('click', selectTable);
    });
});
    

