/**
 * DatRey.ma - Magic UX & Animations
 * Utilise GSAP & ScrollTrigger (chargés via CDN)
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialisation GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // 2. Parallax des Orbes (Hero Section)
    const orbs = document.querySelectorAll('.hero-orb');
    if (orbs.length > 0) {
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 2;
            const y = (e.clientY / window.innerHeight - 0.5) * 2;
            
            gsap.to('.hero-orb-1', {
                x: x * 50,
                y: y * 50,
                duration: 2,
                ease: "power2.out"
            });
            
            gsap.to('.hero-orb-2', {
                x: x * -40,
                y: y * -40,
                duration: 2.5,
                ease: "power2.out"
            });
        });
    }

    // 3. Boutons Magnétiques (Magnetic CTA)
    const magneticElements = document.querySelectorAll('.btn-primary, .btn-outline, .btn-ghost, .service-card');
    
    magneticElements.forEach((el) => {
        // Seulement pour les boutons, les cartes de service ont leur propre effet Tilt
        if(el.classList.contains('service-card')) return;
        
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            gsap.to(el, {
                x: x * 0.2,
                y: y * 0.2,
                duration: 0.4,
                ease: "power2.out"
            });
        });

        el.addEventListener('mouseleave', () => {
            gsap.to(el, {
                x: 0,
                y: 0,
                duration: 0.7,
                ease: "elastic.out(1, 0.3)"
            });
        });
    });

    // 4. Effet Tilt 3D sur les Cartes de Service (Glassmorphism 2.0)
    const cards = document.querySelectorAll('.service-card, .service-detail');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within the element.
            const y = e.clientY - rect.top;  // y position within the element.
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -5; // Max 5 deg
            const rotateY = ((x - centerX) / centerX) * 5;
            
            gsap.to(card, {
                rotateX: rotateX,
                rotateY: rotateY,
                transformPerspective: 1000,
                ease: "power1.out",
                duration: 0.4
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                rotateX: 0,
                rotateY: 0,
                ease: "power2.out",
                duration: 0.6
            });
        });
    });

    // 5. GSAP Text Reveal (Titres et Sous-titres)
    // Au lieu de faire un simple fade-in, on anime les éléments un par un quand ils entrent dans le viewport
    const revealElements = document.querySelectorAll('.section-title, .section-subtitle, .section-label');
    
    revealElements.forEach(el => {
        // Enlève la classe de base si elle existe pour éviter les conflits
        if(el.classList.contains('reveal')) {
            el.classList.remove('reveal');
            el.style.opacity = 1;
            el.style.transform = 'none';
        }
        
        gsap.from(el, {
            scrollTrigger: {
                trigger: el,
                start: "top 85%",
                toggleActions: "play none none reverse"
            },
            y: 40,
            opacity: 0,
            duration: 1,
            ease: "power3.out"
        });
    });
    
    // Animer les cartes de la grille avec un stagger
    const grids = document.querySelectorAll('.services-grid, .approach-grid');
    grids.forEach(grid => {
        // Enlève les classes reveal des enfants pour laisser GSAP gérer
        Array.from(grid.children).forEach(child => {
            if(child.classList.contains('reveal')) {
                child.classList.remove('reveal');
                child.style.opacity = 1;
                child.style.transform = 'none';
            }
        });

        gsap.from(grid.children, {
            scrollTrigger: {
                trigger: grid,
                start: "top 80%",
            },
            y: 50,
            opacity: 0,
            duration: 0.8,
            stagger: 0.15,
            ease: "back.out(1.2)"
        });
    });
});
