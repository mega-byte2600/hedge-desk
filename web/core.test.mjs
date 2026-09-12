import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {escapeHTML,scenarioRows,filterRows,readNotes,saveNote,statusClass,reasonList} from './core.mjs';
test('reason_codes is normalised to a list for every reader',()=>{
  // The arbitrage group emits reason_codes as a bare string; the table indexes it
  // (rendering a single letter) and the detail dialog maps it (throwing). Normalising
  // in scenarioRows fixes both.
  const rows=scenarioRows({war_games:{arbitrage:[
    {scenario_id:'a',reason_codes:'EDGE_BELOW_SAFETY_BUFFER'},
    {scenario_id:'blank',reason_codes:''},
    {scenario_id:'listed',reason_codes:['ONE','TWO']}],
  },portfolio_stress:{scenarios:[{scenario_id:'p'}]}});
  const byId=Object.fromEntries(rows.map(r=>[r.scenario_id,r]));
  assert.deepEqual(byId.a.reason_codes,['EDGE_BELOW_SAFETY_BUFFER']);
  assert.deepEqual(byId.blank.reason_codes,[]);
  assert.deepEqual(byId.listed.reason_codes,['ONE','TWO']);
  assert.deepEqual(byId.p.reason_codes,[]);
  for(const r of rows){assert.ok(Array.isArray(r.reason_codes),r.scenario_id);assert.doesNotThrow(()=>r.reason_codes.map(x=>x),r.scenario_id);}
  assert.deepEqual(reasonList(undefined),[]);
  assert.deepEqual(reasonList('X'),['X']);
});
const {report}=JSON.parse(readFileSync(new URL('./report.json',import.meta.url)));
test('all declared scenarios are accessible without changing their results',()=>{const rows=scenarioRows(report);const ids=new Set(rows.map(r=>r.scenario_id));for(const id of report.war_games.fixture_manifest.scenario_ids)assert.ok(ids.has(id),id);assert.equal(rows.filter(r=>r.group==='portfolio_stress').length,5);assert.equal(rows.find(r=>r.scenario_id==='all-signals-crowded-exit').combined_net_pnl,'-4655.60');});
test('search combines reason, group and decision filters',()=>{const rows=scenarioRows(report);assert.ok(filterRows(rows,'HASH','audit_attacks','NO_TRADE').length>0);assert.equal(filterRows(rows,'not-a-scenario').length,0);assert.ok(filterRows(rows,'','portfolio_stress','FREEZE_NEW_RISK').every(r=>r.disposition==='FREEZE_NEW_RISK'));});
test('untrusted notes and evidence are escaped',()=>{assert.equal(escapeHTML('<img src=x onerror="x">'), '&lt;img src=x onerror=&quot;x&quot;&gt;');});
test('notes persist with report identity and cannot silently replace corrupt storage',()=>{let value=null;const storage={getItem:()=>value,setItem:(_,v)=>value=v};const note={id:'fixed-id',created_at:'2026-09-06T00:00:00Z',desk:'overnight-premium-desk',thesis:'A thesis',evidence:'A reference',invalidation:'A falsifier',report_sha256:report.report_sha256};saveNote(storage,note);assert.deepEqual(readNotes(storage),[note]);assert.throws(()=>saveNote(storage,{...note,thesis:' '}));value='invalid';assert.throws(()=>saveNote(storage,note));assert.equal(value,'invalid');});
test('control status remains blocked or pending as recorded',()=>{assert.equal(statusClass('NO_TRADE'),'blocked');assert.equal(statusClass('HUMAN_REVIEW'),'pending');assert.equal(statusClass('NOT_REQUIRED'),'');});
