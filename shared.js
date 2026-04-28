/**
 * DatRey.ma — Shared JavaScript
 * Common logic for all pages: header, mobile nav, slider, scroll reveal, counters.
 */
(function () {
  'use strict';

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
    window.closeMobileNav = () => mobileNav.classList.remove('active');
  }

  // --- Theme Toggle (Dark Mode) ---
  const themeToggle = document.getElementById('themeToggle');
  const sunIcon = document.querySelector('.sun-icon');
  const moonIcon = document.querySelector('.moon-icon');
  
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('datrey-theme', theme);
    if (sunIcon && moonIcon) {
      sunIcon.style.display = theme === 'dark' ? 'block' : 'none';
      moonIcon.style.display = theme === 'dark' ? 'none' : 'block';
    }
  }

  // Initialize theme
  const savedTheme = localStorage.getItem('datrey-theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (savedTheme) {
    applyTheme(savedTheme);
  } else if (prefersDark) {
    applyTheme('dark');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
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

  // --- Slider (only if slider elements exist) ---
  const slides = document.querySelectorAll('.slider-slide');
  const dots = document.querySelectorAll('.slider-dot');
  const prevBtn = document.getElementById('sliderPrev');
  const nextBtn = document.getElementById('sliderNext');

  if (slides.length && prevBtn && nextBtn) {
    let currentSlide = 0;
    let sliderInterval;

    function goToSlide(index) {
      slides[currentSlide].classList.remove('active');
      dots[currentSlide].classList.remove('active');
      currentSlide = (index + slides.length) % slides.length;
      slides[currentSlide].classList.add('active');
      dots[currentSlide].classList.add('active');
    }
    function startSlider() {
      sliderInterval = setInterval(() => goToSlide(currentSlide + 1), 4500);
    }
    function stopSlider() { clearInterval(sliderInterval); }

    prevBtn.addEventListener('click', () => { stopSlider(); goToSlide(currentSlide - 1); startSlider(); });
    nextBtn.addEventListener('click', () => { stopSlider(); goToSlide(currentSlide + 1); startSlider(); });
    dots.forEach(dot => {
      dot.addEventListener('click', () => {
        stopSlider();
        goToSlide(parseInt(dot.dataset.slide, 10));
        startSlider();
      });
    });

    const sliderSection = document.querySelector('.slider-section');
    if (sliderSection) {
      sliderSection.addEventListener('mouseenter', stopSlider);
      sliderSection.addEventListener('mouseleave', startSlider);
    }
    startSlider();
  }

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


// --- ANTIGRAVITY UI GSAP INTEGRATION ---
document.addEventListener("DOMContentLoaded", () => {
  if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
    gsap.registerPlugin(ScrollTrigger);

    // 1. Hero Parallax & Depth Effect
    const hero = document.querySelector(".page-hero") || document.querySelector(".hero");
    if (hero) {
      gsap.to(hero, {
        scrollTrigger: {
          trigger: hero,
          start: "top top",
          end: "bottom top",
          scrub: true
        },
        y: 100, // Move down slightly for parallax
        opacity: 0.8,
        scale: 0.98,
        transformOrigin: "center top",
        ease: "none"
      });
    }

    // 2. Service Cards Staggered Entrance
    const serviceGrids = document.querySelectorAll(".services-grid");
    serviceGrids.forEach(grid => {
      const cards = grid.querySelectorAll(".service-card");
      if (cards.length > 0) {
        // Set initial state
        gsap.set(cards, { y: 50, opacity: 0, rotateX: 10 });
        
        ScrollTrigger.create({
          trigger: grid,
          start: "top 85%", // Trigger when the top of grid is 85% down the viewport
          onEnter: () => {
            gsap.to(cards, {
              y: 0,
              opacity: 1,
              rotateX: 0,
              stagger: 0.1,
              duration: 0.8,
              ease: "back.out(1.7)"
            });
          },
          once: true // Only animate once
        });
      }
    });

    // 3. Floating Image Effects
    const floatingImages = document.querySelectorAll(".approach-visual img, .service-hero-img img, .service-detail-img img");
    floatingImages.forEach(img => {
      gsap.set(img, { y: 30, opacity: 0, scale: 0.95 });
      ScrollTrigger.create({
        trigger: img,
        start: "top 85%",
        onEnter: () => {
          gsap.to(img, {
            y: 0,
            opacity: 1,
            scale: 1,
            duration: 1,
            ease: "power3.out"
          });
        },
        once: true
      });
    });
  }
});
