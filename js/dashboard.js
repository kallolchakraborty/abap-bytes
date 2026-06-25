function getBookmarks() {
  try { return JSON.parse(localStorage.getItem('ab_bookmarks')) || []; } catch (e) { return []; }
}

function getProgress() {
  try { return JSON.parse(localStorage.getItem('ab_progress')) || []; } catch (e) { return []; }
}

function getStudyPlannerData() {
  try { return JSON.parse(localStorage.getItem('study-planner')) || null; } catch (e) { return null; }
}

function getStarStories() {
  try { return JSON.parse(localStorage.getItem('star-builder-stories')) || []; } catch (e) { return []; }
}

function getWhiteboardState() {
  try { return JSON.parse(localStorage.getItem('whiteboard-state')) || []; } catch (e) { return []; }
}

function getTheme() {
  try { return localStorage.getItem('theme') || 'light'; } catch (e) { return 'light'; }
}

function getSearchIndex() {
  return window.__SEARCH_INDEX || [];
}

function getRouteMap() {
  return window.__ROUTE_MAP || {};
}

function calculateStats() {
  var progress = getProgress();
  var bookmarks = getBookmarks();
  var searchIndex = getSearchIndex();
  var routeMap = getRouteMap();
  var total = Object.keys(routeMap).length;
  var validProgress = progress.filter(function(hash) { return routeMap[hash]; });
  var completed = validProgress.length;
  var pct = total > 0 ? Math.round((completed / total) * 100) : 0;

  var categories = {};
  searchIndex.forEach(function(item) {
    var cat = item.category || 'Uncategorized';
    if (!categories[cat]) categories[cat] = { total: 0, done: 0 };
    categories[cat].total++;
    if (validProgress.includes(item.url.replace('docs.html', '#'))) categories[cat].done++;
  });

  var byCategory = Object.keys(categories).map(function(k) {
    return { name: k, total: categories[k].total, done: categories[k].done, pct: Math.round((categories[k].done / categories[k].total) * 100) };
  });
  byCategory.sort(function(a, b) { return b.total - a.total; });

  var planner = getStudyPlannerData();
  var plannerInfo = null;
  if (planner && planner.plan) {
    plannerInfo = {
      level: planner.plan.level,
      weeks: planner.plan.numWeeks,
      hrsPerDay: planner.plan.hrsPerDay,
      companies: (planner.plan.companies || []).join(', '),
      savedAt: planner.ts || 'Unknown'
    };
  }

  var stories = getStarStories();
  var whiteboardPaths = getWhiteboardState();

  return {
    total: total,
    completed: completed,
    percentage: pct,
    categories: byCategory,
    bookmarks: bookmarks.length,
    stories: stories.length,
    whiteboardSaved: whiteboardPaths.length > 0,
    planner: plannerInfo
  };
}

