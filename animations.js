/**
 * DatRey.ma — Lightweight High-Performance Animations
 * Fast, GPU-accelerated entrance effects without thread blocking.
 */

document.addEventListener('DOMContentLoaded', () => {

  // --- 1. HERO ENTRANCE (Lightweight CSS/GSAP) ---
  if (typeof gsap !== 'undefined') {
    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    const hero = document.querySelector('.hero, .page-hero');

    if (hero) {
      gsap.set('.hero-badge, .hero-title, .hero-subtitle, .hero-actions, .hero-stats', { y: 24, opacity: 0 });
      heroTl
        .to('.hero-badge', { y: 0, opacity: 1, duration: 0.5 })
        .to('.hero-title', { y: 0, opacity: 1, duration: 0.7 }, '-=0.3')
        .to('.hero-subtitle', { y: 0, opacity: 1, duration: 0.6 }, '-=0.4')
        .to('.hero-actions', { y: 0, opacity: 1, duration: 0.5 }, '-=0.3')
        .to('.hero-stats', { y: 0, opacity: 1, duration: 0.5 }, '-=0.2');
    }
  }

  // --- 2. FAST INTERSECTION OBSERVER FOR REVEALS ---
  const revealElements = document.querySelectorAll('.reveal, .service-card, .faq-item-chic, .approach-step');
  if (revealElements.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'none';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

    revealElements.forEach(el => observer.observe(el));
  }

  // --- 3. STAT COUNTERS ---
  const counters = document.querySelectorAll('.counter, .hero-stat-value[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-target') || el.dataset.count, 10);
          if (!target) return;
          const suffix = el.textContent.replace(/[0-9]/g, '');
          let current = 0;
          const step = Math.max(1, Math.floor(target / 30));
          const timer = setInterval(() => {
            current += step;
            if (current >= target) {
              current = target;
              clearInterval(timer);
            }
            el.textContent = current.toLocaleString('fr-FR').replace(/\s/g, ' ') + suffix;
          }, 35);
          counterObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(el => counterObserver.observe(el));
  }

  // --- 4. READING PROGRESS BAR (Blog Articles) ---
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

  // --- 5. SOCIAL SHARE BUTTONS ---
  var articleEl = document.querySelector('article.blog-content');
  if (articleEl) {
    var shareContainer = document.createElement('div');
    shareContainer.className = 'blog-share';
    var shareUrl = encodeURIComponent(window.location.href);
    var shareTitle = encodeURIComponent(document.title);

    shareContainer.innerHTML = '<span class="blog-share-label">Partager :</span>'
      + '<a href="https://www.linkedin.com/sharing/share-offsite/?url=' + shareUrl + '" target="_blank" rel="noopener" aria-label="LinkedIn" class="blog-share-btn blog-share-linkedin"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 6a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/></svg></a>'
      + '<a href="https://twitter.com/intent/tweet?url=' + shareUrl + '&text=' + shareTitle + '" target="_blank" rel="noopener" aria-label="X" class="blog-share-btn blog-share-x"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M4 4l11.73 16h5L9 4H4z"/></svg></a>'
      + '<a href="https://api.whatsapp.com/send?text=' + shareTitle + '%20' + shareUrl + '" target="_blank" rel="noopener" aria-label="WhatsApp" class="blog-share-btn blog-share-whatsapp"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0012.05 0z"/></svg></a>';

    var metaEl = articleEl.querySelector('.blog-meta');
    if (metaEl) {
      metaEl.insertAdjacentElement('afterend', shareContainer);
    } else {
      articleEl.prepend(shareContainer);
    }
  }

  // --- 6. EXIT INTENT POPUP (Strict Window Mouseleave Trigger) ---
  var exitPopup = document.getElementById('exitIntentPopup');
  if (exitPopup) {
    var popupModal = exitPopup.querySelector('.exit-popup-modal');
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
