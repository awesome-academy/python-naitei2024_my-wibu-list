document.addEventListener('click', function(event) {
    const submenu = document.querySelectorAll('.submenu');
    submenu.forEach(menu => {
        if (!menu.contains(event.target) && !event.target.closest('li')) {
            menu.style.display = 'none';
        }
    });
});

document.querySelectorAll('nav ul li').forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.querySelector('.submenu').style.display = 'block';
    });

    item.addEventListener('mouseleave', () => {
        item.querySelector('.submenu').style.display = 'none';
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const prevButton = document.querySelector('.pagination .prev');
    const nextButton = document.querySelector('.pagination .next');
    const currentPage = document.querySelector('.pagination .current-page');
    
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            // Logic to go to the previous page
        });
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            // Logic to go to the next page
        });
    }
});

