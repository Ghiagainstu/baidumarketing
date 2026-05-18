"use strict";

// ===== PAGE FADE-IN =====
document.body.style.opacity = '0';
document.body.style.transition = 'opacity 0.5s ease';
requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    document.body.style.opacity = '1';
  });
});

// ===== THEME TOGGLE =====
function toggleTheme() {
  const html = document.documentElement;
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  try { localStorage.setItem('theme', next); } catch(e) {}
  const themeColor = document.querySelector('meta[name="theme-color"]');
  if (themeColor) {
    themeColor.content = next === 'dark' ? '#0B0F1A' : '#FFFFFF';
  }
}

// Initialize theme from localStorage or system preference
(function initTheme() {
  let theme = 'light';
  try {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark' || saved === 'light') theme = saved;
    else if (window.matchMedia('(prefers-color-scheme: dark)').matches) theme = 'dark';
  } catch(e) {}
  document.documentElement.setAttribute('data-theme', theme);
  const themeColor = document.querySelector('meta[name="theme-color"]');
  if (themeColor) {
    themeColor.content = theme === 'dark' ? '#0B0F1A' : '#FFFFFF';
  }
})();

// ===== MOBILE NAV TOGGLE =====
let mobileNavOpen = false;
function toggleMobileNav() {
  const links = document.getElementById('navLinks');
  const hamburger = document.querySelector('.hamburger-icon');
  const closeX = document.querySelector('.close-icon');
  const overlay = document.getElementById('navOverlay');
  if (!links) return;
  
  mobileNavOpen = !mobileNavOpen;
  if (mobileNavOpen) {
    links.classList.add('open');
    if (hamburger) hamburger.style.display = 'none';
    if (closeX) closeX.style.display = 'block';
    if (overlay) overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  } else {
    links.classList.remove('open');
    if (hamburger) hamburger.style.display = 'block';
    if (closeX) closeX.style.display = 'none';
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// ===== LANGUAGE SWITCHER =====
function toggleLangMenu() {
  const menu = document.getElementById('langSwitchMenu');
  if (menu) menu.classList.toggle('open');
}

// ===== FAQ ACCORDION =====
function toggleFaq(btn) {
  const item = btn.closest('.faq-item');
  if (!item) return;
  const isOpen = item.classList.contains('open');
  // Close all other items
  document.querySelectorAll('.faq-item.open').forEach(el => {
    if (el !== item) el.classList.remove('open');
  });
  // Toggle current
  item.classList.toggle('open', !isOpen);
}

// ===== FORM SUBMIT =====
function handleSubmit(e) {
  e.preventDefault();
  // Honeypot check
  const honeypot = document.getElementById('website');
  if (honeypot && honeypot.value) return;
  
  const form = e.target;
  const email = form.querySelector('[name="email"]')?.value || '';
  
  // Show success message
  const successEmail = document.getElementById('successEmail');
  if (successEmail) successEmail.textContent = email;
  
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');
  if (contactForm) contactForm.style.display = 'none';
  if (formSuccess) formSuccess.style.display = 'block';
  
  // Build mailto link
  const formData = new FormData(form);
  const fname = formData.get('fname') || '';
  const lname = formData.get('lname') || '';
  const company = formData.get('company') || '';
  const service = formData.get('service') || '';
  const budget = formData.get('budget') || '';
  const message = formData.get('message') || '';
  
  const subject = encodeURIComponent('New Baidu PPC Inquiry from ' + company);
  const body = encodeURIComponent(
    'Name: ' + fname + ' ' + lname + '\n' +
    'Email: ' + email + '\n' +
    'Company: ' + company + '\n' +
    'Service: ' + service + '\n' +
    'Budget: ' + budget + '\n' +
    'Message: ' + message
  );
  
  const emailEl = document.querySelector('.obf-email');
  if (emailEl) {
    const emailAddr = emailEl.dataset.u + '@' + emailEl.dataset.d;
    window.location.href = 'mailto:' + emailAddr + '?subject=' + subject + '&body=' + body;
  }
}

// ===== COUNTER ANIMATION =====
function animateCounter(el) {
  const target = parseFloat(el.dataset.target);
  const prefix = el.dataset.prefix || '';
  const suffix = el.dataset.suffix || '';
  const decimals = parseInt(el.dataset.decimals) || 0;
  const duration = 1500;
  const start = performance.now();
  
  function easeOutExpo(t) {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }
  
  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeOutExpo(progress);
    const current = target * eased;
    
    if (decimals > 0) {
      el.textContent = prefix + current.toFixed(decimals) + suffix;
    } else {
      el.textContent = prefix + Math.round(current) + suffix;
    }
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  requestAnimationFrame(update);
}

// ===== DASHBOARD KPI ANIMATION =====
function animateKPIs() {
  const kpis = {
    spend:      { target: 48650,  format: v => '¥' + v.toLocaleString() },
    conversions: { target: 1283,   format: v => v.toLocaleString() },
    cpc:        { target: 0.45,   format: v => '¥' + v.toFixed(2), decimals: 2 },
    ctr:        { target: 4.8,    format: v => v.toFixed(1) + '%', decimals: 1 },
  };
  const duration = 1800;
  const startTime = performance.now();
  
  function easeOutExpo(t) {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }
  
  function update() {
    const elapsed = performance.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeOutExpo(progress);
    
    for (const [key, config] of Object.entries(kpis)) {
      const el = document.querySelector(`[data-kpi="${key}"]`);
      if (el) {
        const current = config.target * eased;
        const decimals = config.decimals || 0;
        const value = decimals > 0 ? parseFloat(current.toFixed(decimals)) : Math.round(current);
        el.textContent = config.format(value);
      }
    }
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  requestAnimationFrame(update);
}

// ===== DASHBOARD CHART LINE ANIMATION =====
function animateChartLine() {
  const line = document.querySelector('.chart-line');
  const area = document.querySelector('.chart-area');
  if (!line || !area) return;
  
  const lineLength = line.getTotalLength();
  line.style.strokeDasharray = lineLength;
  line.style.strokeDashoffset = lineLength;
  line.style.transition = 'stroke-dashoffset 2s cubic-bezier(.16,1,.3,1)';
  
  area.style.opacity = '0';
  area.style.transition = 'opacity 1s ease .8s';
  
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      line.style.strokeDashoffset = '0';
      area.style.opacity = '1';
    });
  });
}

