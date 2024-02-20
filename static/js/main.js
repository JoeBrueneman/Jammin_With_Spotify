document.addEventListener('DOMContentLoaded', () => {
    // Handle click events on sidebar navigation items
    const navItems = document.querySelectorAll('.sidebar .navigation ul li a');
    const subMenus = document.querySelectorAll('.sidebar .navigation ul .submenu');

    navItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            const parentLi = item.parentElement;

            // Collapse all submenus when a non-expandable item is clicked
            if (!parentLi.classList.contains('expandable')) {
                subMenus.forEach(subMenu => {
                    subMenu.style.display = 'none';
                });
            }

            // Handle expandable items to toggle submenus
            if (item.nextElementSibling && item.nextElementSibling.classList.contains('submenu')) {
                const submenu = item.nextElementSibling;
                submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
            }

            // Set active state
            navItems.forEach(nav => {
                nav.parentElement.classList.remove('active');
            });
            parentLi.classList.add('active');
            
            // Load the content related to the clicked item
            // This is where you would add the content loading logic
            // loadContent(item.getAttribute('href').substring(1)); // Implement loadContent function based on your needs
        });
    });

    // Function to load content based on the section identifier (e.g., "home", "search", etc.)
    function loadContent(sectionId) {
        // Example content loading logic (you would expand this to load actual content)
        console.log('Loading content for section:', sectionId);
        // Placeholder logic to show how you might load content
        const contentArea = document.querySelector('.main-container .content-area');
        contentArea.innerHTML = `<div>Loading content for ${sectionId}...</div>`;
    }
});
