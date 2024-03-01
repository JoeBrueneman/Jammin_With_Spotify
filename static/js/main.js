document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetClass = this.getAttribute('href').substring(1); 
            const targetSection = document.querySelector('.' + targetClass); 
            if (targetSection) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight; 
                const offsetPosition = targetSection.getBoundingClientRect().top + window.scrollY - navbarHeight; 
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // Explore button functionality (if applicable)
    const exploreButton = document.querySelector('.showcase .btn');
    if (exploreButton) {
        exploreButton.addEventListener('click', function(e) {
            e.preventDefault();
            const searchSection = document.querySelector('.search');
            searchSection.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Tab functionality
    function openTab(event, modelName) {
        let tabcontent, tablinks;
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
    window.openTab = openTab;

    // Automatically open the first tab on page load
    const firstTab = document.querySelector('.tab-links');
    if (firstTab) {
        firstTab.click();
    }

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
    

