lucide.createIcons();

const swiper = new Swiper('.swiper-container', {
  slidesPerView: 1,
  spaceBetween: 30,
  loop: true,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  breakpoints: {
    640: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});

function toggleModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.toggle('active');
}

window.onclick = function(event) {
  const modals = document.getElementsByClassName('modal');
  for (const modal of modals) {
    if (event.target === modal) {
      modal.classList.remove('active');
    }
  }
}

function navigateToCourse(course) {
  alert(`Navigating to ${course.toUpperCase()} course page`);
}
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});
function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
  }
