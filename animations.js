/**
 * DatRey.ma — Zero-Lag Performance Script
 * Fast, instant UI loading without scroll-blocking animations.
 */

document.addEventListener('DOMContentLoaded', () => {

  // --- 1. INSTANT REVEALS ---
  document.querySelectorAll('.reveal, .service-card, .faq-item-chic, .approach-step').forEach(el => {
    el.classList.add('visible');
    el.style.opacity = '1';
    el.style.transform = 'none';
  });

  // --- 2. STAT COUNTERS ---
  const counters = document.querySelectorAll('.counter, .hero-stat-value[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-target') || el.dataset.count, 10);
          if (!target) return;
          const suffix = el.textContent.replace(/[0-9]/g, '');
          el.textContent = target.toLocaleString('fr-FR').replace(/\s/g, ' ') + suffix;
          counterObserver.unobserve(el);
        }
      });
    }, { threshold: 0.1 });

    counters.forEach(el => counterObserver.observe(el));
  }

  // --- 3. READING PROGRESS BAR (Blog Articles) ---
  var blogContent = document.querySelector('.blog-content');
  if (blogContent) {
    var progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    var progressFill = document.createElement('div');
    progressFill.className = 'reading-progress-fill';
    progressBar.appendChild(progressFill);
    document.body.appendChild(progressBar);

    var scrollTicking = false;
    window.addEventListener('scroll', function() {
      if (!scrollTicking) {
        requestAnimationFrame(function() {
          var rect = blogContent.getBoundingClientRect();
          var total = blogContent.scrollHeight - window.innerHeight;
          var scrolled = window.scrollY - blogContent.offsetTop;
          var pct = Math.min(Math.max(scrolled / total, 0), 1) * 100;
          progressFill.style.width = pct + '%';
          if (rect.top < 0 && rect.bottom > 0) {
            progressBar.classList.add('active');
          } else {
            progressBar.classList.remove('active');
          }
          scrollTicking = false;
        });
        scrollTicking = true;
      }
    }, { passive: true });
  }

  // --- 4. EXIT INTENT POPUP (Strict Window Mouseleave Trigger) ---
  var exitPopup = document.getElementById('exitIntentPopup');
  if (exitPopup) {
    var closeBtn = exitPopup.querySelector('.exit-popup-close');

    function openExitPopup() {
      if (sessionStorage.getItem('exitPopupShown')) return;
      exitPopup.classList.add('active');
      sessionStorage.setItem('exitPopupShown', 'true');
    }

    function closeExitPopup() {
      exitPopup.classList.remove('active');
    }

    if (closeBtn) closeBtn.addEventListener('click', closeExitPopup);
    exitPopup.addEventListener('click', function(e) {
      if (e.target === exitPopup) closeExitPopup();
    });

    document.addEventListener('mouseleave', function(e) {
      if (e.clientY <= 0 || e.clientX <= 0 || e.clientX >= window.innerWidth) {
        openExitPopup();
      }
    });
  }

});
