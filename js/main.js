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

  /* ---------- 3. Текущий год (футер и вертикальная подпись в hero) ---------- */
  ['year', 'hero-year'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.textContent = new Date().getFullYear();
  });

  /* ---------- 4. Лента кейсов: кнопки «назад / вперёд» ---------- */
  var track = document.getElementById('cases-track');
  if (track) {
    document.querySelectorAll('[data-slide]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var card = track.querySelector('.case-card');
        var step = card ? card.getBoundingClientRect().width + 28 : track.clientWidth * 0.8;
        track.scrollBy({ left: step * parseInt(btn.getAttribute('data-slide'), 10), behavior: 'smooth' });
      });
    });
  }

  /* ---------- 5. Оглавление статьи: подсветка текущего раздела ---------- */
  var tocLinks = document.querySelectorAll('.toc__list a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var tocObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.remove('is-active'); });
        var link = byId[entry.target.id];
        if (link) link.classList.add('is-active');
      });
    }, { rootMargin: '-100px 0px -65% 0px' });
    Object.keys(byId).forEach(function (id) {
      var h = document.getElementById(id);
      if (h) tocObserver.observe(h);
    });
  }
})();
// Интерактивная модель в кейсе Stroy-dom; данные примера не являются фактическими.
(() => {
  const form = document.getElementById('stroy-form');
  if (!form) return;
  const format = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 2 });
  const update = () => {
    if (!form.checkValidity()) return;
    const value = name => Number(form.elements[name].value);
    const leads = value('traffic') * value('conversion') / 100;
    const qualified = leads * value('quality') / 100;
    const deals = qualified * value('sales') / 100;
    const revenue = deals * value('amount');
    const results = { leads, qualified, deals, revenue, profit: revenue * value('margin') / 100 };
    Object.entries(results).forEach(([name, number]) => {
      document.querySelector(`[data-result="${name}"]`).textContent = format.format(number) + (name === 'revenue' || name === 'profit' ? ' BYN' : '');
    });
  };
  form.addEventListener('input', update);
  form.addEventListener('reset', () => setTimeout(update, 0));
  update();
})();
