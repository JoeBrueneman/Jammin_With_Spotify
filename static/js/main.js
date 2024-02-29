document.addEventListener('DOMContentLoaded', function() {
    // Nav menu interactions
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const navMenu = document.querySelector('.nav-menu');
    hamburgerMenu.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    // Close nav menu on link click
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = document.querySelector(this.getAttribute('href'));
            targetSection.scrollIntoView({ behavior: 'smooth' });
            navMenu.classList.remove('active');
        });
    });

    // Close nav menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!navMenu.contains(e.target) && !hamburgerMenu.contains(e.target)) {
            navMenu.classList.remove('active');
        }
    });

    // Explore button
    const exploreButton = document.querySelector('.showcase .btn');
    exploreButton.addEventListener('click', function(e) {
        e.preventDefault();
        const searchSection = document.querySelector('.search');
        searchSection.scrollIntoView({ behavior: 'smooth' });
    });

    // Tab functionality
    function openTab(event, modelName) {
        var tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tab-content");
        for (let i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tab-links");
        for (let i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(modelName).style.display = "block";
        event.currentTarget.className += " active";
    }
    window.openTab = openTab; // Make openTab available globally

    // Automatically open the first tab on page load
    document.querySelector('.tab-links').click();

    // Adjust audio volume
    const audios = document.querySelectorAll('audio');
    audios.forEach(function(audio) {
        audio.volume = 0.2;
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
    contentToShow.classList.add('show-wrapped'); 
    });
    });
});
    

