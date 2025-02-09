lucide.createIcons();

function toggleMenu() {
  const mobileMenu = document.getElementById('mobileMenu');
  const menuIcon = document.getElementById('menuIcon');
  const closeIcon = document.getElementById('closeIcon');
  
  mobileMenu.classList.toggle('hidden');
  menuIcon.classList.toggle('hidden');
  closeIcon.classList.toggle('hidden');
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    const mobileMenu = document.getElementById('mobileMenu');
  
    if (section) { // Ensure section exists
      if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
        toggleMenu();
      }
      section.scrollIntoView({ behavior: 'smooth' });
    } else {
      console.warn(`Section with ID '${sectionId}' not found.`);
    }
  }
  

function openModal(modalId) {
  document.getElementById(modalId).classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.add('hidden');
  document.body.style.overflow = 'auto';
}

function switchForm(show, hide) {
  document.getElementById(show).classList.remove('hidden');
  document.getElementById(hide).classList.add('hidden');
}

window.onclick = function(event) {
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    if (event.target === modal) {
      closeModal(modal.id);
    }
  });
}

function toggleFaq(index) {
  const faqItems = document.querySelectorAll('.faq-item');
  const clickedItem = faqItems[index];
  const answer = clickedItem.querySelector('.faq-answer');
  const icon = clickedItem.querySelector('.faq-icon');
  
  faqItems.forEach((item, i) => {
    if (i !== index) {
      item.querySelector('.faq-answer').classList.remove('active');
      item.querySelector('.faq-icon').style.transform = 'rotate(0deg)';
    }
  });
  
  answer.classList.toggle('active');
  icon.style.transform = answer.classList.contains('active') ? 'rotate(180deg)' : 'rotate(0deg)';
}

function handleGoogleSignIn() {
  console.log('Google Sign In clicked');
}

function validatePassword(password, confirmPassword) {
  if (password !== confirmPassword) {
    return 'Passwords do not match';
  }
  if (password.length < 8) {
    return 'Password must be at least 8 characters long';
  }
  return null;
}

function validatePhone(phone) {
  const phoneRegex = /^\+?[\d\s-]{10,}$/;
  return phoneRegex.test(phone);
}

function handleSignup(event) {
  event.preventDefault();
  
  const form = event.target;
  const password = form.querySelector('#password').value;
  const confirmPassword = form.querySelector('#confirmPassword').value;
  const phone = form.querySelector('#phone').value;
  
  const passwordError = validatePassword(password, confirmPassword);
  if (passwordError) {
    alert(passwordError);
    return;
  }
  
  if (!validatePhone(phone)) {
    alert('Please enter a valid phone number');
    return;
  }
  
  console.log('Signup form submission:', {
    fullName: form.querySelector('#fullName').value,
    email: form.querySelector('#signupEmail').value,
    phone: phone,
    password: password
  });
  
  form.reset();
  closeModal('signupModal');
  alert('Thank you for signing up! Welcome to ExamMentor.');
}

function handleLogin(event) {
  event.preventDefault();
  
  console.log('Login form submission:', {
    email: document.getElementById('loginEmail').value,
    password: document.getElementById('loginPassword').value
  });
  
  event.target.reset();
  closeModal('loginModal');
  alert('Successfully logged in!');
}

const observerOptions = {
  threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('fade-in');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.feature-card, .price-card, .faq-item').forEach(el => {
  observer.observe(el);
});

window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 50) {
    navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    navbar.style.backdropFilter = 'blur(8px)';
  } else {
    navbar.style.backgroundColor = 'var(--white)';
    navbar.style.backdropFilter = 'none';
  }
});