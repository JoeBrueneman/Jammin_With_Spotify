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
    
    // Floating button to show popup
    const recommendationBtn = document.getElementById('teamrecommendationBtn');
    const teamRecommendationPopup = document.getElementById('teamRecommendationPopup');
        
    // Close button inside the popup
    const closeBtn = document.querySelector('.close-btn');
        
    // Team member buttons
    const memberButtons = document.querySelectorAll('.teammate-icon');
        
    // Contents for each team member
    const allWrappedContents = document.querySelectorAll('.wrapped-content');
        
    // Open popup
    recommendationBtn.addEventListener('click', function() {
        teamRecommendationPopup.style.display = 'block';
    });
        
    // Close popup
    closeBtn.addEventListener('click', function() {
        teamRecommendationPopup.style.display = 'none';
    });
        
    // Close popup when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === teamRecommendationPopup) {
            teamRecommendationPopup.style.display = 'none';
        }
    });
        
    // Show recommendation content for each member
    memberButtons.forEach(button => {
        button.addEventListener('click', function() {
    
    // Hide all content
    allWrappedContents.forEach(content => {
        content.classList.add('hidden');
        content.classList.remove('show-wrapped');
    });
    
    // Show the clicked member's content
    const contentId = `recommendations-${this.dataset.member}`;
    const contentToShow = document.getElementById(contentId);
    contentToShow.classList.remove('hidden');
    contentToShow.classList.add('show-wrapped'); // Add class to display the content
    });
    });
});
    

