import test from 'node:test';
import assert from 'node:assert/strict';
import {escapeHTML,scenarioRows,filterRows,readNotes,saveNote,statusClass,reasonList} from './core.mjs';
test('reason_codes is normalised to a list for every reader',()=>{
  const rows=scenarioRows({scenarios:[
    {scenario_id:'a',group:'arbitrage',reason_codes:'EDGE_BELOW_SAFETY_BUFFER'},
    {scenario_id:'blank',group:'arbitrage',reason_codes:''},
    {scenario_id:'listed',group:'arbitrage',reason_codes:['ONE','TWO']},
    {scenario_id:'p',group:'portfolio_stress'}
  ]});
  const byId=Object.fromEntries(rows.map(r=>[r.scenario_id,r]));
  assert.deepEqual(byId.a.reason_codes,['EDGE_BELOW_SAFETY_BUFFER']);
  assert.deepEqual(byId.blank.reason_codes,[]);
  assert.deepEqual(byId.listed.reason_codes,['ONE','TWO']);
  assert.deepEqual(byId.p.reason_codes,[]);
  for(const r of rows){assert.ok(Array.isArray(r.reason_codes),r.scenario_id);assert.doesNotThrow(()=>r.reason_codes.map(x=>x),r.scenario_id);}
  assert.deepEqual(reasonList(undefined),[]);
  assert.deepEqual(reasonList('X'),['X']);
});
const report={report_sha256:'fixture-report-sha256',scenarios:[
  {scenario_id:'a',group:'arbitrage',reason_codes:'EDGE_BELOW_SAFETY_BUFFER',disposition:'NO_TRADE'},
  {scenario_id:'blank',group:'other',reason_codes:'',disposition:'NO_TRADE'},
  {scenario_id:'listed',group:'other',reason_codes:['ONE','TWO'],disposition:'NO_TRADE'},
  {scenario_id:'audit-hash',group:'audit_attacks',reason_codes:'HASH_MISMATCH',disposition:'NO_TRADE'},
  {scenario_id:'portfolio-stress-1',group:'portfolio_stress',disposition:'FREEZE_NEW_RISK',combined_net_pnl:'-4655.60'},
  {scenario_id:'portfolio-stress-2',group:'portfolio_stress',disposition:'FREEZE_NEW_RISK'},
  {scenario_id:'portfolio-stress-3',group:'portfolio_stress',disposition:'FREEZE_NEW_RISK'},
  {scenario_id:'portfolio-stress-4',group:'portfolio_stress',disposition:'FREEZE_NEW_RISK'},
  {scenario_id:'portfolio-stress-5',group:'portfolio_stress',disposition:'FREEZE_NEW_RISK'}
]};
const declaredScenarioIds=report.scenarios.map(s=>s.scenario_id);

test('all declared scenarios are accessible without changing their results',()=>{const rows=scenarioRows(report);const ids=new Set(rows.map(r=>r.scenario_id));for(const id of declaredScenarioIds)assert.ok(ids.has(id),id);assert.equal(rows.filter(r=>r.group==='portfolio_stress').length,5);assert.equal(rows.find(r=>r.scenario_id==='portfolio-stress-1').combined_net_pnl,'-4655.60');});
test('search combines reason, group and decision filters',()=>{const rows=scenarioRows(report);assert.ok(filterRows(rows,'HASH','audit_attacks','NO_TRADE').length>0);assert.equal(filterRows(rows,'not-a-scenario').length,0);assert.ok(filterRows(rows,'','portfolio_stress','FREEZE_NEW_RISK').every(r=>r.disposition==='FREEZE_NEW_RISK'));});
test('untrusted notes and evidence are escaped',()=>{assert.equal(escapeHTML('<img src=x onerror="x">'), '&lt;img src=x onerror=&quot;x&quot;&gt;');});
test('notes persist with report identity and cannot silently replace corrupt storage',()=>{let value=null;const storage={getItem:()=>value,setItem:(_,v)=>value=v};const note={id:'fixed-id',created_at:'2026-09-06T00:00:00Z',desk:'overnight-premium-desk',thesis:'A thesis',evidence:'A reference',invalidation:'A falsifier',report_sha256:report.report_sha256};saveNote(storage,note);assert.deepEqual(readNotes(storage),[note]);assert.throws(()=>saveNote(storage,{...note,thesis:' '}));value='invalid';assert.throws(()=>saveNote(storage,note));assert.equal(value,'invalid');});
test('control status remains blocked or pending as recorded',()=>{assert.equal(statusClass('NO_TRADE'),'blocked');assert.equal(statusClass('HUMAN_REVIEW'),'pending');assert.equal(statusClass('NOT_REQUIRED'),'');});
