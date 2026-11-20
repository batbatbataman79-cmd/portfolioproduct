/* =========================================================
   main.js — анимации и мелкая логика интерфейса.
   Без библиотек. Работает локально и на GitHub Pages.
   ========================================================= */

(function () {
  // JS загрузился — снимаем «страховочный» класс (см. .no-js в style.css)
  document.documentElement.classList.remove('no-js');

  /* ---------- 1. Fade-in при скролле ----------
     Любому элементу добавьте класс "reveal" — он плавно появится.
     data-delay="150" — задержка в мс (для карточек по очереди). */
  var items = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var delay = parseInt(el.getAttribute('data-delay'), 10) || 0;
        el.style.transitionDelay = delay + 'ms';
        el.classList.add('is-visible');
        observer.unobserve(el); // анимируем один раз
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    items.forEach(function (el) { observer.observe(el); });
  } else {
    // Старые браузеры — просто показываем всё
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- 2. Линия под шапкой после начала прокрутки ---------- */
  var header = document.querySelector('.header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- 3. Текущий год в футере ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
