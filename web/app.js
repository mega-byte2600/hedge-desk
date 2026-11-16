import { escapeHTML as e, human, statusClass, readNotes, saveNote } from './core.mjs';
import { assessShortPut, extractShortPutRows, mrMarketContext, readFilter, readOwnIt, saveFilter, saveOwnIt } from './graham-filter.mjs';
import { mountWorkbench } from './options-workbench-ui.js';
const $ = s => document.querySelector(s);
let data, report, route='overview';
let grahamNightly=null, grahamLoading=null;
const names={'overnight-premium-desk':'Overnight Premium','earnings-event-desk':'Earnings Event','arbitrage-observer':'Box / Parity Observer','dividend-opportunity-desk':'Dividend Opportunity','open-quant-ai-model-lab':'Short Sale Research','event-futures-desk':'Futures Event'};
const layers={OBSERVED:'Observed data',STAT:'Statistical evidence',BIG:'Research proposal',DETERMINISTIC_RISK:'Deterministic risk',DETERMINISTIC_COMPLIANCE:'Compliance',HUMAN:'Human review'};
const title={overview:'Overview',dashboard:'Dashboard',candidates:'Candidates',desks:'Research desks',desk5:'Desk 5 · Short Research',desk7:'Desk 7 · Bonds & Rates',controls:'Controls & evidence',journal:'Yellow Sheets',resources:'Research resources',workbench:'Options Workbench','real-estate':'Real Estate',brief:'Daily brief',about:'About'};
const tag=s=>`<span class="tag ${statusClass(s)}">${e(human(s))}</span>`;
const money=v=>{const n=String(v);return `${n.startsWith('-')?'−':''}$${n.replace('-','').replace(/\B(?=(\d{3})+(?!\d))/g,',')}`;};
const date=v=>new Date(v).toLocaleString(undefined,{dateStyle:'medium',timeStyle:'short'});
const shortName=id=>names[id]||human(id);
const head=(t,sub,actions='')=>`<div class="page-head"><div><h1>${t}</h1><p class="subtitle">${sub}</p></div><div class="actions">${actions}</div></div>`;
const btn=(a,t,primary=false)=>`<button class="btn ${primary?'primary':''}" data-action="${a}">${t}</button>`;
const gates=p=>{const ls=p.layers||[];return `<div class="gate-bars" aria-label="${e(ls.map(l=>`${layers[l.layer]}: ${human(l.status)}`).join('; '))}">${ls.map(l=>`<span class="${statusClass(l.status)}" title="${e(layers[l.layer]+': '+human(l.status))}"></span>`).join('')}</div>`;};
const stat=(label,value,foot)=>`<article class="stat"><div class="eyebrow">${label}</div><div class="stat-value">${value}</div><div class="stat-foot">${foot}</div></article>`;
const panel=(t,sub,body,link='')=>`<section class="panel"><div class="panel-head"><div><h2>${t}</h2>${sub?`<p>${sub}</p>`:''}</div>${link}</div>${body}</section>`;
let overviewBrief=null, overviewBriefDone=false;
async function ensureOverviewBrief(){if(overviewBriefDone)return;overviewBriefDone=true;try{const r=await fetch('./research-brief.json',{cache:'default'});if(r.ok)overviewBrief=await r.json();}catch(_){overviewBrief=null;}}
const OV_BRAND='';
function overview(){
if(typeof HedgeDeskOverview==='undefined'||!HedgeDeskOverview.render){
return OV_BRAND+'<div class="ov"><section class="ov-hero"><div class="ov-eyebrow">Overview unavailable</div><p class="ov-muted">The overview module failed to load.</p><div class="actions">'+btn('reload','Reload',true)+'</div></section></div>';
}
return OV_BRAND+HedgeDeskOverview.render(data, report, overviewBrief);
}
function brief(){return head('Daily brief','Today\u2019s research input from the six desks. Replaced every morning.',`<a class="btn" href="./research-today.md" download>↓ Full package (.md)</a>`)+
`<section class="panel" id="research-brief" aria-live="polite"><div class="panel-body"><p class="muted">Loading today\u2019s brief\u2026</p></div></section>`;}
async function hydrateBrief(){const host=document.getElementById('research-brief');if(!host)return;try{const r=await fetch('./research-brief.json',{cache:'default'});if(!r.ok)throw Error('brief unavailable');const b=await r.json();
host.innerHTML=`<div class="panel-head"><div><div class="eyebrow">${e(b.date||'')}</div><h2>${e(b.headline||'Daily research brief')}</h2></div></div><div class="panel-body">`+
(b.items||[]).map(it=>`<div class="brief-item"><h3>${e(it.title)}</h3><p>${e(it.detail)}</p></div>`).join('')+
`<details><summary>Per-desk one-liners</summary><div class="table-scroll"><table><thead><tr><th>Desk</th><th>Note</th></tr></thead><tbody>${Object.entries(b.desks||{}).map(([k,v])=>`<tr><td><strong>${e(k)}</strong></td><td>${e(v)}</td></tr>`).join('')}</tbody></table></div></details>`+
`<p class="small-note">${e(b.note||'')}</p><p><a class="text-link" href="${e(b.full_report||'./research-today.md')}" download>Download the full research package (.md) ↗</a></p></div>`;
}catch(err){host.innerHTML=`<div class="panel-body"><p class="muted">Today\u2019s brief has not been published yet. Check back after the morning research run.</p></div>`;}}
function desks(){return head('Research desks','Inspect each workflow, its evidence, and what stops the next decision.')+`<div class="cards">${report.projects.map((p,i)=>{const reg=data.registry.find(r=>r.project_id===p.project_id);return `<article class="panel desk-card"><div style="display:flex;justify-content:space-between"><span class="eyebrow">DESK 0${i+1}</span>${p.disposition?tag(p.disposition):''}</div><h2>${e(shortName(p.project_id))}</h2><p>${e(reg.objective)}</p>${gates(p)}<button class="btn" data-desk="${p.project_id}">Open desk ↗</button>${p.project_id==='bonds-rates-desk'?`<a class="btn" href="#desk7">Indicator dashboard ↗</a>`:''}</article>`}).join('')}</div>`;}
function grahamBadge(value){return `<span class="graham-badge graham-${String(value).toLowerCase().replace(/_/g,'-')}">${e(human(value))}</span>`;}
function grahamCell(row,vix){
  if(!row.grahamEligible)return '<span class="muted">Not a short put</span>';
  const ownIt=readOwnIt(localStorage,row.symbol);
  const a=assessShortPut({symbol:row.symbol,...(row.grahamMarket||{}),ownIt,vix});
  const selected=value=>ownIt===value?' selected':'';
  const metrics=a.totalMarginPct===null
    ? '<small>Awaiting nightly option data</small>'
    : `<small>MoS ${e(a.marginRating)} ${a.totalMarginPct.toFixed(2)}% · Annualized ${a.annualizedPct.toFixed(1)}% / ${a.hurdlePct.toFixed(0)}%</small>`;
  return `${grahamBadge(a.verdict)}<label class="graham-own">Own if assigned?<select class="input" data-graham-own="${e(row.symbol)}" aria-label="Would you own ${e(row.symbol)} if assigned?"><option value=""${selected(null)}>Unanswered</option><option value="yes"${selected(true)}>Yes</option><option value="no"${selected(false)}>No</option></select></label>${metrics}`;
}
function candidates(){
  const enriched=extractShortPutRows(data.candidate_feed,grahamNightly);
  const vix=grahamNightly?.vix_regime?.last_close;
  const filterOn=readFilter(localStorage);
  const assessed=enriched.map(row=>{
    if(!row.grahamEligible)return {...row,grahamAssessment:null};
    const ownIt=readOwnIt(localStorage,row.symbol);
    return {...row,grahamAssessment:assessShortPut({symbol:row.symbol,...(row.grahamMarket||{}),ownIt,vix})};
  });
  const rows=filterOn?assessed.filter(row=>row.grahamAssessment?.verdict!=='SPECULATION'):assessed;
  const market=mrMarketContext(vix);
  const marketCopy=grahamNightly
    ? `VIX ${market.vix===null?'—':market.vix.toFixed(2)} · ${e(market.read)}`
    : 'Loading real nightly VIX and short-put chain data…';
  const hidden=assessed.length-rows.length;
  return head('Research candidates','Real symbols entering your six desk methods. Graham discipline is applied inline to short puts; it does not authorize trades.',btn('export-candidates','↓ Candidate feed'))+
  `<div class="notice"><strong>Overnight candidates</strong><span>Overnight wheel candidates from the nightly batch (Yahoo/Cboe). Graham inputs use the same real nightly report.</span></div>`+
  `<div class="mr-market"><strong>MR. MARKET · ${e(market.regime)}</strong><span>${marketCopy}</span></div>`+
  `<div class="graham-toolbar"><label><input id="graham-filter-toggle" type="checkbox" ${filterOn?'checked':''}> Hide Graham speculation</label><span class="small">${hidden} filtered · NEEDS YOU remains visible</span></div>`+
  `<div class="stats">${stat('Symbols',new Set(assessed.map(r=>r.symbol)).size,'Real tickers and futures roots')}${stat('Desk assignments',assessed.length,'Shared client-neutral feed')}${stat('Short puts',assessed.filter(r=>r.grahamEligible).length,'Graham-eligible rows')}</div>`+
  panel('Six-desk candidate board','Verdict is context, not an execution gate. RoR and order flow are unchanged.',`<div class="table-scroll cards-table"><table><thead><tr><th>Symbol</th><th>Desk</th><th>Stage</th><th>Method</th><th>Graham</th><th>Evidence needed</th></tr></thead><tbody>${rows.map(r=>`<tr><td><strong class="mono">${e(r.symbol)}</strong><small>${e(human(r.instrument_type))}</small></td><td data-label="Desk">${e(shortName(r.desk_id))}</td><td data-label="Stage">${tag(r.stage)}</td><td data-label="Method">${e(r.method)}</td><td data-label="Graham" class="graham-cell">${grahamCell(r,vix)}</td><td data-label="Evidence needed">${e(r.evidence_needed)}</td></tr>`).join('')}</tbody></table></div>`);
}
async function hydrateGraham(){
  if(grahamNightly||grahamLoading)return grahamLoading;
  grahamLoading=fetch('./api/am-report',{cache:'no-store'}).then(async response=>{
    if(!response.ok)throw Error('nightly report unavailable');
    const candidate=await response.json();
    if(!candidate||typeof candidate.cash_secured_put_scan!=='object'||typeof candidate.vix_regime!=='object')throw Error('nightly Graham inputs unavailable');
    grahamNightly=candidate;
    if(route==='candidates')render();
    return candidate;
  }).catch(()=>null).finally(()=>{grahamLoading=null;});
  return grahamLoading;
}
function about(){const o=data.owner;return head('About','The builder behind Trade Desk Research.')+`<section class="panel"><div class="panel-body about-card"><div class="eyebrow">FOUNDER / BUILDER</div><h1>${e(o.display_name)}</h1><p>Trade Desk is an independent research platform built to test six specialized market approaches with reproducible evidence, with a seventh (Bonds & Rates) in development, explicit controls, and human judgment.</p><p>Research automation is separate from deterministic portfolio survival controls. Live trading and fully autonomous execution are not part of this MVP.</p><div class="actions"><a class="btn primary" href="${e(o.linkedin_url)}" target="_blank" rel="noopener noreferrer">View LinkedIn ↗</a><a class="btn" href="https://github.com/mega-byte2600/hedge-desk" target="_blank" rel="noopener noreferrer">View GitHub ↗</a></div></div></section>`+`<div class="section-gap">${panel('Research only','Public market research and decision support.','<div class="panel-body"><p class="small">The workspace presents sourced market context and paper research. Nothing here is investment advice.</p></div>')}</div>`;}
function kv(obj){return Object.entries(obj).map(([k,v])=>`<div class="keyvalue"><span>${e(human(k))}</span><strong>${e(typeof v==='object'?JSON.stringify(v):v)}</strong></div>`).join('')}
function openDesk(id){const p=report.projects.find(p=>p.project_id===id);if(!p)return;const reg=data.registry.find(r=>r.project_id===id);const live=p.data_status==='live';const needsWatchlist=id==='open-quant-ai-model-lab'&&String(p.reason||'').includes('approved watchlist symbols required');const statusEyebrow=needsWatchlist?'WATCHLIST REQUIRED':(live?'LIVE MARKET DATA':(p.data_status==='batch'?'BATCH DATA':'DATA UNAVAILABLE'));const quotes=Object.values(p.live_data||{});const body=needsWatchlist?`<div class="notice">Desk 5 has no approved watchlist symbols yet.</div><p class="small muted">Add approved symbols to start sourced short-sale research. The desk will not select a universe or infer candidates on its own.</p>`:(live||p.data_status==='batch'?`<div class="notice">${tag(p.data_status.toUpperCase())}<span>Base data as of ${e(date(p.data_as_of))} · ${e(p.data_source||'')}</span></div>${p.reason?`<p class="small">${e(p.reason)}</p>`:''}<div class="table-scroll cards-table"><table><thead><tr><th>Symbol</th><th>Name</th><th>Last</th><th>Change</th><th>Source</th></tr></thead><tbody>${quotes.map(q=>`<tr><td><strong>${e(q.symbol)}</strong></td><td data-label="Name">${e(q.name)}</td><td data-label="Last" class="mono">${e(q.last)}</td><td data-label="Change" class="mono">${e(q.change_pct)}%</td><td data-label="Source">${e(q.source)}</td></tr>`).join('')}</tbody></table></div>${(p.unavailable||[]).length?`<p class="small">Unavailable: ${(p.unavailable||[]).map(u=>e(u.symbol)+' — '+e(u.reason)).join('; ')}</p>`:''}`:`<div class="data-reconnecting" role="status" aria-live="polite"><span>Market data reconnecting</span><span class="data-dots" aria-hidden="true"><i></i><i></i><i></i></span></div><p class="small muted">Latest validated data will resume automatically when the feed is available.</p>`);const shortDesk=id==='open-quant-ai-model-lab'?`<section class="panel section-gap"><div class="eyebrow">DESK 5 · SHORT CANDIDATE WORKFLOW</div><h3>Develop the thesis before it becomes a candidate</h3><ol><li>Use only approved watchlist symbols.</li><li>Build a point-in-time bear thesis from SEC filings and attributable evidence.</li><li>Map catalysts, financial deterioration, valuation, and the strongest counter-thesis.</li><li>Check liquidity, volatility, reported short interest and borrow status separately.</li><li>Record thesis invalidation conditions and missing evidence.</li><li>Send complete research for independent human review.</li></ol><p class="small"><strong>Rules lens:</strong> CFA Standards V(A), V(B), and VI(A); FINRA Series 7 short-sale concepts; Series 4 supervisory principles when options are considered. Short-sale volume is not short interest. A research desk cannot certify borrow availability, locate, order marking, delivery, or Rule 201 compliance.</p><p class="small">No candidate is a recommendation or trade authorization. There are no short-sale candidates until source-backed research has been completed.</p></section>`:'';$('#detail-content').innerHTML=`<div class="dialog-head"><div><div class="eyebrow">${statusEyebrow} / ${e(date(p.evaluated_at))}</div><h2 style="margin-top:9px">${e(reg?reg.name:id)}</h2></div><button class="close" data-action="close" aria-label="Close desk">×</button></div><div class="dialog-body">${reg?`<p class="small">${e(reg.objective||'')}</p>`:''}${shortDesk}${body}<div class="actions section-gap"><button class="btn primary" data-note-desk="${id}">Write Yellow Sheet</button><button class="btn" data-export-desk="${id}">↓ Export desk JSON</button></div></div>`;$('#detail').showModal();}
function controls(){const sources=data.research_data_sources||[];const liveDesks=(report.projects||[]).filter(p=>p.data_status==='live').length;return head('Controls & evidence','Trace the published data to its sources.',btn('export-json','↓ Export evidence'))+`<div class="stats">${stat('Desks live',liveDesks+' / '+report.projects.length,'Real market data')}${stat('Data sources',sources.length,'Free public APIs')}${stat('Synthetic data','0','None served')}${stat('Trade authorization','None','Paper research only')}</div>`+panel('Carpe DATA feed status','Live observations from authoritative public feeds. Read-only research data.', '<div id="market-context-host" class="panel-body"><p class="muted" role="status">Loading public market context…</p></div>')+panel('Research data pipeline','Live data from free public APIs. No synthetic fixtures are served.',`<div class="table-scroll cards-table"><table><thead><tr><th>Source</th><th>Dataset</th><th>Status</th><th>Research desks</th></tr></thead><tbody>${sources.map(s=>`<tr><td>${e(human(s.source_id))}</td><td data-label="Dataset">${e(s.dataset)}</td><td data-label="Status">${tag(s.status)}</td><td data-label="Research desks">${e((s.feeds||[]).map(shortName).join(', '))}</td></tr>`).join('')}</tbody></table></div>`)+`<div class="section-gap">${panel('Report identity','Live data snapshot.',`<div class="panel-body">${kv({generated_at:report.generated_at,engine_code_commit:report.code_commit,report_type:report.report_type,runner_version:report.runner_version})}<p class="small">${report.limitations.map(e).join(' ')}</p></div>`)}</div>`;}
async function hydrateMarketContext(){
const host=$('#market-context-host');if(!host)return;
try{
const response=await fetch('./api/market-context',{cache:'no-store'});
if(!response.ok)throw Error('Public data status unavailable ('+response.status+').');
const snapshot=await response.json();if(snapshot.status==='LOADING'){host.innerHTML='<p class="muted" role="status">Refreshing public providers in the background. This does not block the research workspace.</p>';setTimeout(hydrateMarketContext,5000);return;}const sources=Object.values(snapshot.sources||{});
const rows=sources.map(s=>{
const detail=JSON.stringify(s.observations||[],null,2);
return '<tr><td><strong>'+e(s.provider_id||'')+'</strong><small>'+e(s.dataset||'')+'</small></td><td>'+tag(s.status||'UNKNOWN')+'</td><td>'+e(s.observation_count||0)+'</td><td><details><summary>Observations</summary><pre>'+e(detail.length>3000?detail.slice(0,3000)+'…':detail)+'</pre></details></td></tr>';
}).join('');
host.innerHTML='<div class="notice"><strong>'+e(snapshot.status||'UNKNOWN')+'</strong><span>'+e(snapshot.live_sources||0)+' live · '+e(snapshot.blocked_sources||0)+' blocked · '+e(snapshot.unconfigured_sources||0)+' unconfigured · storage '+e(snapshot.storage?.status||'UNKNOWN')+' · '+e(snapshot.generated_at||'')+'</span></div><div class="table-scroll cards-table"><table><thead><tr><th>Provider / dataset</th><th>Status</th><th>Rows</th><th>Sample</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
}catch(err){host.innerHTML='<p class="muted" role="status">'+e(err.message||'Public market context unavailable.')+'</p>';}
}
function notes(){try{return readNotes(localStorage)}catch{return []}}
function journal(){const ns=notes();return head('Yellow Sheets','Record the thesis, evidence, and conditions that would invalidate your research.',btn('export-notes','↓ Export notes'))+`<div class="notice"><strong>Saved in this browser</strong><span>Notes stay in this browser. Export a copy to keep them. They do not authorize trades or change engine decisions.</span></div><div class="journal-layout">${panel('New research note','A deliberate record before a decision.',`<form id="note-form" class="panel-body"><label class="form-field">Research desk<select class="input" name="desk">${report.projects.map(p=>`<option value="${p.project_id}">${e(shortName(p.project_id))}</option>`).join('')}</select></label><label class="form-field">Thesis<textarea class="input" name="thesis" maxlength="6000" required placeholder="What do you believe, and why?"></textarea></label><label class="form-field">Evidence<textarea class="input" name="evidence" maxlength="6000" required placeholder="Which observations support this thesis?"></textarea></label><label class="form-field">What would invalidate it?<textarea class="input" name="invalidation" maxlength="6000" required placeholder="Define the facts that would change your view."></textarea></label><button class="btn primary" type="submit">Save research note</button><p class="small">Bound to the currently displayed report hash.</p></form>`)}${panel('Research journal',`${ns.length} saved ${ns.length===1?'note':'notes'} in this browser`,ns.length?ns.slice().reverse().map(n=>`<article class="saved-note"><div class="eyebrow">${e(shortName(n.desk))} · ${e(date(n.created_at))}</div><p><strong>Thesis</strong><br>${e(n.thesis)}</p><details><summary>Evidence & invalidation</summary><p><strong>Evidence</strong><br>${e(n.evidence)}</p><p><strong>Invalidation</strong><br>${e(n.invalidation)}</p><p class="hash">Report: ${e(n.report_sha256)}</p></details></article>`).join(''):'<div class="empty">Your first research note starts here.</div>')}</div>`;}
function resources(){return head('Research resources','Institutional sources, market infrastructure, and selected research tools used to orient Emporion research.')+'<div class="panel"><div class="panel-body"><div class="skel-rows" aria-hidden="true"><div class="skeleton" style="height:18px;width:45%"></div><div class="skeleton" style="height:14px"></div><div class="skeleton" style="height:14px;width:82%"></div><div class="skeleton" style="height:14px;width:64%"></div></div><p class="small" role="status">Loading research resources…</p></div></div>';}
function dashSummary(){const rd=data.risk_dashboard||{};const cands=(data.candidate_feed&&data.candidate_feed.candidates)||[];const srcs=(report.data_batch&&report.data_batch.source_results)||[];const live=srcs.filter(s=>String(s.status).toUpperCase()==='PASS').length;const top=cands.slice(0,5);const acts=rd.executive_actions||[];return `<div data-dash-summary><div class="stats">`+stat('Candidates',cands.length,'Real symbols in the feed')+stat('Qualified picks',cands.filter(c=>c.stage==='REAL_EOD_CANDIDATE').length,'Method-qualified this run')+stat('Sources live',live+' / '+srcs.length,'Reporting sources')+stat('Desks evaluated',report.projects.length,'Six-desk coverage')+`</div>`+(acts.length?`<section class="panel"><div class="panel-head"><div><div class="eyebrow">WHAT NEEDS YOU</div><h2>Morning checklist</h2></div></div><div class="panel-body">`+acts.map(a=>`<p class="small">\u25b8 ${e(a)}</p>`).join('')+`</div></section>`:'')+`<div class="section-gap"><section class="panel"><div class="panel-head"><div><div class="eyebrow">TOP CANDIDATES</div><h2>First five in the feed</h2></div><a class="text-link" href="#candidates">Full board \u2197</a></div><div class="table-scroll"><table><thead><tr><th>Symbol</th><th>Desk</th><th>Stage</th></tr></thead><tbody>`+top.map(c=>`<tr><td><strong class="mono">${e(c.symbol)}</strong></td><td>${e(shortName(c.desk_id))}</td><td>${tag(c.stage)}</td></tr>`).join('')+`</tbody></table></div><div class="panel-body small">Snapshot ${e(date(report.generated_at))} \u00b7 report ${e(String((data.summary||{}).report_sha256||'').slice(0,10))}</div></section></div></div>`;}
function dashboard(){const frame='<div class="frame-shell"><div class="skeleton" aria-hidden="true"></div><iframe class="autofit-frame dash-frame" data-autofit title="Live market-data dashboard"></iframe></div>';const desktop=frame.replace('<iframe','<iframe src="/dashboard"');const mobile=`<div class="dash-mobile">${dashSummary()}<div class="section-gap"><button class="btn primary" data-action="open-full-dash" style="width:100%">Open full dashboard \u2197</button><p class="small-note">The full dashboard is a desktop-density chart wall. It loads only when you ask.</p></div><div class="frame-shell section-gap" id="dash-full" hidden><div class="skeleton" aria-hidden="true"></div><iframe class="autofit-frame dash-frame" data-autofit data-src="/dashboard" title="Live market-data dashboard"></iframe></div></div>`;return `<div class="panel"><div class="panel-head"><div><div class="eyebrow">LIVE REAL-DATA DASHBOARD</div><h2>Overnight candidates, options premium, and the wheel — on real market data.</h2></div></div>${mobile}<div class="dash-desktop">${desktop}</div></div>`;}
function workbench(){return `<div class="panel"><div class="panel-body" id="workbench-host"><p class="muted">Loading the options workbench\u2026</p></div></div>`;}
function hydrateWorkbench(){const host=document.getElementById('workbench-host');if(host)mountWorkbench(host);}
function realEstate(){return `<div class="panel"><div class="panel-body" id="real-estate-host"><p class="muted">Loading Real Estate models…</p></div></div>`;}
async function hydrateRealEstate(){
  const host=document.getElementById('real-estate-host');if(!host)return;
  try{
    if(!document.getElementById('real-estate-style')){
      const link=document.createElement('link');link.id='real-estate-style';link.rel='stylesheet';link.href='./real-estate.css?v=20261004-noir';document.head.appendChild(link);
    }
    const mod=await import('./real-estate-ui.js');
    const current=document.getElementById('real-estate-host');
    if(route!=='real-estate'||!current)return;
    current.innerHTML=mod.realEstatePage();
    mod.mountRealEstate(current);
  }catch(err){
    host.innerHTML=`<div class="error"><h2>Real Estate models unavailable</h2><p>${e(err.message||'The model UI could not load.')}</p><p>The rest of Emporion remains available.</p></div>`;
  }
}
function desk7(){return head('Desk 7 · Bonds & Rates','The core indicators behind the Fed rate decision, with the trigger rule, the read, and the vote on each.')+`<div id="desk7-host"><div class="panel"><div class="panel-body"><p class="muted">Loading Desk 7 indicators…</p></div></div></div>`;}
function desk5(){return head('Desk 5 · Short Research','Watchlist-level price context, dated catalysts, filings, short interest, and borrow status. Research queue only.')+`<div id="desk5-host"><div class="panel"><div class="panel-body"><p class="muted" role="status">Loading Desk 5 watchlist…</p></div></div></div>`;}
async function hydrateDesk5(){
  const host=document.getElementById('desk5-host');if(!host)return;
  try{
    const r=await fetch('./api/short-research',{cache:'no-store'});if(!r.ok)throw Error('Desk 5 data unavailable');
    const d=await r.json();if(d.schema_version!=='hedge-desk-short-research-board-1.0.0'||!Array.isArray(d.symbols))throw Error('Desk 5 data unavailable');
    if(route!=='desk5')return;
    const rows=d.symbols;
    const complete=rows.filter(x=>x.case_status==='READY_FOR_INDEPENDENT_REVIEW').length;
    const weak=rows.filter(x=>x.price_context==='BOTH_LOOKBACKS_NEGATIVE').map(x=>x.symbol);
    const body=rows.length?rows.map(x=>`<tr><td><strong class="mono">${e(x.symbol)}</strong></td><td data-label="Last close" class="mono">${x.last_close==null?'—':'$'+Number(x.last_close).toFixed(2)}</td><td data-label="5-session change" class="mono">${x.return_5_sessions_pct==null?'—':Number(x.return_5_sessions_pct).toFixed(1)+'%'}</td><td data-label="20-session change" class="mono">${x.return_20_sessions_pct==null?'—':Number(x.return_20_sessions_pct).toFixed(1)+'%'}</td><td data-label="Price context">${e(x.price_context.replaceAll('_',' '))}</td><td data-label="SEC filing">${e(x.sec_filing_status)}</td><td data-label="Catalyst">${e(x.catalyst_status)}</td><td data-label="Short interest">${e(x.short_interest_status)}</td><td data-label="Borrow">${e(x.borrow_status)}</td><td data-label="Research case">${e(x.case_status.replaceAll('_',' '))}</td></tr>`).join(''):'<tr><td colspan="10">No watchlist symbols in the latest validated report.</td></tr>';
    host.innerHTML=`<div class="stats">${stat('Watchlist symbols',rows.length,'From latest validated nightly report')}${stat('Price weakness',weak.length,weak.length?weak.join(', ')+' · both lookbacks negative':'None in both lookbacks')}${stat('Research complete',complete,'Ready for independent review')}${stat('Catalyst / borrow','Not sourced','No dates or broker evidence')}</div>`
      +`<div class="section-gap">${panel('Price behavior · context only','Each point is one watchlist symbol. The lower-left quadrant shows negative returns over both lookback windows; this is a review cue, not a short ranking.',`<div class="panel-body"><div id="desk5-return-chart" role="img" aria-label="Scatter plot of five-session and twenty-session price returns for Desk 5 watchlist symbols"><p class="muted">Loading chart…</p></div><p class="small muted">X axis: 20-session price change. Y axis: 5-session price change. Source: real nightly EOD closes, as of ${e(d.as_of||'unavailable')}. Earnings and other catalyst dates are not yet sourced into this board.</p></div>`)}</div>`
      +`<div class="section-gap">${panel('Desk 5 research queue','Symbols are shown because they are in the configured watchlist. None has a completed short thesis in this snapshot.',`<div class="table-scroll cards-table"><table><thead><tr><th>Symbol</th><th>Last close</th><th>5-session</th><th>20-session</th><th>Price context</th><th>SEC filing</th><th>Catalyst</th><th>Short interest</th><th>Borrow</th><th>Case</th></tr></thead><tbody>${body}</tbody></table></div>`)}</div>`
      +`<div class="section-gap">${panel('Burry-inspired valuation work','A documented research lens, not a proprietary Burry formula or a Burry signal.',`<div class="panel-body"><p>Start with the company’s filings and derive a conservative intrinsic-value range from explicit, sourced assumptions. Then show the price premium to that estimate: <span class="mono">(current price ÷ conservative value) − 1</span>. This is a Desk 5 diagnostic, not a formula attributed to Michael Burry and not a standalone short signal.</p><p>Show the valuation inputs, filing dates, peer or historical basis, sensitivity range, and strongest bull case. If those inputs are missing, label valuation incomplete; do not manufacture a score.</p><p class="small">Reference lens: Burry’s 2000 Scion letter describes margin-of-safety and individual-security valuation principles; see <a class="text-link" href="https://www.valuebeast.co.kr/guru/michael-burry/docs/2000-annual" target="_blank" rel="noopener">archived letter text</a>. The app adapts the discipline to short research; it does not claim Burry used this short-side equation.</p></div>`)}</div>`
      +`<div class="section-gap">${panel('Schwab / thinkorswim verification','Market data is not a locate or borrow confirmation.',`<div class="panel-body"><p>Before a short idea could be considered outside this research app, manually verify in Schwab’s short-sale workflow: security and account eligibility, shares available, locate or pre-borrow status, borrow fee/rebate, quantity, quote time and expiry, and any restrictions. Record the Schwab confirmation reference and timestamp in the research note. Recheck availability immediately before any external order.</p><p class="small">Schwab is a broker-dealer, but this integration remains market-data-only. No Schwab account, positions, balances, order history, locate request, or order endpoint is accessed here.</p></div>`)}</div>`
      +`<div class="section-gap">${panel('Broker-readiness gates','These facts cannot be inferred from a price chart or public short-sale volume.',`<div class="panel-body"><p>${e(d.interpretation||'')}</p><ul><li>Specific locate or pre-borrow evidence, with broker/source and timestamp</li><li>Current borrow availability, fee/rebate, quantity, and expiration terms where provided</li><li>Short-interest report with settlement date; daily short-sale volume is not a substitute</li><li>Point-in-time SEC filing, independent corroboration, catalyst, counter-thesis, valuation, liquidity, and invalidation conditions</li><li>Broker confirmation of order marking and applicable Regulation SHO controls at execution</li></ul><p class="small">CFA standards inform research integrity; FINRA Series 7 topics inform product and order concepts; Series 4 supervisory concepts inform options oversight. The desk does not provide a locate or authorize a trade.</p></div>`)}</div>`;
    renderDesk5Chart(rows);
  }catch(_){host.innerHTML='<div class="error"><h2>Desk 5 data unavailable</h2><p>The latest validated watchlist snapshot could not be loaded.</p></div>';}
}
let desk5PlotlyPromise=null;
async function renderDesk5Chart(rows){
  const el=document.getElementById('desk5-return-chart');if(!el)return;
  if(!window.Plotly&&!desk5PlotlyPromise)desk5PlotlyPromise=import('./vendor/plotly-2.35.2.min.js').then(()=>window.Plotly,()=>null);
  const P=window.Plotly||await desk5PlotlyPromise;if(route!=='desk5')return;
  const valid=rows.filter(x=>x.return_5_sessions_pct!=null&&x.return_20_sessions_pct!=null);
  if(!P){el.innerHTML='<p class="muted">Chart unavailable. The sourced return table above remains available.</p>';return;}
  if(!valid.length){el.innerHTML='<p class="muted">Not enough validated closes to plot return context. No placeholder points are shown.</p>';return;}
  const colors=valid.map(x=>x.return_5_sessions_pct<0&&x.return_20_sessions_pct<0?'#e77d74':x.return_5_sessions_pct>=0&&x.return_20_sessions_pct<0?'#e3b765':x.return_5_sessions_pct<0?'#79a9dc':'#8fc9a3');
  const trace={type:'scatter',mode:'markers+text',x:valid.map(x=>x.return_20_sessions_pct),y:valid.map(x=>x.return_5_sessions_pct),text:valid.map(x=>x.symbol),textposition:'top center',textfont:{size:11,color:'#f4f1e8'},marker:{size:13,color:colors,line:{width:1,color:'#111114'}},customdata:valid.map(x=>[x.symbol,x.price_as_of,x.last_close]),hovertemplate:'<b>%{customdata[0]}</b><br>20-session: %{x:.1f}%<br>5-session: %{y:.1f}%<br>Close: $%{customdata[2]:.2f}<br>As of: %{customdata[1]}<extra></extra>'};
  const xExtent=Math.max(5,...valid.map(x=>Math.abs(x.return_20_sessions_pct)))*1.18;const yExtent=Math.max(5,...valid.map(x=>Math.abs(x.return_5_sessions_pct)))*1.18;
  const layout={paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{size:11,color:'#f4f1e8'},height:340,margin:{l:54,r:16,t:18,b:52},showlegend:false,xaxis:{title:'20-session price change',range:[-xExtent,xExtent],ticksuffix:'%',zeroline:false,gridcolor:'rgba(128,128,128,.2)'},yaxis:{title:'5-session price change',range:[-yExtent,yExtent],ticksuffix:'%',zeroline:false,gridcolor:'rgba(128,128,128,.2)'},shapes:[{type:'line',xref:'x',yref:'paper',x0:0,x1:0,y0:0,y1:1,line:{color:'rgba(244,241,232,.38)',dash:'dot'}},{type:'line',xref:'paper',yref:'y',x0:0,x1:1,y0:0,y1:0,line:{color:'rgba(244,241,232,.38)',dash:'dot'}}]};
  try{el.innerHTML='';await P.newPlot(el,[trace],layout,{responsive:true,displayModeBar:false});}catch(_){el.innerHTML='<p class="muted">Chart unavailable. The sourced return table above remains available.</p>';}
}
async function hydrateDesk7(){
  const host=document.getElementById('desk7-host');if(!host)return;
  try{
    const r=await fetch('./desk7-indicators.json',{cache:'default'});
    if(!r.ok)throw Error('Desk 7 indicators unavailable');
    const d=await r.json();
    if(d.schema_version!=='desk7-indicators-2'||!Array.isArray(d.indicators)||d.indicators.length!==10)throw Error('Desk 7 indicators unavailable');
    if(route!=='desk7')return;
    const t=d.decision.tally;
    const rows=d.indicators.map((x,i)=>`<tr id="desk7-row-${i}"><td><strong>${e(x.name)}</strong><br><span class="mono small">${e(x.series)}</span><br><span class="small muted">${e(x.source)}</span></td><td data-label="Why it matters">${e(x.why)}</td><td data-label="Trigger rule">${e(x.trigger)}</td><td data-label="Today's read">${e(x.read)}</td><td data-label="Vote"><strong>${e(x.vote)}</strong></td><td data-label="Broker view">${e(x.broker)}</td></tr>`).join('');
    host.innerHTML=`<div class="stats">${stat('Call',e(d.decision.call),'FOMC '+e(d.decision.meeting)+', range '+e(d.decision.target_range))}${stat('Tally',t.hike+' HIKE / '+t.cut+' CUT / '+t.neutral+' NEUTRAL','Across the 10 core indicators')}${stat('Market pricing',e(d.market_pricing.total_hike),'Kalshi total hike, Dec meeting')}${stat('As of',e(d.as_of),'Snapshot, see note below')}</div>`
    +panel('The decision','',`<div class="panel-body"><p>${e(d.decision.summary)}</p><p class="small muted">${e(d.as_of_note)}</p></div>`)
    +`<div class="section-gap">${panel('Vote balance','The tally as a balance. Hover a segment for the indicators behind it.',`<div class="panel-body"><div id="desk7-vote-chart"><p class="muted">Loading chart…</p></div></div>`)}</div>`
    +`<div class="section-gap">${panel('Where each indicator sits against its trigger','Each row is one indicator in its own units. Dashed lines are the tripwires from the trigger rule; the marker is today’s read. Click a row to jump to its detail.',`<div class="panel-body"><div id="desk7-gauge-chart"><p class="muted">Loading chart…</p></div><p class="small muted">FOMC vote and guidance has no numeric trigger: it votes HIKE on the 10–2 dissent pattern. See the table.</p><p class="small muted">On Claims and HY OAS, higher readings push toward a cut, so the CUT zone is on the right; on every other row the HIKE zone is on the right.</p></div>`)}</div>`
    +`<div class="section-gap">${panel('Core indicators','Each indicator carries its trigger rule, today\u2019s read, and its vote.',`<div class="table-scroll cards-table"><table><thead><tr><th>Indicator</th><th>Why it matters</th><th>Trigger rule</th><th>Today's read</th><th>Vote</th><th>Broker view</th></tr></thead><tbody>${rows}</tbody></table></div>`)}</div>`
    +`<div class="section-gap">${panel('Market pricing vs indicators','',`<div class="panel-body"><div id="desk7-kalshi-chart"><p class="muted">Loading chart…</p></div><p>${e(d.market_pricing.kalshi_note)}</p><p>${e(d.market_pricing.fedwatch_note)}</p><p>${e(d.market_pricing.disagreement)}</p></div>`)}</div>`
    +`<div class="section-gap">${panel('What would change the call','',`<div class="panel-body">${d.what_would_change.map(w=>`<p class="small">\u25b8 ${e(w)}</p>`).join('')}</div>`)}</div>`
    +`<div class="section-gap">${panel('Graham lens','',`<div class="panel-body">${d.graham.lines.map(g=>`<p>${e(g)}</p>`).join('')}<p class="small">${e(d.graham.spread)}</p></div>`)}</div>`
    +`<div class="section-gap">${panel('Grounding','',`<div class="panel-body"><p class="small">${e(d.grounding)}</p><p class="small"><a class="text-link" href="#brief">Daily brief ↗</a> — the full package carries the newer read.</p></div>`)}</div>`;
    renderDesk7Charts(d);
  }catch(err){
    host.innerHTML=`<div class="error"><h2>Desk 7 indicators unavailable</h2><p>data unavailable</p><p>The rest of Emporion remains available.</p></div>`;
  }
}
const DESK7_VOTE_COLOR={HIKE:'#dcb96f',NEUTRAL:'#a39e93',CUT:'#4a90d9'};
let desk7PlotlyPromise=null;
async function ensureDesk7Plotly(){
  if(window.Plotly)return window.Plotly;
  if(!desk7PlotlyPromise){desk7PlotlyPromise=import('./vendor/plotly-2.35.2.min.js').then(()=>window.Plotly,()=>null);}
  return desk7PlotlyPromise;
}
function desk7ChartBase(){return {paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{size:11,color:'#f4f1e8'},showlegend:false};}
function desk7ChartFail(id){const el=document.getElementById(id);if(el)el.innerHTML='<p class="muted">Chart unavailable. The table below carries the same data.</p>';}
async function renderDesk7Charts(d){
  const P=await ensureDesk7Plotly();
  if(route!=='desk7')return;
  if(!P){['desk7-vote-chart','desk7-gauge-chart','desk7-kalshi-chart'].forEach(desk7ChartFail);return;}
  try{renderDesk7VoteChart(P,d);}catch(_){desk7ChartFail('desk7-vote-chart');}
  try{await renderDesk7GaugeChart(P,d);}catch(_){desk7ChartFail('desk7-gauge-chart');}
  try{renderDesk7KalshiChart(P,d);}catch(_){desk7ChartFail('desk7-kalshi-chart');}
}
function renderDesk7VoteChart(P,d){
  const el=document.getElementById('desk7-vote-chart');if(!el)return;
  el.innerHTML='';
  const traces=['HIKE','NEUTRAL','CUT'].map(v=>{
    const names=d.indicators.filter(x=>x.vote===v).map(x=>x.name);
    return {x:[names.length],y:['Votes'],type:'bar',orientation:'h',marker:{color:DESK7_VOTE_COLOR[v]},text:[names.length+' '+v],textposition:v==='CUT'?'outside':'inside',textfont:{size:11,color:v==='CUT'?'#f4f1e8':'#0a0a0c'},hovertext:['<b>'+v+' ('+names.length+')</b><br>'+names.map(n=>e(n)).join('<br>')],hovertemplate:'%{hovertext}<extra></extra>'};
  });
  const layout={...desk7ChartBase(),barmode:'stack',height:104,margin:{l:8,r:8,t:8,b:28},xaxis:{range:[0,12],tickvals:[0,2,4,6,8,10],gridcolor:'rgba(128,128,128,.25)',zeroline:false,tickfont:{size:10,color:'#a39e93'}},yaxis:{showticklabels:false,showgrid:false,zeroline:false}};
  return P.newPlot(el,traces,layout,{responsive:true,displayModeBar:false});
}
async function renderDesk7GaugeChart(P,d){
  const el=document.getElementById('desk7-gauge-chart');if(!el)return;
  el.innerHTML='';
  const rows=d.indicators.map((x,i)=>({x,i})).filter(o=>o.x.gauge);
  const n=rows.length;
  const traces=[],shapes=[],annotations=[];
  const layout={...desk7ChartBase(),grid:{rows:n,columns:1,pattern:'independent',roworder:'top to bottom'},margin:{l:92,r:16,t:12,b:30},height:n*72+48};
  rows.forEach((o,k)=>{
    const g=o.x.gauge,ax=k===0?'x':'x'+(k+1),ay=k===0?'y':'y'+(k+1);
    const axKey=k===0?'xaxis':'xaxis'+(k+1),ayKey=k===0?'yaxis':'yaxis'+(k+1);
    const [lo,hi]=g.window;
    if(g.hike_at!=null){
      shapes.push({type:'rect',xref:ax,yref:ay,x0:g.hike_when==='above'?g.hike_at:lo,x1:g.hike_when==='above'?hi:g.hike_at,y0:-0.55,y1:0.75,fillcolor:'rgba(220,185,111,.08)',line:{width:0},layer:'below'});
      shapes.push({type:'line',xref:ax,yref:ay,x0:g.hike_at,x1:g.hike_at,y0:-0.55,y1:0.75,line:{color:'#dcb96f',width:1,dash:'dash'}});
    }
    if(g.cut_at!=null){
      shapes.push({type:'rect',xref:ax,yref:ay,x0:g.cut_when==='above'?g.cut_at:lo,x1:g.cut_when==='above'?hi:g.cut_at,y0:-0.55,y1:0.75,fillcolor:'rgba(74,144,217,.08)',line:{width:0},layer:'below'});
      shapes.push({type:'line',xref:ax,yref:ay,x0:g.cut_at,x1:g.cut_at,y0:-0.55,y1:0.75,line:{color:'#4a90d9',width:1,dash:'dash'}});
    }
    const hover=g.values.map((v,j)=>'<b>'+e(o.x.name)+'</b><br>'+e(g.labels[j])+': '+e(g.display[j])+' — '+o.x.vote+'<br>Trigger: '+e(o.x.trigger)+'<br>Read: '+e(o.x.read)+(g.note?'<br>'+e(g.note):''));
    const multi=g.values.length>1;
    if(multi){const mean=g.values.reduce((a,b)=>a+b,0)/g.values.length;annotations.push({xref:ax,yref:ay,x:mean,y:0.62,text:g.display.join(' / '),showarrow:false,font:{size:10,color:'#f4f1e8'}});}
    traces.push({x:g.values,y:g.values.map(()=>0),xaxis:ax,yaxis:ay,type:'scatter',mode:'markers+text',marker:{size:13,symbol:'diamond',color:DESK7_VOTE_COLOR[o.x.vote],line:{color:'#0a0a0c',width:1}},text:multi?g.values.map(()=> ''):g.display,textposition:'top center',textfont:{size:10,color:'#f4f1e8'},hovertext:hover,hovertemplate:'%{hovertext}<extra></extra>',customdata:g.values.map(()=>o.i)});
    layout[axKey]={range:[lo,hi],showgrid:true,gridcolor:'rgba(128,128,128,.25)',zeroline:false,nticks:4,tickfont:{size:9,color:'#a39e93'}};
    if(hi>=10000)layout[axKey].tickformat=',';
    layout[ayKey]={range:[-0.55,0.75],showticklabels:true,tickvals:[0],ticktext:[g.short+(g.unit?' ('+g.unit+')':'')],tickfont:{size:11,color:'#f4f1e8'},showgrid:false,zeroline:false};
  });
  layout.shapes=shapes;layout.annotations=annotations;
  await P.newPlot(el,traces,layout,{responsive:true,displayModeBar:false});
  el.on('plotly_click',ev=>{
    try{
      const idx=ev.points[0].customdata;
      const row=document.getElementById('desk7-row-'+idx);
      if(row){row.scrollIntoView({behavior:'smooth',block:'center'});row.style.background='rgba(198,161,91,.16)';setTimeout(()=>{row.style.background='';},1800);}
    }catch(_){}
  });
}
function renderDesk7KalshiChart(P,d){
  const el=document.getElementById('desk7-kalshi-chart');if(!el)return;
  el.innerHTML='';
  const m=d.market_pricing.kalshi_markets;
  if(!Array.isArray(m)||!m.length)throw Error('no kalshi markets');
  const FAM={hike:'#dcb96f',hold:'#a39e93',cut:'#4a90d9'};
  const rows=[...m].reverse();
  const trace={x:rows.map(r=>r.last),y:rows.map(r=>r.outcome),type:'bar',orientation:'h',marker:{color:rows.map(r=>FAM[r.family])},text:rows.map(r=>'$'+r.last.toFixed(2)),textposition:rows.map(r=>r.last>=0.5?'inside':'outside'),textfont:{size:11,color:rows.map(r=>r.last>=0.5?'#0a0a0c':'#f4f1e8')},hovertext:rows.map(r=>'<b>'+e(r.outcome)+'</b><br>Last $'+r.last.toFixed(2)+(r.bid!=null?'<br>Bid/ask '+r.bid.toFixed(2)+' / '+r.ask.toFixed(2):'')+(r.note?'<br>'+e(r.note):'')),hovertemplate:'%{hovertext}<extra></extra>'};
  const layout={...desk7ChartBase(),height:216,margin:{l:116,r:44,t:8,b:30},xaxis:{range:[0,1.0],tickvals:[0,0.25,0.5,0.75,1],tickprefix:'$',gridcolor:'rgba(128,128,128,.25)',zeroline:false,tickfont:{size:10,color:'#a39e93'}},yaxis:{tickfont:{size:11,color:'#f4f1e8'},showgrid:false,zeroline:false}};
  return P.newPlot(el,[trace],layout,{responsive:true,displayModeBar:false});
}
function fitFrame(f){try{const d=f.contentDocument;if(!d||!d.documentElement)return;const h=Math.max(d.documentElement.scrollHeight,d.body?d.body.scrollHeight:0);f.style.height=Math.max(500,h+8)+'px';}catch(_){}}
// The /dashboard chart wall is embedded from this same origin. On phones, Plotly's
// floating toolbar and redundant in-chart headings collide with chart content.
// The containing card already supplies a visible, readable heading. This is
// presentation-only; figures, axes, traces and calculations are untouched.
function fitMobilePlotlyChrome(f){try{
  if(!f.classList.contains('dash-frame'))return;
  const d=f.contentDocument;if(!d||!d.head||d.getElementById('hedge-mobile-plotly-qa'))return;
  const s=d.createElement('style');s.id='hedge-mobile-plotly-qa';
  s.textContent='@media(max-width:640px){.js-plotly-plot .plotly .modebar-container{display:none!important}.js-plotly-plot .gtitle{display:none!important}}';
  d.head.appendChild(s);
}catch(_){}}
function wireFrames(){document.querySelectorAll('#main iframe[data-autofit]').forEach(f=>{if(f.dataset.wired)return;f.dataset.wired='1';f.addEventListener('load',()=>{const sk=f.previousElementSibling;if(sk&&sk.classList.contains('skeleton'))sk.style.display='none';fitMobilePlotlyChrome(f);fitFrame(f);try{new ResizeObserver(()=>fitFrame(f)).observe(f.contentDocument.documentElement);}catch(_){}});});}
let framesResizeArmed=false;
function armFramesResize(){if(framesResizeArmed)return;framesResizeArmed=true;window.addEventListener('resize',()=>{document.querySelectorAll('#main iframe[data-wired]').forEach(fitFrame);});}
async function render(){route=location.hash.slice(1)||'overview';if(!title[route])route='overview';document.body.dataset.route=route;document.querySelectorAll('[data-nav]').forEach(a=>{a.classList.toggle('active',a.dataset.nav===route);if(a.dataset.nav===route)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});$('#breadcrumb').textContent=title[route];if(route==='overview')await ensureOverviewBrief();$('#main').innerHTML=({overview,dashboard,candidates,desks,desk5,desk7,controls,journal,resources,workbench,'real-estate':realEstate,brief,about})[route]();if(route==='candidates')hydrateGraham();if(route==='brief')hydrateBrief();if(route==='controls')hydrateMarketContext();if(route==='workbench')hydrateWorkbench();if(route==='real-estate')hydrateRealEstate();if(route==='desk5')hydrateDesk5();if(route==='desk7')hydrateDesk7();wireFrames();}
function download(name,content,type='application/json'){const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Download prepared');}
function toast(message){$('#toast').textContent=message;$('#toast').style.display='block';setTimeout(()=>$('#toast').style.display='none',3500)}
async function acceptPayload(candidate){if(candidate.schema_version!=='desk-console-1'||candidate.report?.environment!=='paper'||candidate.report.live_orders_enabled!==false||candidate.report.synthetic_data!==false||!Array.isArray(candidate.report.projects)||candidate.report.projects.length<6||!candidate.summary||!candidate.registry||candidate.candidate_feed?.schema_version!=='hedge-desk-candidates-1.0.0')throw Error('Unsupported report or paper boundary.');}
armFramesResize();
async function load(){const main=document.getElementById('main');const slow=setTimeout(()=>{if(main){const l=main.querySelector('.loading');if(l)l.textContent='Loading the overnight report…';}},2500);try{let viaApi=false,got=false;try{const response=await fetch('./api/report',{cache:'default'});if(response&&response.ok){const candidate=await response.json();await acceptPayload(candidate);data=candidate;viaApi=true;got=true}else if(response&&response.status===503){const body=await response.json().catch(()=>({}));throw Error('Data unavailable: '+(body.reason||'live market data could not be loaded.'))}}catch(err){if(!got)throw err}if(!data)throw Error('Report could not be loaded.');report=data.report;$('#reportstamp').textContent=`${viaApi?'Live engine report':'Deploy snapshot'} exported ${date(report.generated_at)}`;render();}catch(err){$('#main').innerHTML=`<div class="error"><h2>Research report unavailable</h2><p>${e(err.message)}</p><p>The console will not display decisions without its report.</p>${btn('reload','Try again')}</div>`;}finally{clearTimeout(slow);}}
document.addEventListener('click',event=>{const t=event.target.closest('button');if(!t)return;if(t.dataset.desk)openDesk(t.dataset.desk);if(t.dataset.exportDesk){const p=report.projects.find(p=>p.project_id===t.dataset.exportDesk);download(`${p.project_id}.json`,JSON.stringify({report_sha256:report.report_sha256,project:p},null,2));}if(t.dataset.noteDesk){$('#detail').close();location.hash='journal';render();$('#note-form select').value=t.dataset.noteDesk;$('#note-form textarea').focus()}switch(t.dataset.action){case 'toggle-graham':saveFilter(localStorage,!readFilter(localStorage));render();break;case 'open-full-dash':{const shell=document.getElementById('dash-full');const f=shell.querySelector('iframe');if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.src);shell.hidden=false;t.style.display='none';shell.scrollIntoView();break;}case 'close':$('#detail').close();break;case 'reload':t.disabled=true;load();break;case 'export-json':download('trade-desk-report.json',JSON.stringify(report,null,2));break;case 'export-md':download('trade-desk-live-report.json',JSON.stringify(report,null,2));break;case 'export-notes':download('trade-desk-yellow-sheets.json',JSON.stringify(notes(),null,2));break;}});
document.addEventListener('click',event=>{const t=event.target.closest('[data-action="export-candidates"]');if(t)download('trade-desk-candidates.json',JSON.stringify(data.candidate_feed,null,2));});
document.addEventListener('change',event=>{if(event.target.id==='graham-filter-toggle'){saveFilter(localStorage,event.target.checked);render();return;}const symbol=event.target.dataset.grahamOwn;if(!symbol)return;const value=event.target.value==='yes'?true:event.target.value==='no'?false:null;saveOwnIt(localStorage,symbol,value);render();});
document.addEventListener('submit',event=>{if(event.target.id!=='note-form')return;event.preventDefault();const f=new FormData(event.target);try{saveNote(localStorage,{id:crypto.randomUUID(),created_at:new Date().toISOString(),desk:f.get('desk'),thesis:f.get('thesis'),evidence:f.get('evidence'),invalidation:f.get('invalidation'),report_sha256:report.report_sha256});render();toast('Research note saved in this browser')}catch(err){toast('Could not save note: '+err.message)}});
window.addEventListener('hashchange',()=>{if(data)render()});
load();
