(function() {
  var key = 'theme';
  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function safeSet(key, val) {
    try { localStorage.setItem(key, val); } catch (e) {}
  }
  function getTheme() {
    var stored = safeGet(key);
    if (stored === 'dark' || stored === 'light') return stored;
    return 'light';
  }
  function apply(t) {
    document.documentElement.classList.toggle('dark', t === 'dark');
    var icons = document.querySelectorAll('.theme-toggle-btn .material-symbols-outlined');
    for (var i = 0; i < icons.length; i++) {
      icons[i].textContent = t === 'dark' ? 'light_mode' : 'dark_mode';
    }
    try {
      window.dispatchEvent(new CustomEvent('theme-changed', { detail: { theme: t } }));
    } catch (e) {}
  }
  apply(getTheme());
  document.addEventListener('DOMContentLoaded', function() {
    var btns = document.querySelectorAll('.theme-toggle-btn');
    for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener('click', function() {
        var isDark = document.documentElement.classList.contains('dark');
        var t = isDark ? 'light' : 'dark';
        apply(t);
        safeSet(key, t);
      });
    }
  });
  if (/(Mac|iPhone|iPad|iPod)/i.test(navigator.userAgent)) {
    document.addEventListener('DOMContentLoaded', function() {
      document.querySelectorAll('kbd').forEach(function(el) {
        el.textContent = el.textContent.replace('Ctrl', '\u2318');
      });
    });
  }
})();
