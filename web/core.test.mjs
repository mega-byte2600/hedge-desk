import test from 'node:test';
import assert from 'node:assert/strict';
import {escapeHTML,scenarioRows,filterRows,readNotes,saveNote,statusClass,reasonList} from './core.mjs';

const report={
  report_sha256:'live-report-sha',
  scenarios:[
    {scenario_id:'a',group:'hypothetical-move',reason_codes:'EDGE_BELOW_SAFETY_BUFFER',disposition:'NO_TRADE'},
    {scenario_id:'blank',group:'hypothetical-move',reason_codes:'',disposition:'HUMAN_REVIEW'},
    {scenario_id:'listed',group:'audit_attacks',reason_codes:['ONE','HASH'],disposition:'NO_TRADE'},
    {scenario_id:'portfolio',group:'portfolio_stress',reason_codes:[],disposition:'FREEZE_NEW_RISK',combined_net_pnl:'-4655.60'},
  ],
};

test('reason_codes is normalised to a list for every scenario reader',()=>{
  const rows=scenarioRows(report);
  const byId=Object.fromEntries(rows.map(r=>[r.scenario_id,r]));
  assert.deepEqual(byId.a.reason_codes,['EDGE_BELOW_SAFETY_BUFFER']);
  assert.deepEqual(byId.blank.reason_codes,[]);
  assert.deepEqual(byId.listed.reason_codes,['ONE','HASH']);
  assert.deepEqual(byId.portfolio.reason_codes,[]);
  for(const r of rows){
    assert.ok(Array.isArray(r.reason_codes),r.scenario_id);
    assert.doesNotThrow(()=>r.reason_codes.map(x=>x),r.scenario_id);
  }
  assert.deepEqual(reasonList(undefined),[]);
  assert.deepEqual(reasonList('X'),['X']);
});

test('all declared live-console scenarios are accessible without changing their results',()=>{
  const rows=scenarioRows(report);
  assert.deepEqual(rows.map(r=>r.scenario_id),report.scenarios.map(r=>r.scenario_id));
  assert.equal(rows.filter(r=>r.group==='portfolio_stress').length,1);
  assert.equal(rows.find(r=>r.scenario_id==='portfolio').combined_net_pnl,'-4655.60');
});

test('search combines reason, group and decision filters',()=>{
  const rows=scenarioRows(report);
  assert.ok(filterRows(rows,'HASH','audit_attacks','NO_TRADE').length>0);
  assert.equal(filterRows(rows,'not-a-scenario').length,0);
  assert.ok(filterRows(rows,'','portfolio_stress','FREEZE_NEW_RISK').every(r=>r.disposition==='FREEZE_NEW_RISK'));
});

test('untrusted notes and evidence are escaped',()=>{
  assert.equal(escapeHTML('<img src=x onerror="x">'),'&lt;img src=x onerror=&quot;x&quot;&gt;');
});

test('notes persist with report identity and cannot silently replace corrupt storage',()=>{
  let value=null;
  const storage={getItem:()=>value,setItem:(_,v)=>value=v};
  const note={id:'fixed-id',created_at:'2026-09-06T00:00:00Z',desk:'overnight-premium-desk',thesis:'A thesis',evidence:'A reference',invalidation:'A falsifier',report_sha256:report.report_sha256};
  saveNote(storage,note);
  assert.deepEqual(readNotes(storage),[note]);
  assert.throws(()=>saveNote(storage,{...note,thesis:' '}));
  value='invalid';
  assert.throws(()=>saveNote(storage,note));
  assert.equal(value,'invalid');
});

test('control status remains blocked or pending as recorded',()=>{
  assert.equal(statusClass('NO_TRADE'),'blocked');
  assert.equal(statusClass('HUMAN_REVIEW'),'pending');
  assert.equal(statusClass('NOT_REQUIRED'),'');
});
