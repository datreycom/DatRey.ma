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
            trigger: '.faq-container',
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
});
