/**
 * DatRey.ma — Shared JavaScript
 * Common logic for all pages: header, mobile nav, slider, scroll reveal, counters.
 */
(function () {
  'use strict';

  // --- Force Page Scroll Reset to Top on Load ---
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }
  window.addEventListener('load', () => {
    window.scrollTo(0, 0);
  });



  // --- Header scroll effect ---
  const header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });
  }

  // --- Mobile nav ---
  const mobileToggle = document.getElementById('mobileToggle');
  const mobileNav = document.getElementById('mobileNav');
  const mobileClose = document.getElementById('mobileClose');
  if (mobileToggle && mobileNav && mobileClose) {
    mobileToggle.addEventListener('click', () => mobileNav.classList.add('active'));
    mobileClose.addEventListener('click', () => mobileNav.classList.remove('active'));
    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => mobileNav.classList.remove('active'));
    });
    window.closeMobileNav = () => mobileNav.classList.remove('active');
  }

  // --- Strict Light Mode Enforcement ---
  document.documentElement.setAttribute('data-theme', 'light');
  localStorage.setItem('datrey-theme', 'light');
  
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.style.display = 'none';
  }

  // --- Interactive ROI Calculator Engine ---
  const budgetInput = document.getElementById('roiBudget');
  const budgetVal = document.getElementById('roiBudgetValue');
  const leadsOutput = document.getElementById('roiLeadsOutput');
  const revenueOutput = document.getElementById('roiRevenueOutput');

  if (budgetInput && budgetVal && leadsOutput && revenueOutput) {
    function updateROI() {
      const budget = parseInt(budgetInput.value, 10);
      budgetVal.textContent = budget.toLocaleString('fr-FR') + ' DH';
      const estimatedLeads = Math.round(budget / 115);
      const estimatedRevenue = Math.round(budget * 4.2);
      leadsOutput.textContent = '+' + estimatedLeads.toLocaleString('fr-FR');
      revenueOutput.textContent = estimatedRevenue.toLocaleString('fr-FR') + ' DH';
    }
    budgetInput.addEventListener('input', updateROI);
    updateROI();
  }

  // --- High-Performance Mouse Tracking (Card Level) ---
  function initSpotlight() {
    const cards = document.querySelectorAll('.service-card, .blog-card, .chic-card, .glass-card, .bento-card-glass');
    cards.forEach(card => {
      let ticking = false;
      card.addEventListener('mousemove', (e) => {
        if (!ticking) {
          requestAnimationFrame(() => {
            const rect = card.getBoundingClientRect();
            card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
            card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
            ticking = false;
          });
          ticking = true;
        }
      }, { passive: true });
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSpotlight);
  } else {
    initSpotlight();
  }

  // --- Scroll reveal ---
  const revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    revealElements.forEach(el => revealObserver.observe(el));
  }

  // --- Counter animation ---
  const stats = document.querySelectorAll('.hero-stat-value[data-count]');
  if (stats.length) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.count, 10);
          const suffix = el.textContent.replace(/[0-9]/g, '');
          let current = 0;
          const step = Math.max(1, Math.floor(target / 40));
          const timer = setInterval(() => {
            current += step;
            if (current >= target) { current = target; clearInterval(timer); }
            el.textContent = current + suffix;
          }, 30);
          counterObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    stats.forEach(el => counterObserver.observe(el));
  }

  // --- Sliders ---
  const sliderContainers = document.querySelectorAll('.hero-photo-slider, .slider-section');
  sliderContainers.forEach(container => {
    const slides = container.querySelectorAll('.hero-slide, .slider-slide');
    const dots = container.querySelectorAll('.slider-dot');
    const prevBtn = container.querySelector('#sliderPrev, #heroSliderPrev');
    const nextBtn = container.querySelector('#sliderNext, #heroSliderNext');

    if (slides.length) {
      let currentSlide = 0;
      let sliderInterval;

      function goToSlide(index) {
        slides[currentSlide].classList.remove('active');
        if (dots[currentSlide]) dots[currentSlide].classList.remove('active');
        currentSlide = (index + slides.length) % slides.length;
        slides[currentSlide].classList.add('active');
        if (dots[currentSlide]) dots[currentSlide].classList.add('active');
      }
      function startSlider() {
        sliderInterval = setInterval(() => goToSlide(currentSlide + 1), 5000);
      }
      function stopSlider() { clearInterval(sliderInterval); }

      if (prevBtn) prevBtn.addEventListener('click', () => { stopSlider(); goToSlide(currentSlide - 1); startSlider(); });
      if (nextBtn) nextBtn.addEventListener('click', () => { stopSlider(); goToSlide(currentSlide + 1); startSlider(); });
      dots.forEach((dot, idx) => {
        dot.addEventListener('click', () => {
          stopSlider();
          goToSlide(idx);
          startSlider();
        });
      });

      container.addEventListener('mouseenter', stopSlider);
      container.addEventListener('mouseleave', startSlider);
      startSlider();
    }
  });

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const id = link.getAttribute('href');
      if (id.length > 1) {
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });
})();

// --- Service Worker Registration ---
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Service worker disabled for maximum loading speed
  });
}

  // --- Mobile Bottom Tab Bar Injection ---
  function injectBottomTabBar() {
    if (document.querySelector('.bottom-tab-bar')) return; // Already injected
    
    // Determine active path to highlight the correct tab
    const path = window.location.pathname;
    const page = path.split('/').pop() || 'index.html';
    
    const isHome = page === 'index.html' || page === '';
    const isServices = page.startsWith('service');
    const isProjects = page === 'cas-clients.html';
    const isContact = page === 'contact.html';

    const bottomBarHTML = `
      <nav class="bottom-tab-bar">
        <a href="index.html" class="tab-item ${isHome ? 'active' : ''}">
          <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>Accueil</span>
        </a>
        <a href="services.html" class="tab-item ${isServices ? 'active' : ''}">
          <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
          </svg>
          <span>Services</span>
        </a>
        <a href="cas-clients.html" class="tab-item ${isProjects ? 'active' : ''}">
          <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
          </svg>
          <span>Projets</span>
        </a>
        <a href="contact.html" class="tab-item ${isContact ? 'active' : ''}">
          <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
            <polyline points="22,6 12,13 2,6"></polyline>
          </svg>
          <span>Contact</span>
        </a>
      </nav>
    `;
    document.body.insertAdjacentHTML('beforeend', bottomBarHTML);
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBottomTabBar);
  } else {
    injectBottomTabBar();
  }