// ===== STAGGER SCROLL ANIMATIONS =====
const staggerObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const items = entry.target.querySelectorAll('[data-stagger]');
      items.forEach((item, i) => {
        setTimeout(() => {
          item.style.opacity = '1';
          item.style.transform = 'translateY(0)';
        }, i * 80);
      });
      staggerObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.features-grid, .whyus-grid, .testimonials-grid, .pricing-grid, .team-grid').forEach(grid => {
  const children = grid.children;
  Array.from(children).forEach((child, i) => {
    child.style.opacity = '0';
    child.style.transform = 'translateY(24px)';
    child.style.transition = 'opacity .5s cubic-bezier(.16,1,.3,1), transform .5s cubic-bezier(.16,1,.3,1)';
    child.dataset.stagger = i;
  });
  staggerObserver.observe(grid);
});

// ===== SECTION FADE-IN =====
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      sectionObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.05 });

document.querySelectorAll('.section-header, .contact-wrapper, .faq-list, #trusted, .contact-form, .contact-info').forEach(el => {
  if (el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity .6s cubic-bezier(.16,1,.3,1), transform .6s cubic-bezier(.16,1,.3,1)';
    sectionObserver.observe(el);
  }
});

// ===== COUNTER TRIGGER =====
let counterTriggered = false;
const heroStatsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !counterTriggered) {
      counterTriggered = true;
      document.querySelectorAll('.stat-num[data-target]').forEach((el, i) => {
        setTimeout(() => animateCounter(el), i * 200);
      });
      heroStatsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.3 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) heroStatsObserver.observe(heroStats);

// ===== PAGE-SPECIFIC INITIALIZATION =====
// Trigger Dashboard animations on pages that have the chart
const chartLine = document.querySelector('.chart-line');
const kpiElements = document.querySelectorAll('[data-kpi]');
if (chartLine || (kpiElements && kpiElements.length > 0)) {
  setTimeout(() => {
    if (kpiElements && kpiElements.length > 0) animateKPIs();
    if (chartLine) animateChartLine();
  }, 600);
}

// ===== BACK TO TOP BUTTON =====
const backToTopBtn = document.getElementById('backToTop');
if (backToTopBtn) {
  window.addEventListener('scroll', () => {
    backToTopBtn.classList.toggle('visible', window.scrollY > 600);
  });
}

// ===== OBFUSCATED EMAIL RENDERING =====
document.querySelectorAll('.obf-email').forEach(function(el) {
  el.textContent = el.dataset.u + '@' + el.dataset.d;
});
document.querySelectorAll('.obf-email-link').forEach(function(el) {
  const addr = el.dataset.u + '@' + el.dataset.d;
  el.href = 'mailto:' + addr;
  if (!el.textContent) el.textContent = addr;
});
document.querySelectorAll('.obf-email-icon').forEach(function(el) {
  el.href = 'mailto:' + el.dataset.u + '@' + el.dataset.d;
});

// ===== DOM CONTENT LOADED - EVENT BINDING =====
document.addEventListener('DOMContentLoaded', function() {
  // Theme toggle buttons
  const themeToggleBtn = document.getElementById('themeToggle');
  if (themeToggleBtn) themeToggleBtn.addEventListener('click', toggleTheme);
  
  const mobileThemeBtn = document.querySelector('.nav-mobile-theme');
  if (mobileThemeBtn) mobileThemeBtn.addEventListener('click', toggleTheme);
  
  // Mobile nav toggle
  const mobileNavToggleBtn = document.getElementById('navToggle');
  if (mobileNavToggleBtn) mobileNavToggleBtn.addEventListener('click', toggleMobileNav);
  
  const navOverlay = document.getElementById('navOverlay');
  if (navOverlay) navOverlay.addEventListener('click', toggleMobileNav);
  
  // Close mobile nav when a link is clicked
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      if (mobileNavOpen) toggleMobileNav();
    });
  });
  
  // Language switcher
  const langSwitchBtn = document.querySelector('.lang-switch-btn');
  if (langSwitchBtn) langSwitchBtn.addEventListener('click', toggleLangMenu);
  
  // Close lang menu on outside click
  document.addEventListener('click', function(e) {
    const sw = document.querySelector('.lang-switch');
    if (sw && !sw.contains(e.target)) {
      const menu = document.getElementById('langSwitchMenu');
      if (menu) menu.classList.remove('open');
    }
  });
  
  // FAQ questions
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.addEventListener('click', function() { toggleFaq(this); });
  });
  
  // Contact form
  const contactForm = document.getElementById('contactForm');
  if (contactForm) contactForm.addEventListener('submit', handleSubmit);
  
  // Back to top button
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
  
  // Copyright year - safe DOM replacement for document.write()
  const copyrightYearEl = document.getElementById('copyrightYear');
  if (copyrightYearEl) copyrightYearEl.textContent = new Date().getFullYear();
});
