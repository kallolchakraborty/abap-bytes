(function() {
  var shareHTML = '<div id="share-modal" class="hidden fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm p-4 sm:p-10 justify-center items-center" role="dialog" aria-modal="true" aria-label="Share this page"><div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 w-full max-w-lg rounded-2xl shadow-2xl flex flex-col overflow-hidden"><div class="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50"><h3 class="font-bold text-slate-900 dark:text-white">Share this page</h3><button id="close-share-btn" class="text-xs text-slate-400 border border-slate-200 dark:border-slate-800 px-2.5 py-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">ESC</button></div><div class="p-4 border-b border-slate-200 dark:border-slate-800"><div class="flex items-center gap-2"><input id="share-url-input" type="text" readonly class="w-full bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-600 dark:text-slate-400 font-mono"><button id="copy-share-btn" class="shrink-0 px-3 py-2 bg-brand-500 hover:bg-brand-600 text-white rounded-lg text-sm font-medium transition-all flex items-center gap-1.5"><span class="material-symbols-outlined text-sm" aria-hidden="true">content_copy</span> Copy</button></div><p id="copy-confirm" class="hidden text-xs text-green-600 dark:text-green-400 mt-1.5">Link copied to clipboard!</p></div><div class="p-4"><p class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Share via</p><div class="flex flex-wrap gap-3"><a href="#" data-href="https://twitter.com/intent/tweet?url={url}&text={title}" target="_blank" rel="noopener noreferrer" class="share-link flex items-center justify-center w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-black hover:text-white dark:hover:bg-black transition-all text-slate-600 dark:text-slate-400" aria-label="Share on Twitter/X"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path></svg></a><a href="#" data-href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener noreferrer" class="share-link flex items-center justify-center w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-[#0A66C2] hover:text-white dark:hover:bg-[#0A66C2] transition-all text-slate-600 dark:text-slate-400" aria-label="Share on LinkedIn"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg></a><a href="#" data-href="https://wa.me/?text={title}%20{url}" target="_blank" rel="noopener noreferrer" class="share-link flex items-center justify-center w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-[#25D366] hover:text-white dark:hover:bg-[#25D366] transition-all text-slate-600 dark:text-slate-400" aria-label="Share on WhatsApp"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"></path></svg></a><a href="#" data-href="mailto:?subject={title}&body={url}" target="_blank" rel="noopener noreferrer" class="share-link flex items-center justify-center w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-brand-500 hover:text-white dark:hover:bg-brand-500 transition-all text-slate-600 dark:text-slate-400" aria-label="Share via Email"><span class="material-symbols-outlined text-lg" aria-hidden="true">mail</span></a></div></div></div></div>';
  var searchHTML = '<div id="search-modal" class="hidden fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm p-4 sm:p-10 justify-center items-start" role="dialog" aria-modal="true" aria-label="Search documentation"><div id="search-live-announcer" class="sr-only" aria-live="polite"></div><div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 w-full max-w-4xl rounded-2xl shadow-2xl flex flex-col overflow-hidden mt-10 md:h-[550px] max-h-[85vh]"><div class="search-header-container p-4 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3 bg-slate-50/50 dark:bg-slate-900/50 transition-colors duration-200 shrink-0"><span class="material-symbols-outlined text-slate-400 transition-colors duration-200" aria-hidden="true">search</span><input id="modal-search-input" type="text" placeholder="Type to search study materials..." aria-label="Search query" class="w-full bg-transparent border-none focus:ring-0 text-slate-900 dark:text-white font-sans font-medium placeholder:text-slate-400 focus:outline-none"><button id="close-search-btn" class="text-xs text-slate-400 border border-slate-200 dark:border-slate-800 px-2.5 py-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-all font-sans">ESC</button></div><div class="flex flex-1 overflow-hidden min-h-0"><div id="modal-search-results" class="w-full md:w-1/2 p-4 overflow-y-auto flex flex-col gap-2 border-r border-slate-100 dark:border-slate-800/80" role="listbox" aria-label="Search results"></div><div id="modal-search-preview" class="hidden md:flex md:w-1/2 p-6 overflow-y-auto flex-col bg-slate-50/40 dark:bg-slate-900/40 text-slate-700 dark:text-slate-300 min-w-0"></div></div><div class="p-3 bg-slate-50 dark:bg-slate-800/20 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono shrink-0"><span>↑↓ navigate · enter select · esc close</span><span class="hidden sm:inline">filter: <span class="text-brand-400">cat:</span>CDS · <span class="text-brand-400">tag:</span>Staff+</span></div></div></div>';
  document.body.insertAdjacentHTML('beforeend', shareHTML);
  var hasSearch = document.querySelector('.open-search-btn') !== null;
  if (hasSearch) document.body.insertAdjacentHTML('beforeend', searchHTML);
  var _lastFocusedEl = null;
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.open-share-btn');
    if (!btn) return;
    var modal = document.getElementById('share-modal');
    var input = document.getElementById('share-url-input');
    var confirm = document.getElementById('copy-confirm');
    if (!modal) return;
    _lastFocusedEl = document.activeElement;
    var url = window.location.href;
    var title = document.title || 'ABAP Bytes';
    if (input) input.value = url;
    if (confirm) confirm.classList.add('hidden');
    var encodedUrl = encodeURIComponent(url);
    var encodedTitle = encodeURIComponent(title);
    document.querySelectorAll('.share-link').forEach(function(link) { link.href = (link.getAttribute('data-href')||'').replace('{url}',encodedUrl).replace('{title}',encodedTitle); });
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    if (input) input.focus();
  });
  function closeShareModal() {
    var modal = document.getElementById('share-modal');
    if (!modal) return;
    modal.classList.add('hidden'); modal.classList.remove('flex');
    if (_lastFocusedEl) { _lastFocusedEl.focus(); _lastFocusedEl = null; }
  }
  document.addEventListener('click', function(e) { if (e.target.id === 'close-share-btn' || e.target.closest('#close-share-btn')) closeShareModal(); });
  document.addEventListener('click', function(e) { var modal = document.getElementById('share-modal'); if (!modal || modal.classList.contains('hidden')) return; if (e.target === modal) closeShareModal(); });
  document.addEventListener('click', function(e) {
    var copyBtn = e.target.closest('#copy-share-btn');
    if (!copyBtn) return;
    var input = document.getElementById('share-url-input');
    var confirm = document.getElementById('copy-confirm');
    if (!input) return;
    input.select();
    navigator.clipboard.writeText(input.value).then(function() { if (confirm) { confirm.classList.remove('hidden'); setTimeout(function() { confirm.classList.add('hidden'); },2000); } });
  });
  document.addEventListener('keydown', function(e) {
    var modal = document.getElementById('share-modal');
    if (!modal || modal.classList.contains('hidden')) return;
    if (e.key === 'Escape') closeShareModal();
  });
  if (!hasSearch) return;
  var searchIndex = window.__SEARCH_INDEX || [];
  var _selectedIndex = -1;
  var _searchDebounce = null;
  var _currentResults = [];
  function _escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
  function _levenshtein(a,b) {
    if (a.length===0) return b.length; if (b.length===0) return a.length;
    if (a.length>b.length) { var t=a;a=b;b=t; }
    var row=Array(a.length+1); for(var i=0;i<=a.length;i++) row[i]=i;
    for(var j=1;j<=b.length;j++) { var prev=j; for(var i=1;i<=a.length;i++) { var val; if(b.charAt(j-1)===a.charAt(i-1)) val=row[i-1]; else val=Math.min(row[i-1]+1,prev+1,row[i]+1); row[i-1]=prev; prev=val; } row[a.length]=prev; }
    return row[a.length];
  }
  function _fuzzyScore(text, query) {
    if (!text || !query) return 0;
    var t=text.toLowerCase(), q=query.toLowerCase();
    if (t===q) return 1; if (t.indexOf(q)===0) return 0.92; if (t.indexOf(q)!==-1) return 0.85;
    if (q.length<3) return 0;
    var words=t.split(/\s+/);
    for(var w=0;w<words.length;w++) { if(words[w].indexOf(q)===0) return 0.75; }
    var maxLen=Math.max(t.length,q.length), searchLen=Math.min(t.length,q.length+5), bestDist=Infinity;
    for(var start=0;start<=t.length-searchLen;start++) { var dist=_levenshtein(t.substring(start,start+searchLen),q); if(dist<bestDist) bestDist=dist; }
    if(bestDist===Infinity) return 0;
    return Math.max(0,Math.min(1,1-(bestDist/Math.max(q.length,searchLen))));
  }
  function _bigramSet(s) { var set={}; for(var i=0;i<s.length-1;i++) set[s.substring(i,i+2)]=true; return set; }
  function _diceSimilarity(a,b) { if(!a||!b) return 0; var ba=_bigramSet(a), bb=_bigramSet(b), inter=0; for(var k in ba) { if(ba.hasOwnProperty(k)&&bb.hasOwnProperty(k)) inter++; } var total=Object.keys(ba).length+Object.keys(bb).length; return total===0?0:(2*inter)/total; }
  function _didYouMean(query, candidates) {
    if(!query||query.length<2) return null;
    var q=query.toLowerCase().trim(), best=null, bestScore=0;
    for(var i=0;i<candidates.length;i++) {
      var title=(candidates[i].title||'').toLowerCase();
      if(title===q||title.indexOf(q)!==-1) continue;
      var score=_diceSimilarity(q,title);
      if(score>bestScore){bestScore=score;best=candidates[i].title;}
      if(candidates[i].tags) { for(var t=0;t<candidates[i].tags.length;t++) { var tagScore=_diceSimilarity(q,(candidates[i].tags[t]||'').toLowerCase()); if(tagScore>bestScore){bestScore=tagScore;best=candidates[i].tags[t];} } }
    }
    return bestScore>0.35?best:null;
  }
  function _parseQuery(raw) {
    var filters={}, terms=[];
    if(!raw) return {filters:filters,terms:''};
    var parts=raw.trim().split(/\s+/);
    for(var i=0;i<parts.length;i++) {
      var m=parts[i].match(/^(category|cat|tag|section):(.+)$/i);
      if(m) { var key=m[1].toLowerCase(); if(key==='cat') key='category'; var val=m[2].toLowerCase(); if(!filters[key]) filters[key]=[]; filters[key].push(val); }
      else terms.push(parts[i]);
    }
    return {filters:filters,terms:terms.join(' ')};
  }
  function _matchesFilters(item, filters) {
    for(var key in filters) {
      if(!filters.hasOwnProperty(key)) continue;
      var vals=filters[key], field=(key==='tag'?(item.tags||[]).join(' '):key==='section'?(item.sections||[]).join(' '):(item[key]||'')).toLowerCase();
      for(var v=0;v<vals.length;v++) { if(field.indexOf(vals[v])===-1) return false; }
    }
    return true;
  }
  function _scoreItem(item, query) {
    var q=(query||'').toLowerCase().trim();
    if(!q) return 0;
    var qWords=q.split(/\s+/).filter(Boolean);
    var textToSearch=((item.title||'')+' '+(item.category||'')+' '+(item.description||'')+' '+(item.tags||[]).join(' ')+' '+(item.sections||[]).join(' ')).toLowerCase();
    var hasOverlap=false;
    for(var k=0;k<qWords.length;k++) { if(textToSearch.indexOf(qWords[k])!==-1) { hasOverlap=true; break; } }
    if(!hasOverlap&&q.length>=3) return 0;
    var titleScore=_fuzzyScore(item.title,q)*100, catScore=_fuzzyScore(item.category,q)*50, descScore=_fuzzyScore(item.description||'',q)*20, bestSectionScore=0, bestTagScore=0;
    if(item.sections) { for(var i=0;i<item.sections.length;i++) { var s=_fuzzyScore(item.sections[i],q)*25; if(s>bestSectionScore) bestSectionScore=s; } }
    if(item.tags) { for(var j=0;j<item.tags.length;j++) { var t=_fuzzyScore(item.tags[j],q)*15; if(t>bestTagScore) bestTagScore=t; } }
    var matchedFields=0; if(titleScore>0) matchedFields++; if(catScore>0) matchedFields++; if(descScore>0) matchedFields++; if(bestSectionScore>0) matchedFields++; if(bestTagScore>0) matchedFields++;
    var bonus=matchedFields>=3?15:matchedFields>=2?5:0;
    return titleScore+catScore+descScore+bestSectionScore+bestTagScore+bonus;
  }
  function _highlight(text, query) {
    if(!query||!text) return text||'';
    var q=query.toLowerCase().trim();
    if(!q) return text;
    var words=q.split(/\s+/).filter(function(w){return w.length>=2;});
    if(words.length===0) return text;
    var pattern='('+words.map(_escapeRe).join('|')+')';
    var re=new RegExp('<[^>]*>|'+pattern,'gi');
    return text.replace(re,function(match,p1){ if(p1) return '<mark class="bg-brand-100 dark:bg-brand-500/30 text-inherit rounded-sm px-0.5">'+p1+'</mark>'; return match; });
  }
  function _getSearchHistory() { try { return JSON.parse(localStorage.getItem('__SEARCH_HISTORY'))||[]; } catch(e){return [];} }
  function _addSearchHistory(q) { if(!q||typeof q!=='string') return; q=q.trim().toLowerCase(); if(!q||q.length<2) return; try { var h=JSON.parse(localStorage.getItem('__SEARCH_HISTORY'))||[]; h=h.filter(function(s){return s!==q;}); h.unshift(q); if(h.length>5) h.length=5; localStorage.setItem('__SEARCH_HISTORY',JSON.stringify(h)); } catch(e){} }
  function _clearSearchHistory() { try { localStorage.removeItem('__SEARCH_HISTORY'); } catch(e){} }
  function updateSearchPreview(item) {
    var preview=document.getElementById('modal-search-preview');
    if(!preview) return;
    if(!item) { preview.innerHTML='<div class="flex flex-col items-center justify-center h-full text-center p-6 text-slate-400 dark:text-slate-500"><span class="material-symbols-outlined text-4xl mb-2">find_in_page</span><p class="text-xs font-medium">Select a guide to preview</p></div>'; return; }
    var sectionsHtml=''; if(item.sections&&item.sections.length>0) { sectionsHtml='<div class="mt-4"><h5 class="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">Sections</h5><ul class="space-y-1.5">'+item.sections.map(function(sec){return '<li class="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-450 truncate"><span class="w-1.5 h-1.5 rounded-full bg-brand-500 shrink-0"></span><span>'+sec+'</span></li>';}).join('')+'</ul></div>'; }
    var tagsHtml=''; if(item.tags&&item.tags.length>0) { tagsHtml='<div class="flex flex-wrap gap-1.5 mt-4">'+item.tags.map(function(tag){return '<span class="text-[10px] font-semibold font-mono text-brand-500 dark:text-brand-400 bg-brand-50 dark:bg-brand-500/10 px-2 py-0.5 rounded-lg border border-brand-500/10">#'+tag+'</span>';}).join('')+'</div>'; }
    preview.innerHTML='<div class="flex flex-col h-full justify-between gap-6"><div class="flex flex-col gap-3 min-w-0"><div class="flex items-center gap-1.5"><span class="text-[10px] font-bold text-brand-500 uppercase tracking-wider bg-brand-light px-2.5 py-1 rounded-md">'+item.category+'</span></div><h4 class="text-base font-bold text-slate-800 dark:text-white leading-snug tracking-tight">'+item.title+'</h4><p class="text-xs text-slate-500 dark:text-slate-450 leading-relaxed font-sans mt-1">'+item.description+'</p>'+sectionsHtml+tagsHtml+'</div><a href="'+item.url+'" class="w-full py-2.5 px-4 bg-brand-500 hover:bg-brand-600 text-white rounded-xl text-center text-xs font-semibold tracking-wide transition-all shadow-md shadow-brand-500/10 hover:shadow-brand-500/25 flex items-center justify-center gap-1.5 shrink-0 select-guide-btn"><span>Read Study Guide</span><span class="material-symbols-outlined text-sm font-semibold">arrow_forward</span></a></div>';
    var btn=preview.querySelector('.select-guide-btn'); if(btn) btn.addEventListener('click',function(){ closeSearchModal(); });
  }
  function renderResults(rawQuery) {
    var results=document.getElementById('modal-search-results');
    if(!results) return;
    try {
      var query=(rawQuery||'').trim(), q=query.toLowerCase(), parsed=_parseQuery(query), searchTerms=parsed.terms, filters=parsed.filters;
      if(!q) { _currentResults=[]; updateSearchPreview(null); renderEmptyState(results); return; }
      var filtered=searchIndex.filter(function(item){return _matchesFilters(item,filters);});
      var scored=[];
      for(var i=0;i<filtered.length;i++) { var item=filtered[i], score=_scoreItem(item,searchTerms); if(score>0||(filtered.length>0&&searchTerms.length===0&&Object.keys(filters).length>0)) { if(score===0) score=1; scored.push({item:item,score:Math.round(score)}); } }
      scored.sort(function(a,b){return b.score-a.score;});
      var topItems=scored.slice(0,12);
      if(searchTerms.length>=2&&topItems.length>0) _addSearchHistory(searchTerms);
      _currentResults=topItems.map(function(s){return s.item;});
      var announcer=document.getElementById('search-live-announcer');
      if(announcer) announcer.textContent=topItems.length===0?"No results found.":topItems.length+" results found.";
      if(topItems.length===0) { updateSearchPreview(null); renderNoResults(results,searchTerms,filters,query); return; }
      var hasFilters=Object.keys(filters).length>0, html='';
      if(hasFilters) html+='<div class="text-[10px] font-mono text-slate-400 dark:text-slate-500 px-1 pb-1">Filtered: '+Object.keys(filters).map(function(k){return '<span class="text-brand-500">'+k+':'+filters[k].join(',')+'</span>';}).join(', ')+'</div>';
      html+=topItems.map(function(scored,idx){ var item=scored.item; var titleHtml=_highlight(item.title,searchTerms); var catHtml=_highlight(item.category,searchTerms); return '<a href="'+item.url+'" role="option" class="search-result flex items-center justify-between p-3 bg-slate-50/40 dark:bg-slate-800/20 hover:bg-brand-50 dark:hover:bg-brand-500/10 border border-slate-100/50 dark:border-slate-800/30 hover:border-brand-100 dark:hover:border-brand-500/20 rounded-xl transition-all group" data-index="'+idx+'"><div class="flex items-center gap-3 min-w-0"><span class="material-symbols-outlined text-slate-400 dark:text-slate-500 group-hover:text-brand-500 transition-colors shrink-0">description</span><div class="flex flex-col min-w-0"><span class="text-[9px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">'+catHtml+'</span><span class="font-semibold text-xs text-slate-700 dark:text-slate-200 group-hover:text-brand-500 transition-colors truncate">'+titleHtml+'</span></div></div><span class="material-symbols-outlined text-slate-350 dark:text-slate-650 group-hover:text-brand-500 transition-all transform group-hover:translate-x-0.5 shrink-0 text-sm">chevron_right</span></a>';}).join('');
      results.innerHTML=html;
      _selectedIndex=0; var firstLink=results.querySelector('.search-result'); if(firstLink) { _applySelection(firstLink); } updateSearchPreview(_currentResults[0]);
    } catch(err) { console.error('Search error:',err); results.innerHTML='<div role="status" aria-live="polite" class="p-8 text-center text-red-500 dark:text-red-400 font-mono text-sm">Search encountered an error.</div>'; }
  }
  function renderEmptyState(results) {
    var history=_getSearchHistory();
    var categories={};
    for(var i=0;i<searchIndex.length;i++) { var cat=searchIndex[i].category; if(!categories[cat]) categories[cat]=0; categories[cat]++; }
    var catList=Object.keys(categories).sort();
    var html='';
    if(history.length>0){
      html+='<div class="mb-4"><div class="flex items-center justify-between mb-2"><span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Recent</span><button id="clear-search-history-btn" class="text-[10px] text-slate-400 hover:text-red-500 transition-colors font-mono uppercase tracking-wider">Clear</button></div><div class="flex flex-wrap gap-2">';
      for(var h=0;h<history.length;h++) html+='<button data-history="'+_escapeRe(history[h])+'" class="search-history-chip text-xs text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-brand-50 dark:hover:bg-brand-500/10 px-2.5 py-1 rounded-lg transition-colors">'+_escapeRe(history[h])+'</button>';
      html+='</div></div>';
    }
    html+='<div class="mb-3"><span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Browse by category</span></div><div class="flex flex-wrap gap-2">';
    for(var c=0;c<catList.length;c++) html+='<button data-category="'+_escapeRe(catList[c])+'" class="category-chip text-xs text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-brand-50 dark:hover:bg-brand-500/10 px-2.5 py-1 rounded-lg transition-colors">'+catList[c]+' <span class="text-slate-400">('+categories[catList[c]]+')</span></button>';
    html+='</div><div role="status" aria-live="polite" class="pt-4 pb-1 text-center text-xs text-slate-400 font-mono">'+searchIndex.length+' pages</div>';
    results.innerHTML=html;
    results.querySelectorAll('.search-history-chip').forEach(function(chip){ chip.addEventListener('click',function(){ var input=document.getElementById('modal-search-input'); if(input){input.value=chip.getAttribute('data-history');renderResults(input.value);input.focus();}});});
    results.querySelectorAll('.category-chip').forEach(function(chip){ chip.addEventListener('click',function(){ var input=document.getElementById('modal-search-input'); if(input){input.value='category:'+chip.getAttribute('data-category');renderResults(input.value);input.focus();}});});
    var clearBtn=document.getElementById('clear-search-history-btn'); if(clearBtn) clearBtn.addEventListener('click',function(e){ e.stopPropagation(); _clearSearchHistory(); renderResults(''); });
  }
  function renderNoResults(results, queryTerms, filters, rawQuery) {
    var html='<div class="p-8 text-center font-mono"><span class="material-symbols-outlined text-3xl text-slate-300 dark:text-slate-600 mb-3" aria-hidden="true">search_off</span><p class="text-slate-500 dark:text-slate-400 text-sm mb-1">No matches for <span class="text-slate-700 dark:text-slate-200 font-bold">&ldquo;'+_escapeRe(queryTerms)+'&rdquo;</span></p><p class="text-xs text-slate-400 dark:text-slate-500 mb-4">Try a broader term or check your spelling.</p>';
    if(queryTerms.length>=2) { var suggestion=_didYouMean(queryTerms,searchIndex); if(suggestion) html+='<button data-suggestion="'+_escapeRe(suggestion)+'" class="search-suggestion-chip text-sm text-brand-500 hover:text-brand-600 bg-brand-50 dark:bg-brand-500/10 px-3 py-1.5 rounded-lg transition-colors font-medium">Did you mean: '+_escapeRe(suggestion)+'?</button>'; }
    html+='</div>';
    if(rawQuery.indexOf(':')!==-1) html+='<div class="px-4 pb-2 text-center"><p class="text-[10px] text-slate-400 font-mono">Filter syntax: <span class="text-brand-500">cat:ABAP</span> <span class="text-slate-500">or</span> <span class="text-brand-500">tag:Staff+</span></p></div>';
    results.innerHTML=html;
    var suggestionBtn=results.querySelector('.search-suggestion-chip'); if(suggestionBtn) suggestionBtn.addEventListener('click',function(){ var input=document.getElementById('modal-search-input'); if(input){input.value=suggestionBtn.getAttribute('data-suggestion');renderResults(input.value);input.focus();}});
  }
  function _applySelection(el) { if(!el) return; el.classList.add('bg-brand-50','dark:bg-brand-500/10','border-brand-100','dark:border-brand-500/30'); el.setAttribute('aria-selected','true'); }
  function _clearSelection(el) { if(!el) return; el.classList.remove('bg-brand-50','dark:bg-brand-500/10','border-brand-100','dark:border-brand-500/30'); el.removeAttribute('aria-selected'); }
  function _navigateSearch(dir) {
    var links=document.querySelectorAll('#modal-search-results .search-result');
    if(links.length===0) return;
    if(_selectedIndex>=0&&links[_selectedIndex]) _clearSelection(links[_selectedIndex]);
    _selectedIndex=(_selectedIndex+dir+links.length)%links.length;
    _applySelection(links[_selectedIndex]);
    links[_selectedIndex].focus();
    if(_currentResults[_selectedIndex]) updateSearchPreview(_currentResults[_selectedIndex]);
  }
  function openSearchModal() {
    var modal=document.getElementById('search-modal'), input=document.getElementById('modal-search-input');
    if(!modal) return;
    _lastFocusedEl=document.activeElement;
    modal.classList.remove('hidden'); modal.classList.add('flex');
    if(input) input.value=''; if(input) input.focus();
    document.body.style.overflow='hidden';
    _selectedIndex=-1; renderResults('');
  }
  function closeSearchModal() {
    var modal=document.getElementById('search-modal'), input=document.getElementById('modal-search-input'), results=document.getElementById('modal-search-results');
    if(!modal) return;
    modal.classList.remove('flex'); modal.classList.add('hidden');
    document.body.style.overflow='';
    if(input) input.value=''; if(results) results.innerHTML='';
    _selectedIndex=-1; if(_lastFocusedEl){_lastFocusedEl.focus();_lastFocusedEl=null;}
  }
  document.addEventListener('click',function(e){ if(e.target.closest('.open-search-btn')) openSearchModal(); });
  document.addEventListener('click',function(e){ if(e.target.id==='close-search-btn'||e.target.closest('#close-search-btn')) closeSearchModal(); });
  document.addEventListener('click',function(e){ var modal=document.getElementById('search-modal');if(!modal||modal.classList.contains('hidden'))return; if(e.target===modal) closeSearchModal(); });
  document.addEventListener('click',function(e){ var link=e.target.closest('#modal-search-results a'); if(link) closeSearchModal(); });
  document.addEventListener('keydown',function(e){ var modal=document.getElementById('search-modal');if(!modal||modal.classList.contains('hidden'))return; if(e.key==='Escape') closeSearchModal(); });
  document.addEventListener('keydown',function(e){ var shareModal=document.getElementById('share-modal');if(shareModal&&!shareModal.classList.contains('hidden'))return; var searchModal=document.getElementById('search-modal'); if((e.metaKey||e.ctrlKey)&&e.key==='k'){e.preventDefault(); if(searchModal&&searchModal.classList.contains('hidden')) openSearchModal(); else closeSearchModal(); } });
  document.addEventListener('input',function(e){ if(e.target.id!=='modal-search-input') return; var value=e.target.value; if(_searchDebounce) clearTimeout(_searchDebounce); if(!value||value.trim().length===0){renderResults(value);return;} _searchDebounce=setTimeout(function(){renderResults(value);},150); });
  document.addEventListener('keydown',function(e){ var modal=document.getElementById('search-modal');if(!modal||modal.classList.contains('hidden'))return; if(e.key==='ArrowDown'){e.preventDefault();_navigateSearch(1);}else if(e.key==='ArrowUp'){e.preventDefault();_navigateSearch(-1);}else if(e.key==='Enter'){var links=document.querySelectorAll('#modal-search-results .search-result');if(_selectedIndex>=0&&links[_selectedIndex]){e.preventDefault();window.location.href=links[_selectedIndex].getAttribute('href');closeSearchModal();}}});
  document.addEventListener('mouseover',function(e){ var result=e.target.closest('.search-result');if(!result)return; var links=document.querySelectorAll('#modal-search-results .search-result'); if(_selectedIndex>=0&&links[_selectedIndex]) _clearSelection(links[_selectedIndex]); _selectedIndex=Array.prototype.indexOf.call(links,result); _applySelection(result); if(_currentResults[_selectedIndex]) updateSearchPreview(_currentResults[_selectedIndex]); });
})();