function renderDashboard() {
  var stats = calculateStats();
  var el = document.getElementById('dashboard-root');
  if (!el) return;

  el.innerHTML =
    '<div class="dash-grid">' +
      '<div class="dash-card dash-card-primary">' +
        '<div class="dash-card-icon"><span class="material-symbols-outlined">check_circle</span></div>' +
        '<div class="dash-card-value">' + stats.percentage + '%</div>' +
        '<div class="dash-card-label">Overall Progress</div>' +
        '<div class="dash-card-sub">' + stats.completed + ' of ' + stats.total + ' topics</div>' +
      '</div>' +
      '<div class="dash-card">' +
        '<div class="dash-card-icon"><span class="material-symbols-outlined">star</span></div>' +
        '<div class="dash-card-value">' + stats.bookmarks + '</div>' +
        '<div class="dash-card-label">Bookmarked Guides</div>' +
        '<div class="dash-card-sub"><a href="docs.html#faang-mindset" style="color:var(--brand-primary);">Continue learning &rarr;</a></div>' +
      '</div>' +
      '<div class="dash-card">' +
        '<div class="dash-card-icon"><span class="material-symbols-outlined">auto_stories</span></div>' +
        '<div class="dash-card-value">' + stats.stories + '</div>' +
        '<div class="dash-card-label">STAR Stories</div>' +
        '<div class="dash-card-sub"><a href="star-builder.html" style="color:var(--brand-primary);">Open builder &rarr;</a></div>' +
      '</div>' +
      '<div class="dash-card">' +
        '<div class="dash-card-icon"><span class="material-symbols-outlined">gesture</span></div>' +
        '<div class="dash-card-value">' + (stats.whiteboardSaved ? 'Saved' : 'Empty') + '</div>' +
        '<div class="dash-card-label">Whiteboard</div>' +
        '<div class="dash-card-sub"><a href="whiteboard.html" style="color:var(--brand-primary);">Open board &rarr;</a></div>' +
      '</div>' +
    '</div>' +
    '<div class="dash-section-title"><span class="material-symbols-outlined">folder</span> Progress by Category</div>' +
    '<div class="dash-category-list">' +
    stats.categories.map(function(c) {
      var color = c.pct >= 80 ? 'var(--svg-success-stroke)' : c.pct >= 40 ? 'var(--svg-warning-stroke)' : 'var(--brand-primary)';
      return '<div class="dash-category-row">' +
        '<div class="dash-category-name">' + c.name + '</div>' +
        '<div class="dash-category-bar-wrap"><div class="dash-category-bar" style="width:' + c.pct + '%;background:' + color + ';"></div></div>' +
        '<div class="dash-category-pct" style="color:' + color + ';">' + c.pct + '%</div>' +
        '<div class="dash-category-nums">' + c.done + '/' + c.total + '</div>' +
      '</div>';
    }).join('') +
    '</div>';

  if (stats.planner) {
    var p = stats.planner;
    el.innerHTML +=
      '<div class="dash-section-title" style="margin-top:24px;"><span class="material-symbols-outlined">calendar_month</span> Study Plan</div>' +
      '<div class="dash-plan-card">' +
        '<div class="dash-plan-row"><span class="dash-plan-label">Target Level</span><span class="dash-plan-value">' + p.level + '</span></div>' +
        '<div class="dash-plan-row"><span class="dash-plan-label">Duration</span><span class="dash-plan-value">' + p.weeks + ' weeks</span></div>' +
        '<div class="dash-plan-row"><span class="dash-plan-label">Daily Study</span><span class="dash-plan-value">' + p.hrsPerDay + ' hrs</span></div>' +
        '<div class="dash-plan-row"><span class="dash-plan-label">Companies</span><span class="dash-plan-value">' + p.companies + '</span></div>' +
        '<div class="dash-plan-row"><span class="dash-plan-label">Last Saved</span><span class="dash-plan-value">' + p.savedAt + '</span></div>' +
        '<a href="study-planner.html" class="dash-plan-btn">Open Study Planner &rarr;</a>' +
      '</div>';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var style = document.createElement('style');
  style.textContent = `
    .dash-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin-bottom:20px; }
    .dash-card { background:var(--bg-primary); border:1px solid var(--border-default); border-radius:14px; padding:20px; text-align:center; transition:background 0.25s ease, border-color 0.25s ease; }
    .dash-card-primary { border-color:var(--brand-primary); }
    .dash-card-icon { margin-bottom:8px; }
    .dash-card-icon .material-symbols-outlined { font-size:32px; color:var(--brand-primary); }
    .dash-card-value { font-size:28px; font-weight:700; color:var(--text-primary); font-family:'JetBrains Mono',monospace; }
    .dash-card-label { font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; margin-top:4px; }
    .dash-card-sub { font-size:11px; color:var(--text-secondary); margin-top:6px; }
    .dash-card-sub a { font-weight:600; }
    .dash-section-title { font-size:18px; font-weight:700; color:var(--text-primary); margin-bottom:12px; display:flex; align-items:center; gap:8px; }
    .dash-section-title .material-symbols-outlined { font-size:20px; color:var(--brand-primary); }
    .dash-category-list { display:flex; flex-direction:column; gap:8px; margin-bottom:16px; }
    .dash-category-row { display:flex; align-items:center; gap:12px; padding:8px 12px; background:var(--bg-primary); border:1px solid var(--border-default); border-radius:10px; }
    .dash-category-name { font-size:12px; font-weight:600; color:var(--text-primary); min-width:100px; }
    .dash-category-bar-wrap { flex:1; height:8px; background:var(--border-default); border-radius:999px; overflow:hidden; }
    .dash-category-bar { height:100%; border-radius:999px; transition:width 0.5s ease; min-width:4px; }
    .dash-category-pct { font-size:12px; font-weight:700; font-family:'JetBrains Mono',monospace; min-width:36px; text-align:right; }
    .dash-category-nums { font-size:11px; color:var(--text-muted); min-width:40px; text-align:right; }
    .dash-plan-card { background:var(--bg-primary); border:1px solid var(--border-default); border-radius:14px; padding:16px; }
    .dash-plan-row { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border-default); font-size:13px; }
    .dash-plan-row:last-of-type { border-bottom:none; }
    .dash-plan-label { color:var(--text-secondary); }
    .dash-plan-value { color:var(--text-primary); font-weight:600; }
    .dash-plan-btn { display:block; text-align:center; margin-top:12px; padding:8px; background:var(--brand-primary); color:#fff; border-radius:8px; font-size:13px; font-weight:600; transition:background 0.2s; }
    .dash-plan-btn:hover { background:var(--brand-hover); }
  `;
  document.head.appendChild(style);
  renderDashboard();
  window.addEventListener('storage', function(e) {
    if (e.key && (e.key.startsWith('ab_') || e.key === 'study-planner' || e.key === 'star-builder-stories' || e.key === 'whiteboard-state')) {
      renderDashboard();
    }
  });
});
