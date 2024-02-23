document.addEventListener('DOMContentLoaded', function() {
    // Target the hamburger icon
    const hamburger = document.querySelector('.hamburger-menu');
    // Target the navigation menu
    const navMenu = document.querySelector('.nav-menu');

// Listen for hamburger menu click
hamburger.addEventListener('click', () => {
    console.log("Hamburger clicked");
    sidebar.classList.toggle('active-navbar');
});

    // Close the nav-menu when a link is clicked (useful for single-page applications)
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });

    /* Footer */
footer {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    background: #e50914;
    height: 190px;
    padding: 20px 50px;
    flex-direction: column;
}

footer .icons,
footer .menu {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px 0;
    flex-wrap: wrap;
}

footer .icons li,
footer .menu li {
    list-style: none;
}

footer .icons li a {
    font-size: 2em;
    color: #141414;
    margin: 0 10px;
    display: inline-block;
    transition: 0.5s;
}

footer .icons li a:hover {
    transform: translateY(-10px);
}

footer .menu li a {
    font-size: 1.2 rem;
    color: #fff;
    margin: 0 10px;
    display: inline-block;
    text-decoration: none;
    opacity: 0.75;
    transition: 0.5s;
}

footer .menu li a:hover {
    opacity: 1;
}
footer p {
    color: #fff;
    text-align: center;
    margin-top: 15px;
    margin-bottom: 10px;
    font-size: 1em;
    opacity: 0.75;
}
