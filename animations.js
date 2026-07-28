/**
 * DatRey.ma — Ultra-Chic Premium Animations
 * GSAP & ScrollTrigger — Luxury Tech Agency level
 */

document.addEventListener('DOMContentLoaded', () => {
    if (typeof gsap === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    // ─── 0. LENIS SMOOTH SCROLL ───
    if (typeof Lenis !== 'undefined') {
        const lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            direction: 'vertical',
            gestureDirection: 'vertical',
            smooth: true,
            mouseMultiplier: 1,
            smoothTouch: false,
            touchMultiplier: 2,
            infinite: false,
        })
        function raf(time) {
            lenis.raf(time)
            requestAnimationFrame(raf)
        }
        requestAnimationFrame(raf)
        
        // Sync Lenis with ScrollTrigger
        lenis.on('scroll', ScrollTrigger.update)
        gsap.ticker.add((time)=>{
            lenis.raf(time * 1000)
        })
        gsap.ticker.lagSmoothing(0)
    }

    // Custom cursor removed — using native browser cursor



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
    // Mouse effect removed as requested
    const orbs = document.querySelectorAll('.hero-orb');

    // ─── 3. SPOTLIGHT HOVER ON CARDS ───
    // Mouse tilt effect removed as requested

    // ─── 4. MAGNETIC BUTTONS ───
    // Magnetic mouse effect removed as requested

    // ─── 5. STAGGERED SCROLL REVEALS ───
    // Section titles & typography stagger
    document.querySelectorAll('.section-title, .section-subtitle, .section-label, h2.blog-grid-title').forEach(el => {
        if (el.classList.contains('reveal')) {
            el.classList.remove('reveal');
            el.style.opacity = 1;
            el.style.transform = 'none';
        }

        // Simple text split for staggered effect
        // We only split if it hasn't been split yet and doesn't contain HTML tags that would break
        if (!el.classList.contains('split-done') && !el.querySelector('*')) {
            const words = el.innerText.split(' ');
            el.innerHTML = '';
            words.forEach(word => {
                const wrapper = document.createElement('span');
                wrapper.style.display = 'inline-block';
                wrapper.style.overflow = 'hidden';
                wrapper.style.verticalAlign = 'top';
                wrapper.style.marginRight = '0.3em'; // Space between words

                const inner = document.createElement('span');
                inner.innerText = word;
                inner.style.display = 'inline-block';
                inner.style.transform = 'translateY(100%)'; // Hidden initially
                inner.classList.add('stagger-word');
                
                wrapper.appendChild(inner);
                el.appendChild(wrapper);
            });
            el.classList.add('split-done');

            gsap.to(el.querySelectorAll('.stagger-word'), {
                scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none reverse' },
                y: '0%', duration: 0.8, stagger: 0.05, ease: 'power4.out'
            });
        } else {
            // Fallback for elements with HTML inside
            gsap.from(el, {
                scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none reverse' },
                y: 40, opacity: 0, duration: 1, ease: 'power3.out'
            });
        }
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
    }

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



  // --- 10. EXIT INTENT POPUP — Fixed Modal & Zero-Scroll ---
  var exitPopup = document.getElementById('exitIntentPopup');
  if (exitPopup) {
    var popupModal = exitPopup.querySelector('.exit-popup-modal');
    var closeBtn = exitPopup.querySelector('.exit-popup-close');
    var pageStartTime = Date.now();

    function openExitPopup() {
      if (sessionStorage.getItem('exitPopupShown')) return;
      if (window.scrollY < 200) return; // Prevent triggering if user is still at the top of the page
      exitPopup.classList.add('active');
      sessionStorage.setItem('exitPopupShown', 'true');
      document.addEventListener('keydown', trapFocus);
    }

    function closeExitPopup() {
      exitPopup.classList.remove('active');
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

    // Exit intent trigger (mouse leaves viewport top after at least 6s and scrolled down)
    document.addEventListener('mouseout', function(e) {
      if (Date.now() - pageStartTime > 6000 && window.scrollY >= 200) {
        if (!e.relatedTarget && e.clientY < 10) {
          openExitPopup();
        }
      }
    });
  }

});
