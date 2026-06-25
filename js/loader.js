var _TAG_COLORS = ['#2563eb','#34d399','#fbbf24','#c4b5fd','#fb923c','#6366f1','#0ea5e9','#ef4444','#a855f7','#10b981','#f59e0b','#ec4899','#f97316','#d946ef','#22c55e','#eab308','#7c3aed','#2dd4bf'];
var PREREQUISITES = {
  'abap-rap-managed': ['abap-cds','abap-odata'],
  'abap-rap-unmanaged': ['abap-rap-managed'],
  'abap-rap-extensions': ['abap-rap-managed'],
  'abap-cap': ['abap-cds'],
  'abap-cds': ['abap-opensql','abap-platform'],
  'abap-performance': ['abap-internal-tables','abap-opensql'],
  'abap-amdp': ['abap-cds','abap-hana'],
  'abap-clean-core': ['abap-platform'],
  'abap-fiori': ['abap-odata','abap-cds'],
  'abap-events': ['abap-rap-managed'],
  'abap-odata': ['abap-platform'],
  'abap-hana': ['abap-platform'],
  'abap-security': ['abap-platform'],
  'abap-observability': ['abap-platform'],
  'abap-migration': ['abap-platform','abap-clean-core'],
  'abap-devops': ['abap-platform'],
  'abap-testing': ['abap-platform','abap-rap-managed'],
  'abap-design-docs': ['abap-behavioral'],
  'abap-extensibility': ['abap-clean-core','abap-rap-extensions'],
  'abap-finops': ['abap-cloud'],
  'abap-multitenancy': ['abap-platform'],
  'sysdesign-faang': ['staff-framing'],
  'design-global-erp': ['sysdesign-faang'],
  'design-integration-hub': ['sysdesign-faang'],
  'design-master-data': ['sysdesign-faang'],
  'design-dr': ['sysdesign-faang','design-global-erp'],
  'interview-structure': ['faang-mindset'],
  'mock-transcripts': ['interview-structure','abap-behavioral'],
  'offer-negotiation': ['faang-mindset'],
  'translation-map': ['faang-mindset'],
  'interview-playbook': ['faang-mindset'],
  'start-here': ['faang-mindset'],
  'sap-business-ai': ['abap-cap'],
  'elephant-in-room': ['faang-mindset'],
  'abap-internal-tables': ['abap-platform'],
  'abap-oop': ['abap-platform'],
  'abap-transaction': ['abap-platform'],
  'abap-opensql': ['abap-platform']
};
var NEXT_UP = {
  'faang-mindset': 'start-here',
  'start-here': 'translation-map',
  'translation-map': 'elephant-in-room',
  'elephant-in-room': 'interview-playbook',
  'interview-playbook': 'interview-structure',
  'interview-structure': 'mock-transcripts',
  'mock-transcripts': 'abap-behavioral',
  'abap-behavioral': 'sysdesign-faang',
  'sysdesign-faang': 'design-global-erp',
  'staff-framing': 'tradeoff-matrices',
  'tradeoff-matrices': 'estimation',
  'estimation': 'sysdesign-faang',
  'abap-platform': 'abap-internal-tables',
  'abap-internal-tables': 'abap-oop',
  'abap-oop': 'abap-transaction',
  'abap-transaction': 'abap-opensql',
  'abap-opensql': 'abap-cds',
  'abap-cds': 'abap-rap-managed',
  'abap-rap-managed': 'abap-rap-unmanaged',
  'abap-rap-unmanaged': 'abap-rap-extensions',
  'abap-rap-extensions': 'abap-events',
  'abap-clean-core': 'abap-extensibility',
  'abap-fiori': 'abap-odata',
  'abap-odata': 'abap-cap'
};
function colorizeTags(root) {
  (root || document).querySelectorAll('[data-tag]').forEach(function(el) {
    var t = el.getAttribute('data-tag');
    var h = 0; for (var i = 0; i < t.length; i++) h = ((h << 5) - h) + t.charCodeAt(i);
    var c = _TAG_COLORS[Math.abs(h) % _TAG_COLORS.length];
    el.style.setProperty('--tag-color', c);
    el.style.setProperty('--tag-bg', c + '1A');
    if (document.documentElement.classList.contains('dark')) el.style.setProperty('--tag-bg', c + '2E');
  });
}
function getBookmarks() { try { return JSON.parse(localStorage.getItem('ab_bookmarks')) || []; } catch (e) { return []; } }
function saveBookmarks(bookmarks) { localStorage.setItem('ab_bookmarks', JSON.stringify(bookmarks)); }
function getProgress() { try { return JSON.parse(localStorage.getItem('ab_progress')) || []; } catch (e) { return []; } }
function saveProgress(progress) { localStorage.setItem('ab_progress', JSON.stringify(progress)); }
function toggleBookmark(hash) {
  var bookmarks = getBookmarks();
  var index = bookmarks.indexOf(hash);
  if (index > -1) bookmarks.splice(index, 1); else bookmarks.push(hash);
  saveBookmarks(bookmarks);
  updateBookmarkUI(hash); updateSidebarBookmarks(); updateSidebarLinksUI();
}
window.toggleBookmark = toggleBookmark;
function toggleProgress(hash) {
  var progress = getProgress();
  var index = progress.indexOf(hash);
  if (index > -1) progress.splice(index, 1); else progress.push(hash);
  saveProgress(progress);
  updateProgressUI(hash); updateSidebarProgress(); updateSidebarLinksUI();
}
window.toggleProgress = toggleProgress;
function updateBookmarkUI(hash) {
  if (window.location.hash !== hash && (window.location.hash || '#faang-mindset') !== hash) return;
  var btn = document.getElementById('btn-bookmark');
  if (!btn) return;
  var isBookmarked = getBookmarks().includes(hash);
  var icon = btn.querySelector('.material-symbols-outlined');
  if (icon) {
    icon.textContent = isBookmarked ? 'star' : 'star_border';
    if (isBookmarked) { btn.classList.add('text-amber-500','border-amber-500/40','bg-amber-500/5'); btn.classList.remove('text-slate-400'); }
    else { btn.classList.remove('text-amber-500','border-amber-500/40','bg-amber-500/5'); btn.classList.add('text-slate-400'); }
  }
}
function updateProgressUI(hash) {
  if (window.location.hash !== hash && (window.location.hash || '#faang-mindset') !== hash) return;
  var btn = document.getElementById('btn-progress');
  if (!btn) return;
  var isCompleted = getProgress().includes(hash);
  var icon = btn.querySelector('.material-symbols-outlined');
  var text = btn.querySelector('.progress-btn-text');
  if (icon && text) {
    icon.textContent = isCompleted ? 'check_circle' : 'circle';
    text.textContent = isCompleted ? 'Completed' : 'Mark as Done';
    if (isCompleted) { icon.classList.add('text-emerald-500'); icon.classList.remove('text-slate-400'); btn.classList.add('text-emerald-600','border-emerald-500/40','bg-emerald-500/5'); }
    else { icon.classList.remove('text-emerald-500'); icon.classList.add('text-slate-400'); btn.classList.remove('text-emerald-600','border-emerald-500/40','bg-emerald-500/5'); }
  }
}
function updateSidebarProgress() {
  var progress = getProgress();
  var total = Object.keys(window.__ROUTE_MAP || {}).length;
  var completedCount = progress.filter(function(hash) { return window.__ROUTE_MAP[hash]; }).length;
  var percentage = total > 0 ? Math.round((completedCount / total) * 100) : 0;
  var textEl = document.getElementById('sidebar-progress-text');
  var barEl = document.getElementById('sidebar-progress-bar');
  var statsEl = document.getElementById('sidebar-progress-stats');
  if (textEl) textEl.textContent = percentage + '%';
  if (barEl) barEl.style.width = percentage + '%';
  if (statsEl) statsEl.textContent = completedCount + ' of ' + total + ' topics completed';
}
function updateSidebarBookmarks() {
  var bookmarks = getBookmarks();
  var container = document.getElementById('sidebar-bookmarks-container');
  var list = document.getElementById('sidebar-bookmarks-list');
  if (!container || !list) return;
  var validBookmarks = bookmarks.filter(function(hash) { return window.__ROUTE_MAP[hash]; });
  if (validBookmarks.length === 0) { container.classList.add('hidden'); return; }
  container.classList.remove('hidden');
  list.innerHTML = validBookmarks.map(function(hash) {
    var title = hash.replace('#','');
    var entry = (window.__SEARCH_INDEX || []).find(function(e) { return e.url === 'docs.html' + hash; });
    if (entry) { title = entry.title; if (title.length > 24) title = title.substring(0,22)+'...'; }
    return '<a href="'+hash+'" class="sidebar-link !py-1 flex items-center justify-between hover:text-brand-500"><span class="truncate">'+title+'</span><span class="material-symbols-outlined text-[12px] text-amber-500">star</span></a>';
  }).join('');
}
function updateSidebarLinksUI() {
  var progress = getProgress();
  document.querySelectorAll('.sidebar-link').forEach(function(link) {
    var href = link.getAttribute('href');
    if (!href || !href.startsWith('#')) return;
    var isCompleted = progress.includes(href);
    var checkIndicator = link.querySelector('.completion-indicator');
    if (isCompleted) {
      if (!checkIndicator) {
        checkIndicator = document.createElement('span');
        checkIndicator.className = 'completion-indicator material-symbols-outlined text-[13px] text-emerald-500 ml-auto shrink-0';
        checkIndicator.textContent = 'check_circle';
        link.appendChild(checkIndicator);
      } else { checkIndicator.classList.remove('hidden'); }
    } else { if (checkIndicator) checkIndicator.classList.add('hidden'); }
  });
}
function calculateReadingTimeAndDifficulty(data) {
  var text = data.description || '';
  if (data.details) text += ' ' + data.details;
  if (data.sections) data.sections.forEach(function(s) { if (s.title) text += ' ' + s.title; if (s.description) text += ' ' + s.description; if (s.codeBlock) text += ' ' + s.codeBlock; });
  var cleanText = text.replace(/<[^>]*>/g, ' ');
  var words = cleanText.split(/\s+/).filter(function(w) { return w.length > 0; }).length;
  var codeBlocksCount = 0;
  if (data.sections) data.sections.forEach(function(s) { if (s.codeBlock) codeBlocksCount++; });
  if (data.codeBlock) codeBlocksCount++;
  var readingMinutes = Math.max(1, Math.round((words / 200) + (codeBlocksCount * 0.25)));
  var tags = (data.tags || []).map(function(t) { return t.toLowerCase(); });
  var title = (data.title || '').toLowerCase();
  var isAdvanced = tags.includes('faang') || tags.includes('staff+') || tags.includes('scale') || tags.includes('distributed systems') || title.includes('staff+') || title.includes('distributed');
  var isIntermediate = !isAdvanced && (tags.includes('system design') || tags.includes('architecture') || title.includes('system design') || title.includes('database'));
  var difficulty = 'Foundational', diffColor = 'text-emerald-500 border-emerald-500/20 dark:border-emerald-500/30 bg-emerald-550/5', diffIcon = 'signal_cellular_1_bar';
  if (isAdvanced) { difficulty = 'Advanced / Staff+'; diffColor = 'text-purple-500 border-purple-500/20 dark:border-purple-500/30 bg-purple-550/5'; diffIcon = 'signal_cellular_4_bar'; }
  else if (isIntermediate) { difficulty = 'Intermediate'; diffColor = 'text-amber-500 border-amber-500/20 dark:border-amber-500/30 bg-amber-550/5'; diffIcon = 'signal_cellular_3_bar'; }
  return { time: readingMinutes, difficulty: difficulty, diffColor: diffColor, diffIcon: diffIcon };
}
function getRelatedTopics(currentHash, currentTags, currentCategory) {
  if (!currentTags || currentTags.length === 0) return [];
  var searchIndex = window.__SEARCH_INDEX || [];
  var currentUrl = 'docs.html' + currentHash;
  var related = [];
  searchIndex.forEach(function(item) {
    if (item.url === currentUrl) return;
    var common = 0;
    (item.tags || []).forEach(function(t) { if (currentTags.includes(t)) common++; });
    if (common > 0) related.push({ item: item, score: common + (item.category === currentCategory ? 0.5 : 0) });
  });
  related.sort(function(a,b) { return b.score - a.score; });
  return related.slice(0,3).map(function(r) { return r.item; });
}
function renderRelatedTopics(currentHash, currentTags, currentCategory) {
  var related = getRelatedTopics(currentHash, currentTags, currentCategory);
  if (related.length === 0) return '';
  var cards = related.map(function(item) {
    var hash = item.url.substring(item.url.indexOf('#'));
    return '<a href="'+hash+'" class="related-topic-card flex flex-col gap-2 p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0E1115] group cursor-pointer"><span class="text-[9px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">'+item.category+'</span><h4 class="text-sm font-semibold text-slate-900 dark:text-white group-hover:text-brand-500 transition-colors">'+item.title+'</h4><p class="text-xs text-slate-500 dark:text-slate-400 line-clamp-2 flex-1">'+item.description+'</p><span class="text-xs font-semibold text-brand-500 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 mt-1">Read Guide<span class="material-symbols-outlined text-[13px]">arrow_forward</span></span></a>';
  }).join('');
  return '<div class="mt-8 border-t border-slate-200 dark:border-slate-800 pt-6"><h3 class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-4 flex items-center gap-1.5 select-none"><span class="material-symbols-outlined text-[16px] text-brand-500">grid_view</span> Related Study Guides</h3><div class="grid grid-cols-1 sm:grid-cols-3 gap-4">'+cards+'</div></div>';
}
function renderPrerequisites(hash) {
  var prereqs = PREREQUISITES[hash.replace('#','')];
  if (!prereqs || prereqs.length === 0) return '';
  var progress = getProgress();
  var html = '<div class="flex flex-wrap items-center gap-2 mb-4 p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/20"><span class="material-symbols-outlined text-[16px] text-amber-500">account_tree</span><span class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Prerequisites:</span>';
  prereqs.forEach(function(id) {
    var entry = (window.__SEARCH_INDEX || []).find(function(e) { return e.url === 'docs.html#' + id; });
    var title = entry ? entry.title : id;
    var done = progress.includes('#' + id);
    var cls = done ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700';
    var icon = done ? 'check_circle' : 'radio_button_unchecked';
    html += '<a href="#'+id+'" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md border text-xs font-medium transition-all hover:border-brand-500 hover:text-brand-500 '+cls+'"><span class="material-symbols-outlined text-[12px]">'+icon+'</span>'+title+'</a>';
  });
  html += '</div>';
  return html;
}
function renderStudyPlannerLink(hash, title) {
  return '<a href="study-planner.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-brand-500 hover:border-brand-500/30 transition-all bg-white dark:bg-slate-900"><span class="material-symbols-outlined text-[14px]">calendar_month</span> Add "'+title+'" to Study Plan</a>';
}
function renderNextUp(hash) {
  var nextId = NEXT_UP[hash.replace('#','')];
  if (!nextId) return '';
  var entry = (window.__SEARCH_INDEX || []).find(function(e) { return e.url === 'docs.html#' + nextId; });
  if (!entry) return '';
  return '<div class="mt-8 border-t border-slate-200 dark:border-slate-800 pt-6"><div class="flex items-center justify-between p-4 rounded-xl border border-brand-500/20 bg-brand-500/5"><div class="flex flex-col gap-1"><span class="text-[10px] font-bold text-brand-500 uppercase tracking-wider flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">arrow_forward</span> Up Next</span><span class="text-sm font-semibold text-slate-900 dark:text-white">'+entry.title+'</span><span class="text-xs text-slate-500 dark:text-slate-400">'+entry.description+'</span></div><a href="docs.html#'+nextId+'" class="shrink-0 inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-brand-500 text-white text-sm font-semibold hover:bg-brand-hover transition-all"><span>Start</span><span class="material-symbols-outlined text-[16px]">arrow_forward</span></a></div></div>';
}
async function fetchWithCache(path) {
  var cacheKey = 'ab:' + path;
  try { var cached = sessionStorage.getItem(cacheKey); if (cached) { var parsed = JSON.parse(cached); if (parsed && typeof parsed === 'object') return parsed; } } catch (e) {}
  var res = await fetch(path);
  if (!res.ok) throw new Error('Failed to fetch content');
  var data = await res.json();
  try { sessionStorage.setItem(cacheKey, JSON.stringify(data)); } catch (e) {}
  return data;
}
const COPY_BTN = '<button onclick="copyCode(this)" class="absolute right-3 top-3 opacity-0 group-hover:opacity-100 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 px-2.5 py-1.5 rounded-lg text-xs font-sans text-slate-500 transition-all flex items-center gap-1.5"><span class="material-symbols-outlined text-sm" aria-hidden="true">content_copy</span> Copy</button>';
function codeBlock(code, langClass) {
  return '<div class="border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 rounded-xl p-5 text-sm leading-relaxed overflow-x-auto relative group">'+COPY_BTN+'<pre><code class="'+langClass+'">'+escapeHtml(code)+'</code></pre></div>';
}
function renderComparisonTable(table) {
  if (!table || !table.headers || !table.rows) return '';
  var headers = table.headers.map(function(h) { return '<th class="px-4 py-3 text-left text-[11px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider bg-slate-50 dark:bg-slate-800/40 border-b border-slate-200 dark:border-slate-800">'+h+'</th>'; }).join('');
  var rows = table.rows.map(function(row, ri) {
    var cells = row.map(function(cell, ci) {
      var cls = ci === 0 ? 'font-semibold text-slate-900 dark:text-white whitespace-nowrap' : 'text-slate-600 dark:text-slate-400';
      return '<td class="px-4 py-3 text-sm '+cls+' border-b border-slate-100 dark:border-slate-800/60">'+cell+'</td>';
    }).join('');
    return '<tr class="hover:bg-slate-50 dark:hover:bg-slate-800/20 transition-colors">'+cells+'</tr>';
  }).join('');
  return '<div class="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800 my-3"><table class="w-full min-w-[500px]"><thead><tr>'+headers+'</tr></thead><tbody>'+rows+'</tbody></table></div>';
}
function renderDiffTable(table) {
  if (!table || !table.headers || !table.rows) return '';
  var headers = table.headers.map(function(h) { return '<th class="px-4 py-3 text-left text-[11px] font-bold uppercase tracking-wider bg-slate-50 dark:bg-slate-800/40 border-b border-slate-200 dark:border-slate-800 '+(h === 'Before' ? 'text-red-400' : h === 'After' ? 'text-emerald-400' : 'text-slate-400 dark:text-slate-500')+'">'+h+'</th>'; }).join('');
  var rows = table.rows.map(function(row) {
    var cells = row.map(function(cell, ci) {
      var cls = ci === 0 ? 'font-semibold text-slate-900 dark:text-white whitespace-nowrap' : '';
      if (ci === 1) cls += ' bg-red-50 dark:bg-red-950/10 text-red-600 dark:text-red-400';
      if (ci === 2) cls += ' bg-emerald-50 dark:bg-emerald-950/10 text-emerald-600 dark:text-emerald-400';
      return '<td class="px-4 py-3 text-sm '+cls+' border-b border-slate-100 dark:border-slate-800/60">'+cell+'</td>';
    }).join('');
    return '<tr class="transition-colors">'+cells+'</tr>';
  }).join('');
  return '<div class="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800 my-3"><table class="w-full min-w-[500px]"><thead><tr>'+headers+'</tr></thead><tbody>'+rows+'</tbody></table></div>';
}
function renderX(cfg, cls, icon, label) {
  if (!cfg) return '';
  var h = '<div class="pedagogy-block '+cls+'"><div class="pedagogy-header"><span class="material-symbols-outlined">'+icon+'</span>'+label+'</div>';
  if (cfg.prompt) h += '<div class="pedagogy-prompt">'+cfg.prompt+'</div>';
  return h;
}
function renderDecisionTree(dt) {
  if (!dt) return '';
  var h = renderX(dt, 'dt-block', 'account_tree', 'Decision Framework');
  if (dt.firstQuestion) h += '<div class="dt-first-q"><strong>First question to ask yourself:</strong> '+dt.firstQuestion+'</div>';
  if (dt.branches) {
    h += '<div class="dt-branches">'+dt.branches.map(function(b) {
      return '<div class="dt-branch'+(b.selected ? ' dt-branch-selected' : '')+'"><div class="dt-condition">'+b.condition+'</div><div class="dt-path">'+b.path+'</div></div>';
    }).join('')+'</div>';
  }
  if (dt.staffPlusTip) h += '<div class="pedagogy-tip"><span class="material-symbols-outlined">psychology</span> <span>'+dt.staffPlusTip+'</span></div>';
  return h + '</div>';
}
function renderQuantifiedTradeoff(qt) {
  if (!qt) return '';
  var h = renderX(qt, 'qt-block', 'calculate', 'Quantified Tradeoff');
  if (qt.variables) {
    h += '<div class="qt-vars"><strong>Variables:</strong><ul>'+qt.variables.map(function(v) {
      return '<li><span class="qt-var-name">'+v.name+'</span> = <span class="qt-var-value">'+v.value+'</span> <span class="qt-var-source">('+v.source+')</span></li>';
    }).join('')+'</ul></div>';
  }
  if (qt.calculation) {
    h += '<div class="qt-calc"><strong>Calculation:</strong> '+qt.calculation.formula;
    if (qt.calculation.cp) h += '<div class="qt-scenario dt-branch"><span class="dt-condition">CP path:</span><span class="dt-path">Latency '+(qt.calculation.cp.writeLatency||'?')+', cost '+(qt.calculation.cp.monthlyPenalty||'?')+'</span></div>';
    if (qt.calculation.ap) h += '<div class="qt-scenario dt-branch"><span class="dt-condition">AP path:</span><span class="dt-path">Latency '+(qt.calculation.ap.writeLatency||'?')+', cost '+(qt.calculation.ap.monthlyPenalty||'?')+'</span></div>';
    if (qt.calculation.breakeven) h += '<div class="qt-breakeven"><strong>Breakeven:</strong> '+qt.calculation.breakeven+'</div>';
    h += '</div>';
  }
  return h + '</div>';
}
function renderAmbiguityScaffold(as) {
  if (!as) return '';
  var h = renderX(as, 'as-block', 'my_location', 'Ambiguity Scaffold — First 60 Seconds');
  if (as.first60seconds) h += '<div class="as-transcript"><div class="as-candidate-label">You say:</div><div class="as-candidate-text">'+as.first60seconds+'</div></div>';
  if (as.assumptions) {
    h += '<div class="as-section"><strong>Assumptions I\'m stating upfront:</strong><ul>'+as.assumptions.map(function(a) {
      return '<li>'+a+'</li>';
    }).join('')+'</ul></div>';
  }
  if (as.deferred) h += '<div class="as-deferred"><strong>Intentionally deferring:</strong> '+as.deferred+'</div>';
  return h + '</div>';
}
function renderOrganizationalDimension(od) {
  if (!od) return '';
  var h = renderX(od, 'od-block', 'groups', 'Organizational & Adoption Dimension');
  if (od.migrationStrategy) h += '<div class="od-section"><div class="od-subhead">Migration Strategy</div><p>'+od.migrationStrategy+'</p></div>';
  if (od.stakeholders) {
    h += '<div class="od-section"><div class="od-subhead">Stakeholder Concerns</div>'+od.stakeholders.map(function(s) {
      return '<details class="od-stakeholder"><summary><span>'+s.who+'</span><span class="od-concern">Concern: '+s.concern+'</span></summary><div class="od-address"><strong>How to address:</strong> '+s.address+'</div></details>';
    }).join('')+'</div>';
  }
  return h + '</div>';
}
function renderAdversarialResponse(ar) {
  if (!ar) return '';
  var h = renderX(ar, 'ar-block', 'swords', 'Handling Interviewer Pushback');
  if (ar.challenge) h += '<div class="ar-challenge"><div class="ar-interviewer-label">Interviewer:</div><div class="ar-interviewer-text">'+ar.challenge+'</div></div>';
  if (ar.badResponse) h += '<div class="ar-bad"><div class="ar-response-label">Weak response:</div><div class="ar-response-text">'+ar.badResponse+'</div></div>';
  if (ar.goodResponse) h += '<div class="ar-good"><div class="ar-response-label">Staff+ response:</div><div class="ar-response-text">'+ar.goodResponse+'</div></div>';
  if (ar.pattern) h += '<div class="ar-pattern"><strong>Pattern:</strong> '+ar.pattern+'</div>';
  return h + '</div>';
}
function renderSections(sections, dataId, langClass, extraClass) {
  if (!sections) return '';
  return '<div class="flex flex-col gap-8'+(extraClass||'')+'">'+sections.map(function(section, idx) {
    var sectionId = 'section-'+dataId+'-'+idx;
    var refClass = '';
    if (section.title.indexOf('References') !== -1) refClass = ' references-section';
    var sectionLangClass = section.language ? 'language-'+section.language : langClass;
    var extra = '';
    if (section.comparisonTable) extra += renderComparisonTable(section.comparisonTable);
    if (section.diffTable) extra += renderDiffTable(section.diffTable);
    if (section.decisionTree) extra += renderDecisionTree(section.decisionTree);
    if (section.quantifiedTradeoff) extra += renderQuantifiedTradeoff(section.quantifiedTradeoff);
    if (section.ambiguityScaffold) extra += renderAmbiguityScaffold(section.ambiguityScaffold);
    if (section.organizationalDimension) extra += renderOrganizationalDimension(section.organizationalDimension);
    if (section.adversarialResponse) extra += renderAdversarialResponse(section.adversarialResponse);
    return '<div id="'+sectionId+'" class="scroll-mt-24 flex flex-col gap-3'+refClass+'"><h3 class="text-xl font-semibold text-slate-900 dark:text-white">'+section.title+'</h3>'+(section.description ? '<div class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">'+renderDescription(section.description)+'</div>' : '')+(section.codeBlock ? codeBlock(section.codeBlock, sectionLangClass) : '')+extra+'</div>';
  }).join('\n')+'</div>';
}
async function loadContent(hash) {
  if (window._scrollSpyCleanup) { window._scrollSpyCleanup(); window._scrollSpyCleanup = null; }
  var path = (window.__ROUTE_MAP || {})[hash] || (window.__ROUTE_MAP || {})['#faang-mindset'];
  var contentArea = document.getElementById('docs-dynamic-content');
  if (!contentArea) return;
  contentArea.innerHTML = '<div class="animate-pulse space-y-6"><div class="h-8 bg-slate-200 dark:bg-slate-800 rounded w-3/4"></div><div class="h-4 bg-slate-200 dark:bg-slate-800 rounded w-1/2"></div><div class="h-40 bg-slate-200 dark:bg-slate-800 rounded"></div><div class="h-4 bg-slate-200 dark:bg-slate-800 rounded w-5/6"></div></div>';
  var left = document.getElementById('left-sidebar');
  var outline = document.getElementById('docs-right-outline');
  if (left) left.style.display = '';
  if (outline) outline.parentElement.style.display = '';
  var mainEl = document.querySelector('main');
  if (mainEl) { mainEl.classList.remove('max-w-4xl'); mainEl.classList.add('max-w-3xl'); }
  try {
    var data = await fetchWithCache(path);
    var langClass = data.language ? 'language-'+data.language : (data.language === 'abap' ? 'language-abap' : 'text-slate-800 dark:text-slate-200');
    var embedCode = '';
    if (data.sections) embedCode = renderSections(data.sections, data.id, langClass, '');
    else if (data.timeline) {
      var items = '';
      for (var ti = 0; ti < data.timeline.length; ti++) {
        var t = data.timeline[ti]; var delay = ti * 80;
        items += '<div class="timeline-entry" style="animation-delay: '+delay+'ms"><div class="timeline-dot"><span class="timeline-dot-year">'+t.year+'</span><span class="timeline-dot-ring"></span></div><div class="timeline-body"><div class="flex items-center gap-2 mb-1"><h4 class="timeline-title">'+(t.title||'')+'</h4><span class="timeline-tag">'+(t.tag||'Release')+'</span></div><p class="timeline-event">'+t.event+'</p></div></div>';
      }
      embedCode = '<div id="section-syntax" class="scroll-mt-24 mt-4"><div class="timeline-track">'+items+'</div></div>';
    } else embedCode = '<div id="section-syntax" class="scroll-mt-24">'+(data.codeBlock ? codeBlock(data.codeBlock, langClass) : '')+'</div>';
    var meta = calculateReadingTimeAndDifficulty(data);
    var relatedHtml = renderRelatedTopics(hash, data.tags, data.category);
    var prereqHtml = renderPrerequisites(hash);
    var plannerLink = renderStudyPlannerLink(hash, data.title);
    var nextUpHtml = renderNextUp(hash);
    contentArea.innerHTML = '<article class="flex flex-col gap-5 docs-section" role="region" aria-label="'+(data.title||'')+'"><div class="flex flex-col gap-3"><div class="flex items-center justify-between gap-4 flex-wrap select-none"><nav class="flex items-center gap-1.5 text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider"><span>'+data.category+'</span><span class="material-symbols-outlined text-[12px] text-slate-300 dark:text-slate-700">chevron_right</span><span class="text-brand-500">'+(data.subcategory||'Overview')+'</span></nav><div class="flex items-center gap-2" id="article-actions-toolbar"><button onclick="toggleBookmark(\''+hash+'\')" id="btn-bookmark" class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-400 hover:text-amber-500 hover:border-amber-500/30 flex items-center justify-center transition-all bg-white dark:bg-slate-900" aria-label="Pin this guide"><span class="material-symbols-outlined text-[18px]">star_border</span></button><button onclick="toggleProgress(\''+hash+'\')" id="btn-progress" class="h-8 px-3 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-500 hover:text-emerald-500 hover:border-emerald-500/30 flex items-center gap-1.5 text-[11px] font-semibold transition-all bg-white dark:bg-slate-900"><span class="material-symbols-outlined text-[16px] text-slate-400">circle</span><span class="progress-btn-text">Mark as Done</span></button><button onclick="window.print()" class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-400 hover:text-brand-500 hover:border-brand-500/30 flex items-center justify-center transition-all bg-white dark:bg-slate-900" aria-label="Print"><span class="material-symbols-outlined text-[18px]">print</span></button></div></div><h1 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-white tracking-tight">'+data.title+'</h1><div class="flex flex-wrap items-center gap-3 text-xs text-slate-500 dark:text-slate-400 select-none"><span class="inline-flex items-center gap-1"><span class="material-symbols-outlined text-[16px] text-slate-405">schedule</span><span>'+meta.time+' min read</span></span><span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border text-[10px] font-bold uppercase tracking-wider '+meta.diffColor+'"><span class="material-symbols-outlined text-[12px]">'+meta.diffIcon+'</span><span>'+meta.difficulty+'</span></span>'+plannerLink+'</div>'+(data.tags && data.tags.length > 0 ? '<div class="flex flex-wrap gap-1.5 mt-0.5">'+data.tags.map(function(t) { return '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider tag-badge cursor-default" data-tag="'+t+'">'+t+'</span>'; }).join('')+'</div>' : '')+'</div><p class="text-slate-600 dark:text-slate-400 leading-relaxed text-base">'+data.description+'</p>'+prereqHtml+embedCode+(data.details ? '<div id="section-dive" class="scroll-mt-24"><details class="group border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40 rounded-xl overflow-hidden transition-all duration-300"><summary class="flex items-center justify-between p-4 font-bold text-sm text-slate-800 dark:text-slate-200 cursor-pointer select-none list-none [&::-webkit-details-marker]:hidden"><span class="flex items-center gap-2"><span class="material-symbols-outlined text-[18px] text-brand-500">lightbulb</span><span>Staff+ Deep Dive</span></span><span class="material-symbols-outlined text-[18px] transition-transform duration-200 group-open:rotate-180 text-slate-400">expand_more</span></summary><div class="px-5 pb-5 pt-2 text-slate-600 dark:text-slate-400 text-sm leading-relaxed border-t border-slate-100 dark:border-slate-800/60 font-sans">'+data.details+'</div></details></div>' : '')+relatedHtml+nextUpHtml+'</article>';
    updateBookmarkUI(hash); updateProgressUI(hash); updateSidebarProgress(); updateSidebarBookmarks(); updateSidebarLinksUI();
    addCopyButtonsToPreElements(contentArea);
    colorizeTags(contentArea);
    document.querySelectorAll('.sidebar-section').forEach(function(s) { s.classList.remove('section-active'); });
    document.querySelectorAll('.sidebar-link').forEach(function(link) {
      if (link.getAttribute('href') === hash) { link.classList.add('active-doc-link'); link.setAttribute('aria-current','page'); var section = link.closest('.sidebar-section'); if (section) section.classList.add('section-active'); }
      else { link.classList.remove('active-doc-link'); link.removeAttribute('aria-current'); }
    });
    var outlineArea = document.getElementById('docs-right-outline');
    if (outlineArea) {
      if (data.sections) {
        var outlineHtml = data.sections.map(function(section, idx) { return '<a href="#section-'+data.id+'-'+idx+'" class="outline-link">'+section.title+'</a>'; }).join('\n');
        if (data.details) outlineHtml += '\n<a href="#section-dive" class="outline-link">Staff+ Deep Dive</a>';
        outlineArea.innerHTML = outlineHtml;
      } else { outlineArea.innerHTML = '<a href="#section-syntax" class="outline-link">Syntax Guide</a>'+(data.details?'\n<a href="#section-dive" class="outline-link">Staff+ Deep Dive</a>':''); }
      setupOutlineSmoothScroll();
      window._scrollSpyCleanup = setupOutlineScrollSpy();
    }
    if (contentArea.querySelector('pre code') && typeof Prism !== 'undefined') Prism.highlightAllUnder(contentArea);
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        var article = contentArea.querySelector('article');
        if (article) article.classList.add('anim-ready');
        if (data.sections) data.sections.forEach(function(_, idx) { var sec = document.getElementById('section-'+data.id+'-'+idx); if (sec) sec.classList.add('anim-ready'); });
        var syntax = document.getElementById('section-syntax'); if (syntax) syntax.classList.add('anim-ready');
        var dive = document.getElementById('section-dive');
        if (dive) {
          if (dive.getBoundingClientRect().top < window.innerHeight) dive.classList.add('anim-ready');
          else { var obs = new IntersectionObserver(function(entries) { entries.forEach(function(entry) { if (entry.isIntersecting) { entry.target.classList.add('anim-ready'); obs.unobserve(entry.target); } }); }, { threshold: 0.15 }); obs.observe(dive); }
        }
      });
    });
  } catch (error) {
    console.error("Error in loadContent:", error);
    contentArea.innerHTML = '<div class="p-6 border-2 border-red-200 dark:border-red-900/30 bg-red-50 dark:bg-red-950/10 rounded-xl text-red-600 dark:text-red-400 text-sm"><h3 class="font-bold mb-1">Error Loading Document</h3><p>Failed to load from path: '+path+'. Error: '+error.message+'</p></div>';
  }
}
function setupOutlineSmoothScroll() {
  var outline = document.getElementById('docs-right-outline');
  if (!outline) return;
  outline.addEventListener('click', function(e) {
    var link = e.target.closest('.outline-link');
    if (!link) return;
    var targetId = link.getAttribute('href');
    var targetElement = document.querySelector(targetId);
    if (targetElement) { e.preventDefault(); targetElement.scrollIntoView({ behavior:'smooth', block:'start' }); document.querySelectorAll('.outline-link').forEach(function(l) { l.classList.toggle('active-outline', l.getAttribute('href')===targetId); }); }
  });
}
function setupOutlineScrollSpy() {
  var links = document.querySelectorAll('.outline-link');
  if (links.length === 0) return null;
  var sections = Array.from(links).map(function(link) { return document.querySelector(link.getAttribute('href')); }).filter(Boolean);
  if (sections.length === 0) return null;
  function updateActiveLink() {
    var scrollPosition = window.scrollY + 120;
    if ((window.innerHeight + window.scrollY) >= document.documentElement.scrollHeight - 50) { links.forEach(function(link, idx) { link.classList.toggle('active-outline', idx === links.length-1); }); return; }
    var activeSection = null;
    for (var i = 0; i < sections.length; i++) { var section = sections[i]; if (section.offsetTop <= scrollPosition) activeSection = section; else break; }
    if (!activeSection && sections.length > 0) activeSection = sections[0];
    if (activeSection) { var activeId = activeSection.getAttribute('id'); links.forEach(function(link) { link.classList.toggle('active-outline', link.getAttribute('href')==='#'+activeId); }); }
  }
  var ticking = false;
  var onScroll = function() { if (!ticking) { requestAnimationFrame(function() { updateActiveLink(); ticking = false; }); ticking = true; } };
  window.addEventListener('scroll', onScroll, { passive: true });
  updateActiveLink();
  return function() { window.removeEventListener('scroll', onScroll); };
}
function escapeHtml(text) {
  if (typeof text !== 'string') return '';
  return text.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#039;");
}
function renderDescription(desc) {
  if (!desc) return '';
  if (typeof desc === 'string') return desc;
  if (Array.isArray(desc)) {
    return desc.map(function(item) {
      if (typeof item === 'string') return item;
      if (item && item.type === 'svg') return item.value || '';
      if (item && item.type === 'text') return item.value || '';
      if (item && item.type === 'code') return '<div class="border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 rounded-xl p-4 text-sm overflow-x-auto my-2"><pre><code class="language-abap">'+escapeHtml(item.value||'')+'</code></pre></div>';
      if (item && item.value) return item.value;
      return '';
    }).join('\n');
  }
  if (desc && desc.value) return desc.value;
  return String(desc);
}
window.copyCode = function(btn) {
  var codeEl = btn.parentElement.querySelector('code');
  if (!codeEl) return;
  navigator.clipboard.writeText(codeEl.textContent).then(function() {
    var originalHTML = btn.innerHTML;
    btn.innerHTML = '<span class="material-symbols-outlined text-sm text-emerald-500">check</span> Copied!';
    btn.disabled = true;
    var toast = document.getElementById('clipboard-toast');
    if (!toast) {
      toast = document.createElement('div'); toast.id = 'clipboard-toast';
      toast.className = 'fixed bottom-6 right-6 z-50 flex items-center gap-2.5 bg-slate-900/90 dark:bg-slate-800/90 backdrop-blur-md text-white border border-slate-700/50 px-4 py-2.5 rounded-xl shadow-xl text-sm font-sans font-medium';
      document.body.appendChild(toast);
    }
    toast.innerHTML = '<span class="material-symbols-outlined text-[18px] text-emerald-400" aria-hidden="true">check_circle</span><span>Code copied!</span>';
    toast.style.transition = 'all 0.3s'; toast.style.opacity = '0'; toast.style.transform = 'translateY(10px)';
    requestAnimationFrame(function() { toast.style.opacity = '1'; toast.style.transform = 'translateY(0)'; });
    setTimeout(function() { toast.style.opacity = '0'; toast.style.transform = 'translateY(10px)'; }, 2000);
    setTimeout(function() { btn.innerHTML = originalHTML; btn.disabled = false; }, 2000);
  }).catch(function(err) { console.error('Failed to copy: ', err); });
};
function addCopyButtonsToPreElements(container) {
  (container || document).querySelectorAll('pre').forEach(function(pre) {
    if (pre.parentElement.classList.contains('group') && pre.parentElement.querySelector('button[onclick*="copyCode"]')) return;
    if (!pre.querySelector('code')) return;
    if (pre.classList.contains('copy-btn-initialized')) return;
    pre.classList.add('copy-btn-initialized');
    var wrapper = document.createElement('div');
    wrapper.className = 'border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 rounded-xl p-5 text-sm leading-relaxed overflow-x-auto relative group';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);
    var btn = document.createElement('button');
    btn.className = 'absolute right-3 top-3 opacity-0 group-hover:opacity-100 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 px-2.5 py-1.5 rounded-lg text-xs font-sans text-slate-500 transition-all flex items-center gap-1.5';
    btn.innerHTML = '<span class="material-symbols-outlined text-sm" aria-hidden="true">content_copy</span> Copy';
    btn.addEventListener('click', function() { window.copyCode(btn); });
    wrapper.insertBefore(btn, pre);
  });
}
window.addEventListener('DOMContentLoaded', function() {
  var initialHash = window.location.hash || '#faang-mindset';
  loadContent(initialHash);
  updateSidebarProgress(); updateSidebarBookmarks(); updateSidebarLinksUI();
  (function() {
    var bar = document.getElementById('reading-progress-bar');
    if (!bar) return;
    var ticking = false;
    function updateReadingProgress() {
      var article = document.getElementById('docs-dynamic-content');
      if (!article) { bar.style.width = '0%'; ticking = false; return; }
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var articleTop = article.offsetTop || 0;
      var articleHeight = article.scrollHeight || 1;
      var viewportH = window.innerHeight;
      var scrollable = articleTop + articleHeight - viewportH;
      if (scrollable <= 0) { bar.style.width = '100%'; ticking = false; return; }
      var progress = Math.min(100, Math.max(0, ((scrollTop - articleTop + viewportH * 0.1) / scrollable) * 100));
      bar.style.width = progress.toFixed(1) + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function() { if (!ticking) { requestAnimationFrame(updateReadingProgress); ticking = true; } }, { passive: true });
    window.addEventListener('hashchange', function() { setTimeout(updateReadingProgress, 300); });
    updateReadingProgress();
  })();
});
window.addEventListener('hashchange', function() { loadContent(window.location.hash); window.scrollTo({ top: 0, behavior: 'smooth' }); });
window.addEventListener('theme-changed', function() { colorizeTags(); updateSidebarLinksUI(); });
