/**
 * DatRey.ma — Ultra-Chic Premium Animations
 * GSAP & ScrollTrigger — Luxury Tech Agency level
 */

document.addEventListener('DOMContentLoaded', () => {
    if (typeof gsap === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    // ─── 1. HERO CHOREOGRAPHED ENTRANCE ───
    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    const hero = document.querySelector('.hero');

    if (hero) {
        // Set initial states
        gsap.set('.hero-orb', { scale: 0, opacity: 0 });
        gsap.set('.hero-badge', { y: -20, opacity: 0 });
        gsap.set('.hero-title', { y: 60, opacity: 0 });
        gsap.set('.hero-subtitle', { y: 40, opacity: 0 });
        gsap.set('.hero-actions', { y: 30, opacity: 0 });
        gsap.set('.hero-stats', { y: 30, opacity: 0 });

        heroTl
            .to('.hero-orb', {
                scale: 1, opacity: 1,
                duration: 1.5, stagger: 0.2,
                ease: 'elastic.out(1, 0.6)'
            })
            .to('.hero-badge', {
                y: 0, opacity: 1, duration: 0.6
            }, '-=1')
            .to('.hero-title', {
                y: 0, opacity: 1, duration: 0.9,
                ease: 'power4.out'
            }, '-=0.6')
            .to('.hero-subtitle', {
                y: 0, opacity: 1, duration: 0.7
            }, '-=0.5')
            .to('.hero-actions', {
                y: 0, opacity: 1, duration: 0.6,
                ease: 'back.out(1.4)'
            }, '-=0.3')
            .to('.hero-stats', {
                y: 0, opacity: 1, duration: 0.6
            }, '-=0.2');
    }

    // ─── 2. PARALLAX ORBS (Mouse Reactive) ───
    const orbs = document.querySelectorAll('.hero-orb');
    if (orbs.length > 0) {
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 2;
            const y = (e.clientY / window.innerHeight - 0.5) * 2;

            gsap.to('.hero-orb-1', { x: x * 50, y: y * 50, duration: 2, ease: 'power2.out' });
            gsap.to('.hero-orb-2', { x: x * -40, y: y * -40, duration: 2.5, ease: 'power2.out' });
            gsap.to('.hero-orb-3', { x: x * 30, y: y * -20, duration: 3, ease: 'power2.out' });
        });
    }

    // ─── 3. SPOTLIGHT HOVER ON CARDS ───
    const cards = document.querySelectorAll('.service-card, .service-detail');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Update CSS custom properties for the radial glow
            card.style.setProperty('--mouse-x', x + 'px');
            card.style.setProperty('--mouse-y', y + 'px');

            // 3D Tilt
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -4;
            const rotateY = ((x - centerX) / centerX) * 4;

            gsap.to(card, {
                rotateX: rotateX,
                rotateY: rotateY,
                transformPerspective: 1000,
                ease: 'power1.out',
                duration: 0.4
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                rotateX: 0, rotateY: 0,
                ease: 'elastic.out(1, 0.5)',
                duration: 0.8
            });
        });
    });

    // ─── 4. MAGNETIC BUTTONS ───
    document.querySelectorAll('.btn-primary, .btn-outline, .btn-ghost').forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            gsap.to(el, { x: x * 0.2, y: y * 0.2, duration: 0.4, ease: 'power2.out' });
        });

        el.addEventListener('mouseleave', () => {
            gsap.to(el, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.3)' });
        });
    });

    // ─── 5. STAGGERED SCROLL REVEALS ───
    // Section titles
    document.querySelectorAll('.section-title, .section-subtitle, .section-label').forEach(el => {
        if (el.classList.contains('reveal')) {
            el.classList.remove('reveal');
            el.style.opacity = 1;
            el.style.transform = 'none';
        }

        gsap.from(el, {
            scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none reverse' },
            y: 40, opacity: 0, duration: 1, ease: 'power3.out'
        });
    });

    // Service grids — stagger entrance
    document.querySelectorAll('.services-grid').forEach(grid => {
        const gridCards = grid.querySelectorAll('.service-card');
        gridCards.forEach(child => {
            if (child.classList.contains('reveal')) {
                child.classList.remove('reveal');
                child.style.opacity = 1;
                child.style.transform = 'none';
            }
        });

        gsap.set(gridCards, { y: 50, opacity: 0, rotateX: 8 });

        ScrollTrigger.create({
            trigger: grid,
            start: 'top 85%',
            onEnter: () => {
                gsap.to(gridCards, {
                    y: 0, opacity: 1, rotateX: 0,
                    stagger: 0.12, duration: 0.8,
                    ease: 'back.out(1.5)'
                });
            },
            once: true
        });
    });

    // ─── 6. PARALLAX SCROLL FOR CARDS ───
    document.querySelectorAll('.floating-card .service-card-body').forEach((body) => {
        gsap.to(body, {
            scrollTrigger: {
                trigger: body.parentElement,
                start: 'top bottom',
                end: 'bottom top',
                scrub: 1.5
            },
            y: -25,
            ease: 'none'
        });
    });

    // Approach steps
    document.querySelectorAll('.approach-step').forEach((step, i) => {
        gsap.from(step, {
            scrollTrigger: { trigger: step, start: 'top 88%' },
            x: -30, opacity: 0, duration: 0.7,
            delay: i * 0.15,
            ease: 'power3.out'
        });
    });

    // Floating images
    document.querySelectorAll('.approach-visual img, .service-hero-img img').forEach(img => {
        gsap.set(img, { y: 30, opacity: 0, scale: 0.95 });
        ScrollTrigger.create({
            trigger: img, start: 'top 85%',
            onEnter: () => {
                gsap.to(img, { y: 0, opacity: 1, scale: 1, duration: 1, ease: 'power3.out' });
            },
            once: true
        });
    });

    // FAQ items — set initial state then animate on scroll
    const faqItems = document.querySelectorAll('.faq-item-chic');
    if (faqItems.length > 0) {
        gsap.set(faqItems, { y: 20, opacity: 0 });
        ScrollTrigger.create({
            trigger: '.faq-list, .faq-container',
            start: 'top 88%',
            onEnter: () => {
                gsap.to(faqItems, {
                    y: 0, opacity: 1,
                    stagger: 0.1, duration: 0.6,
                    ease: 'power2.out'
                });
            },
            once: true
        });
    });

    // --- Counter Animation (About Page) ---
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
      ScrollTrigger.create({
        trigger: '.stats-grid',
        start: "top 85%",
        once: true,
        onEnter: () => {
          counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            gsap.to(counter, {
              innerHTML: target,
              duration: 2.5,
              ease: "power2.out",
              snap: { innerHTML: 1 },
              onUpdate: function() {
                if (target >= 1000) {
                  const val = Math.round(this.targets()[0].innerHTML);
                  counter.innerHTML = val.toLocaleString('fr-FR').replace(/\s/g, ' ');
                }
              }
            });
          });
        }
      });
    }

    // ─── 7. CHIC ROWS HOVER EFFECT ───
    const chicRows = document.querySelectorAll('.chic-row');
  const hoverImg = document.getElementById('chicHoverImg');
  
  if (chicRows.length > 0 && hoverImg) {
    // Check if it's a desktop device (no touch)
    const isTouchDevice = (('ontouchstart' in window) || (navigator.maxTouchPoints > 0));
    
    if (!isTouchDevice) {
      chicRows.forEach(row => {
        row.addEventListener('mouseenter', (e) => {
          const imgUrl = row.getAttribute('data-image');
          if (imgUrl) {
            hoverImg.style.backgroundImage = `url('${imgUrl}')`;
          }
          hoverImg.classList.add('active');
        });
        
        row.addEventListener('mousemove', (e) => {
          // Use GSAP for smooth positioning
          if (typeof gsap !== 'undefined') {
            gsap.to(hoverImg, {
              x: e.clientX,
              y: e.clientY,
              duration: 0.6,
              ease: "power3.out"
            });
          } else {
            // Fallback if GSAP is not loaded yet
            hoverImg.style.left = e.clientX + 'px';
            hoverImg.style.top = e.clientY + 'px';
          }
        });
        
        row.addEventListener('mouseleave', () => {
          hoverImg.classList.remove('active');
        });
      });
    } else {
      // On mobile, just show static images or hide the hover element completely
      hoverImg.style.display = 'none';
    }
  }


  // --- 8. READING PROGRESS BAR (Blog Articles) ---
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

  // --- 9. SOCIAL SHARE BUTTONS (Blog Articles) ---
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



  // --- 10. EXIT INTENT POPUP — Focus Trap & Accessibility ---
  var exitPopup = document.getElementById('exitIntentPopup');
  if (exitPopup) {
    var popupModal = exitPopup.querySelector('.exit-popup-modal');
    var closeBtn = exitPopup.querySelector('.exit-popup-close');

    function openExitPopup() {
      if (sessionStorage.getItem('exitPopupShown')) return;
      exitPopup.classList.add('active');
      exitPopup.style.display = 'flex';
      sessionStorage.setItem('exitPopupShown', 'true');
      // Trap focus inside popup
      if (closeBtn) closeBtn.focus();
      document.addEventListener('keydown', trapFocus);
    }

    function closeExitPopup() {
      exitPopup.classList.remove('active');
      exitPopup.style.display = 'none';
      document.removeEventListener('keydown', trapFocus);
    }

    function trapFocus(e) {
      if (e.key === 'Escape') {
        closeExitPopup();
        return;
      }
      if (e.key !== 'Tab' || !popupModal) return;
      var focusable = popupModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (focusable.length === 0) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    // Close triggers
    if (closeBtn) closeBtn.addEventListener('click', closeExitPopup);
    exitPopup.addEventListener('click', function(e) {
      if (e.target === exitPopup) closeExitPopup();
    });

    // Exit intent trigger (mouse leaves viewport top)
    document.addEventListener('mouseout', function(e) {
      if (!e.relatedTarget && e.clientY < 10) {
        openExitPopup();
      }
    });
  }

});
