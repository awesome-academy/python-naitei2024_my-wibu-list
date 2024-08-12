document.addEventListener('DOMContentLoaded', () => {
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');
    const wrapper = document.querySelector('.carousel-wrapper');
    const slides = document.querySelectorAll('.carousel-slide');
    
    let currentIndex = 0;
    const slidesToShow = 6; 
    const totalSlides = slides.length;

    const slidesToMove = 1;
    
    function updateCarousel() {
        const offset = -currentIndex * (100 / slidesToShow);
        wrapper.style.transform = `translateX(${offset}%)`;
    }

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex -= slidesToMove;
        } else {
            currentIndex = totalSlides - slidesToShow;
        }
        updateCarousel();
    });

    nextButton.addEventListener('click', () => {
        if (currentIndex < totalSlides - slidesToShow) {
            currentIndex += slidesToMove;
        } else {
            currentIndex = 0;
        }
        updateCarousel();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    
    const prevButton = document.querySelector('.carousel-control-prev');
    const nextButton = document.querySelector('.carousel-control-next');
    const carouselInner = document.querySelector('.carousel-inner');
    const carouselItems = document.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.carousel-indicators button');

    let currentIndex = 0;

    
    function goToNextSlide() {
        carouselItems[currentIndex].classList.remove('active');
        indicators[currentIndex].classList.remove('active');

        currentIndex = (currentIndex + 1) % carouselItems.length;

        carouselItems[currentIndex].classList.add('active');
        indicators[currentIndex].classList.add('active');
    }

    
    function goToPrevSlide() {
        carouselItems[currentIndex].classList.remove('active');
        indicators[currentIndex].classList.remove('active');

        currentIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;

        carouselItems[currentIndex].classList.add('active');
        indicators[currentIndex].classList.add('active');
    }

    
    nextButton.addEventListener('click', function() {
        goToNextSlide();
    });

    
    prevButton.addEventListener('click', function() {
        goToPrevSlide();
    });

    
    setInterval(goToNextSlide, 5000); 
});
