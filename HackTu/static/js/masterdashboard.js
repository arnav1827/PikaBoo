function updateDateTime() {
  const now = new Date();
  const timeElement = document.getElementById('current-time');
  const dateElement = document.getElementById('current-date');
  
  timeElement.textContent = now.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
  
  dateElement.textContent = now.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

setInterval(updateDateTime, 60000);
updateDateTime();

document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelector('.nav-links li.active')?.classList.remove('active');
    link.parentElement.classList.add('active');
  });
});

function initTableauViz() {
  var containerDiv = document.getElementById("tableauViz");
  var url = "https://public.tableau.com/app/profile/kartik.arora7176/viz/JeeMasterInsights/JeeMasterInsights"; 
  
  var options = {
    hideTabs: true,
    onFirstInteractive: function () {
      console.log("Tableau Dashboard is interactive!");
    }
  };

  new tableau.Viz(containerDiv, url, options);
}

window.onload = initTableauViz;

function showSection(id) {
  const sections = document.querySelectorAll('.section');
  sections.forEach(section => section.style.display = 'none');
  document.getElementById(id).style.display = 'block';
}

showSection('dashboard');
document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.nav-links a');
  const mainContent = document.querySelector('.main-content');

  navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const page = link.getAttribute('data-page');
      if (!page) return;

      const xhr = new XMLHttpRequest();
      xhr.open('GET', page, true);
      xhr.onload = function () {
        if (xhr.status === 200) {
          mainContent.innerHTML = xhr.responseText;

          const scripts = mainContent.querySelectorAll('script');
          scripts.forEach(script => {
            const newScript = document.createElement('script');
            if (script.src) {
              newScript.src = script.src;
            } else {
              newScript.textContent = script.textContent;
            }
            document.body.appendChild(newScript);
          });

          navLinks.forEach(navLink => navLink.parentElement.classList.remove('active'));
          link.parentElement.classList.add('active');
        } else {
          mainContent.innerHTML = `<p>Error loading ${page}</p>`;
        }
      };
      xhr.onerror = function () {
        mainContent.innerHTML = `<p>Network Error</p>`;
      };
      xhr.send();
    });
  });
});
