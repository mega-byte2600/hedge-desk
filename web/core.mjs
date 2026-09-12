export const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const human = value => String(value).replace(/[_-]/g,' ').toLowerCase().replace(/^./,c=>c.toUpperCase());
export const statusClass = value => /^(PASS|WITHIN_SYNTHETIC_LIMIT|RESEARCH_CONTROL_PASS)$/.test(value)?'pass':/BLOCK|NO_TRADE|FREEZE|UNSATISFIED/.test(value)?'blocked':/PENDING|HUMAN_REVIEW|REVIEW_REQUIRED/.test(value)?'pending':'';
export function scenarioRows(report){const rows=[];for(const [group,value] of Object.entries(report.war_games)){if(Array.isArray(value))for(const item of value)if(item&&typeof item==='object'&&item.scenario_id)rows.push({...item,group});}for(const item of report.portfolio_stress.scenarios)rows.push({...item,group:'portfolio_stress'});return rows;}
export function filterRows(rows,query='',group='',state=''){const q=query.toLowerCase().trim();return rows.filter(r=>(!group||r.group===group)&&(!state||r.disposition===state)&&(!q||[r.scenario_id,...(r.reason_codes||[])].join(' ').toLowerCase().includes(q)));}
const KEY='trade-desk-yellow-sheets-v1';
export function readNotes(storage){const raw=storage.getItem(KEY);if(!raw)return [];const parsed=JSON.parse(raw);if(!Array.isArray(parsed)||parsed.some(n=>!n||['id','created_at','desk','thesis','evidence','invalidation','report_sha256'].some(k=>typeof n[k]!=='string')))throw Error('Stored notes are invalid. Export or recover browser storage before saving.');return parsed;}
export function saveNote(storage,note){for(const key of ['thesis','evidence','invalidation']){if(typeof note[key]!=='string'||!note[key].trim()||note[key].length>6000)throw Error('Complete all research fields.');}const notes=readNotes(storage);storage.setItem(KEY,JSON.stringify([...notes,note]));return note;}
// One route derivation for every enhancer. These had drifted: app.js treats a
// hashless or unknown hash as 'candidates' (the HTML's default nav), while three
// enhancers treated the same state as 'overview' — so on a plain "/" load the
// overview subtitle was written onto the Candidates page. The query string is
// stripped for the same reason app.js keys routes off `location.hash.slice(1)`.
export function currentRoute(){return (location.hash||'#candidates').slice(1).split('?')[0]||'candidates';}
