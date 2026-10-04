import { rentalDefaults, analysisDefaults, calcRental, calcAnalysis } from './real-estate-model.mjs';

const fmtMoney=v=>Number.isFinite(v)?new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(v):'N/A';
const fmtPct=v=>Number.isFinite(v)?new Intl.NumberFormat('en-US',{style:'percent',minimumFractionDigits:2,maximumFractionDigits:2}).format(v):'N/A';
const fmtNum=v=>Number.isFinite(v)?new Intl.NumberFormat('en-US',{maximumFractionDigits:2}).format(v):'N/A';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const moneyKeys=new Set(['purchasePrice','initialCapex','purchaseCosts','loanAmount','monthlyRent','propertyTax','insurance','utilities','advertising','other1','other2','unit2br','rent2br','unit1br','rent1br','unitStudio','rentStudio','nonResidentialSqFt','nonResidentialRentPerSf','salary','supplies','maintenance','propertyTaxes','mortgageAmount','depreciableBasis','sellingPrice','sellingCosts','transactionCosts']);
const pctKeys=new Set(['interestRate','rentIncrease','vacancy','improvementRatio','capRate','appreciationRate','saleCost','incomeTax','capitalGainsTax','financeRate','reinvestmentRate','propertyTaxIncrease','insuranceIncrease','utilitiesIncrease','advertisingIncrease','other1Increase','other2Increase','mgmtFee','repairs','other3','otherIncomePct','expenseGrowth','managementFee','mortgageRate','marginalTaxRate','recaptureTax','capRateInput','discountRate','noiVariation','salePriceVariation']);
const rentalGroups=[
 ['Acquisition & financing',['purchasePrice','initialCapex','purchaseCosts','purchaseDate','loanAmount','interestRate','amortMonths']],
 ['Rent & operations',['monthlyRent','rentInterval','rentIncrease','vacancy','improvementRatio','depreciationYears']],
 ['Disposition & taxes',['capRate','appreciationRate','saleCost','terminalOption','incomeTax','capitalGainsTax','financeRate','reinvestmentRate','selectMonth']],
 ['Property tax',['propertyTax','propertyTaxStart','propertyTaxIncrease']],
 ['Insurance',['insurance','insuranceStart','insuranceIncrease']],
 ['Utilities',['utilities','utilitiesStart','utilitiesIncrease']],
 ['Advertising',['advertising','advertisingStart','advertisingIncrease']],
 ['Other 1',['other1','other1Start','other1Increase']],
 ['Other 2',['other2','other2Start','other2Increase']],
 ['Variable expenses',['mgmtFee','mgmtStart','repairs','repairsStart','other3','other3Start']]
];
const analysisGroups=[
 ['Holding & rents',['holdYears','unit2br','rent2br','unit1br','rent1br','unitStudio','rentStudio','nonResidentialSqFt','nonResidentialRentPerSf','otherIncomePct']],
 ['Expenses',['expenseGrowth','managementFee','salary','utilities','insurance','supplies','advertising','maintenance','propertyTaxes']],
 ['Mortgage',['mortgageAmount','mortgageTermYears','mortgageRate','paymentsPerYear']],
 ['Taxes',['marginalTaxRate','depreciableBasis','recoveryYears']],
 ['Sale',['purchasePrice','transactionCosts','sellingPrice','sellingCosts','capitalGainsTax','recaptureTax']],
 ['Valuation ratios',['grmInput','gimInput','nimInput','capRateInput']],
 ['Risk',['discountRate','noiVariation','salePriceVariation']]
];
const labels={
 purchasePrice:'Purchase price',initialCapex:'Additional initial capex',purchaseCosts:'Purchase costs',purchaseDate:'Purchase date',loanAmount:'Loan amount',interestRate:'Interest rate',amortMonths:'Amortization months',
 monthlyRent:'Monthly rent',rentInterval:'Rent increase interval',rentIncrease:'Rent increase',vacancy:'Vacancy',improvementRatio:'Improvement ratio',depreciationYears:'Depreciation years',capRate:'Capitalization rate',
 appreciationRate:'Appreciation rate',saleCost:'Cost of sale',terminalOption:'Terminal value method',incomeTax:'Income tax',capitalGainsTax:'Capital gains tax',financeRate:'MIRR finance rate',reinvestmentRate:'MIRR reinvestment rate',selectMonth:'Selected hold month',
 propertyTax:'Property tax annual',propertyTaxStart:'Start month',propertyTaxIncrease:'Annual increase',insurance:'Insurance annual',insuranceStart:'Start month',insuranceIncrease:'Annual increase',utilities:'Utilities monthly',utilitiesStart:'Start month',utilitiesIncrease:'Annual increase',
 advertising:'Advertising annual',advertisingStart:'Start month',advertisingIncrease:'Annual increase',other1:'Other 1 annual',other1Start:'Start month',other1Increase:'Annual increase',other2:'Other 2 monthly',other2Start:'Start month',other2Increase:'Annual increase',
 mgmtFee:'Management fee',mgmtStart:'Start month',repairs:'Repairs & maintenance',repairsStart:'Start month',other3:'Other 3 annual % of income',other3Start:'Start month',
 holdYears:'Holding period',unit2br:'Two-bedroom units',rent2br:'Two-bedroom monthly rent',unit1br:'One-bedroom units',rent1br:'One-bedroom monthly rent',unitStudio:'Studio units',rentStudio:'Studio monthly rent',
 nonResidentialSqFt:'Non-residential sq ft',nonResidentialRentPerSf:'Annual rent / sq ft',otherIncomePct:'Other income %',expenseGrowth:'Annual expense growth',managementFee:'Management fee %',salary:'Salary',supplies:'Supplies',maintenance:'Maintenance & repairs',propertyTaxes:'Property taxes',
 mortgageAmount:'Mortgage amount',mortgageTermYears:'Mortgage term years',mortgageRate:'Mortgage interest rate',paymentsPerYear:'Payments per year',marginalTaxRate:'Marginal tax rate',depreciableBasis:'Depreciable basis',recoveryYears:'Recovery period',
 transactionCosts:'Transaction costs',sellingPrice:'Selling price',sellingCosts:'Selling costs',recaptureTax:'Depreciation recapture tax',grmInput:'Input GRM',gimInput:'Input GIM',nimInput:'Input NIM',capRateInput:'Input cap rate',
 discountRate:'Discount rate',noiVariation:'NOI sensitivity variation',salePriceVariation:'Sale price sensitivity variation'
};

function field(model,key,value){
  const id=`re-${model}-${key}`,label=labels[key]||key;
  if(key==='rentInterval') return `<label class="re-field"><span>${esc(label)}</span><select id="${id}" data-re-model="${model}" data-re-key="${key}">${['6-Mthly','Annually','2-Yrs','3-Yrs','4-Yrs','5-Yrs'].map(x=>`<option ${x===value?'selected':''}>${x}</option>`).join('')}</select></label>`;
  if(key==='terminalOption') return `<label class="re-field"><span>${esc(label)}</span><select id="${id}" data-re-model="${model}" data-re-key="${key}"><option value="1" ${Number(value)===1?'selected':''}>1 — Appreciation</option><option value="2" ${Number(value)===2?'selected':''}>2 — Cap rate</option></select></label>`;
  if(key==='purchaseDate') return `<label class="re-field"><span>${esc(label)}</span><input id="${id}" type="date" value="${esc(value)}" data-re-model="${model}" data-re-key="${key}"></label>`;
  const pct=pctKeys.has(key),money=moneyKeys.has(key),step=pct?'0.0001':money?'100':'1';
  return `<label class="re-field"><span>${esc(label)}${pct?' (%)':''}</span><input id="${id}" type="number" step="${step}" value="${pct?(Number(value)*100):esc(value)}" data-re-model="${model}" data-re-key="${key}" data-re-pct="${pct?'1':'0'}"></label>`;
}
function group(title,model,keys,state){return `<details class="re-input-group" open><summary>${esc(title)}</summary><div class="re-fields">${keys.map(k=>field(model,k,state[k])).join('')}</div></details>`;}
function yearArray(title,model,key,vals,pct=true){return `<details class="re-input-group"><summary>${title}</summary><div class="re-year-grid">${vals.map((v,i)=>`<label class="re-field"><span>Year ${i+1}</span><input type="number" step="0.01" value="${pct?v*100:v}" data-re-model="${model}" data-re-array="${key}" data-re-index="${i}" data-re-pct="${pct?'1':'0'}"></label>`).join('')}</div></details>`;}
function stats(items){return `<div class="re-stats">${items.map(([l,v,s])=>`<article><span>${l}</span><strong>${v}</strong><small>${s||''}</small></article>`).join('')}</div>`;}
function table(headers,rows){return `<div class="re-table-wrap"><table class="re-table"><thead><tr>${headers.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`;}

function rentalResults(r){
  const s=r.rows[r.selectedMonth-1]||r.rows[0];
  const detail=table(['Mo','Date','Gross rent','Vacancy','Gross income','OpEx','NOI','Interest','Principal','Debt service','Balance','Depreciation','Taxable income','Income tax','TV before tax','Cap gain','CG tax','TV after tax','CFBT','CFAT','IRR ann.','MIRR ann.'],
    r.rows.map(x=>`<tr><td>${x.month}</td><td>${x.date}</td><td>${fmtMoney(x.rent)}</td><td>${fmtMoney(x.vacancy)}</td><td>${fmtMoney(x.gross)}</td><td>${fmtMoney(x.opEx)}</td><td>${fmtMoney(x.noi)}</td><td>${fmtMoney(x.interest)}</td><td>${fmtMoney(x.principal)}</td><td>${fmtMoney(x.payment)}</td><td>${fmtMoney(x.balance)}</td><td>${fmtMoney(x.depreciation)}</td><td>${fmtMoney(x.taxableIncome)}</td><td>${fmtMoney(x.incomeTax)}</td><td>${fmtMoney(x.terminalBeforeTax)}</td><td>${fmtMoney(x.capitalGain)}</td><td>${fmtMoney(x.capGainsTax)}</td><td>${fmtMoney(x.terminalAfterTax)}</td><td>${fmtMoney(x.cfbt)}</td><td>${fmtMoney(x.cfat)}</td><td>${fmtPct(x.irrAnnual)}</td><td>${fmtPct(x.mirrAnnual)}</td></tr>`));
  const cap=table(['Cap rate','Monthly IRR','Annual IRR'],r.capScenarios.map(x=>`<tr><td>${fmtPct(x.rate)}</td><td>${fmtPct(x.irrMonthly)}</td><td>${fmtPct(x.irrAnnual)}</td></tr>`));
  const rate=table(['Mortgage rate','Monthly IRR','Annual IRR'],r.rateScenarios.map(x=>`<tr><td>${fmtPct(x.rate)}</td><td>${fmtPct(x.irrMonthly)}</td><td>${fmtPct(x.irrAnnual)}</td></tr>`));
  return stats([
    ['Total initial cost',fmtMoney(r.totalInitialCost),'Purchase + capex + costs'],
    ['Down payment',fmtMoney(r.downPayment),'Initial equity'],
    [`Year ${Math.ceil(r.selectedMonth/12)} NOI`,fmtMoney(r.rows.slice(Math.max(0,r.selectedMonth-12),r.selectedMonth).reduce((a,x)=>a+x.noi,0)),'Trailing 12 months'],
    ['Annual IRR',fmtPct(s.irrAnnual),`As if sold month ${r.selectedMonth}`],
    ['Annual MIRR',fmtPct(s.mirrAnnual),`As if sold month ${r.selectedMonth}`],
    ['XIRR',fmtPct(r.xirr),'CFAT using actual dates']
  ])+`<section class="re-card"><h3>Selected-month disposition</h3><div class="re-kv"><span>Terminal value before tax</span><strong>${fmtMoney(s.terminalBeforeTax)}</strong><span>Mortgage payoff</span><strong>${fmtMoney(s.balance)}</strong><span>Terminal value after capital-gains tax</span><strong>${fmtMoney(s.terminalAfterTax)}</strong><span>Terminal CFBT</span><strong>${fmtMoney(s.terminalCfbt)}</strong></div></section>`+
  `<div class="re-two"><section class="re-card"><h3>Cap-rate sensitivity</h3>${cap}</section><section class="re-card"><h3>Interest-rate sensitivity</h3>${rate}</section></div>`+
  `<details class="re-card"><summary>Monthly model — all outputs</summary>${detail}</details>`;
}
function analysisResults(r){
  const y=r.years[0],z=r.ratios;
  const annual=table(['Yr','PGR','Vacancy','EGI','Expenses','NOI','Debt service','Interest','Principal','Balance','Depreciation','Taxable income','Tax','BTCF','ATCF'],
    r.years.map(x=>`<tr><td>${x.year}</td><td>${fmtMoney(x.pgr)}</td><td>${fmtMoney(x.vacancy)}</td><td>${fmtMoney(x.egi)}</td><td>${fmtMoney(x.totalExpenses)}</td><td>${fmtMoney(x.noi)}</td><td>${fmtMoney(x.debtService)}</td><td>${fmtMoney(x.interest)}</td><td>${fmtMoney(x.principal)}</td><td>${fmtMoney(x.mortgageBalance)}</td><td>${fmtMoney(x.depreciation)}</td><td>${fmtMoney(x.taxableIncome)}</td><td>${fmtMoney(x.incomeTaxes)}</td><td>${fmtMoney(x.btcf)}</td><td>${fmtMoney(x.atcf)}</td></tr>`));
  return stats([
    ['Year 1 NOI',fmtMoney(y.noi),'Operating'],
    ['Year 1 BTCF',fmtMoney(y.btcf),'NOI − debt service'],
    ['Year 1 ATCF',fmtMoney(y.atcf),'BTCF − tax'],
    ['Before-tax IRR',fmtPct(r.beforeTaxIrr),'DCF stream'],
    ['After-tax IRR',fmtPct(r.afterTaxIrr),'DCF stream'],
    ['NPV',fmtMoney(r.npv),`Discounted at ${fmtPct(r.inputs.discountRate)}`]
  ])+`<div class="re-two"><section class="re-card"><h3>Sale / equity reversion</h3><div class="re-kv"><span>Initial equity</span><strong>${fmtMoney(r.initialEquity)}</strong><span>Cumulative depreciation</span><strong>${fmtMoney(r.sale.cumDep)}</strong><span>Adjusted basis at sale</span><strong>${fmtMoney(r.sale.adjustedBasis)}</strong><span>Gain on disposal</span><strong>${fmtMoney(r.sale.gain)}</strong><span>Sale tax</span><strong>${fmtMoney(r.sale.saleTax)}</strong><span>Mortgage balance</span><strong>${fmtMoney(r.sale.mortgageBalance)}</strong><span>Before-tax equity reversion</span><strong>${fmtMoney(r.sale.bter)}</strong><span>After-tax equity reversion</span><strong>${fmtMoney(r.sale.ater)}</strong></div></section>
  <section class="re-card"><h3>Ratios & implied values</h3><div class="re-kv"><span>GRM</span><strong>${fmtNum(z.grm)}</strong><span>GIM</span><strong>${fmtNum(z.gim)}</strong><span>NIM</span><strong>${fmtNum(z.nim)}</strong><span>Operating ratio</span><strong>${fmtPct(z.operating)}</strong><span>Break-even ratio</span><strong>${fmtPct(z.breakEven)}</strong><span>DSCR</span><strong>${fmtNum(z.dscr)}</strong><span>LTV</span><strong>${fmtPct(z.ltv)}</strong><span>Cap rate</span><strong>${fmtPct(z.capRate)}</strong><span>BT equity dividend rate</span><strong>${fmtPct(z.beforeTaxEquityDividend)}</strong><span>AT equity dividend rate</span><strong>${fmtPct(z.afterTaxEquityDividend)}</strong><span>GRM value</span><strong>${fmtMoney(z.grmValue)}</strong><span>GIM value</span><strong>${fmtMoney(z.gimValue)}</strong><span>NIM value</span><strong>${fmtMoney(z.nimValue)}</strong><span>Cap-rate value</span><strong>${fmtMoney(z.capValue)}</strong></div></section></div>`+
  `<section class="re-card"><h3>Risk</h3><div class="re-kv"><span>Payback period</span><strong>${Number.isFinite(r.payback)?fmtNum(r.payback)+' years':'N/A'}</strong><span>Base NPV</span><strong>${fmtMoney(r.npv)}</strong><span>NOI varied NPV</span><strong>${fmtMoney(r.risk.noiNpv)}</strong><span>NOI value change</span><strong>${fmtMoney(r.risk.noiChange)}</strong><span>NOI elasticity</span><strong>${fmtPct(r.risk.noiElasticity)}</strong><span>Sale varied NPV</span><strong>${fmtMoney(r.risk.saleNpv)}</strong><span>Sale value change</span><strong>${fmtMoney(r.risk.saleChange)}</strong><span>Sale elasticity</span><strong>${fmtPct(r.risk.saleElasticity)}</strong></div></section>`+
  `<details class="re-card" open><summary>Annual pro forma — all outputs</summary>${annual}</details>`;
}
function readState(host,model,base){
  const state=structuredClone(base);
  host.querySelectorAll(`[data-re-model="${model}"][data-re-key]`).forEach(el=>{let v=el.type==='number'?Number(el.value):el.value;if(el.dataset.rePct==='1')v/=100;state[el.dataset.reKey]=v;});
  host.querySelectorAll(`[data-re-model="${model}"][data-re-array]`).forEach(el=>{let v=Number(el.value);if(el.dataset.rePct==='1')v/=100;state[el.dataset.reArray][Number(el.dataset.reIndex)]=v;});
  return state;
}
function renderInvestment(host){
  const p=readState(host,'rental',rentalDefaults),r=calcRental(p);host.querySelector('[data-re-results="rental"]').innerHTML=rentalResults(r);
}
function renderAnalysis(host){
  const p=readState(host,'analysis',analysisDefaults),r=calcAnalysis(p);host.querySelector('[data-re-results="analysis"]').innerHTML=analysisResults(r);
}
export function realEstatePage(){
  return `<div class="re-shell"><div class="page-head"><div><h1>Real estate decision models</h1><p class="subtitle">Spreadsheet-parity underwriting tools for leveraged rental investment and annual acquisition analysis.</p></div></div>
  <div class="notice"><strong>Corrected model port</strong><span>Known spreadsheet defects are corrected here: year-8 <code>&gt;77</code> expense guards, NOI sensitivity sale-price leakage, hardcoded 5% sensitivity selling cost, and dead legacy named-range sections. Rental expense tail behavior remains workbook-compatible.</span></div>
  <div class="re-tabs" role="tablist"><button class="re-tab active" data-re-tab="rental">Investment</button><button class="re-tab" data-re-tab="analysis">Analysis</button></div>
  <section class="re-pane active" data-re-pane="rental"><div class="re-layout"><aside class="re-inputs"><h2>Investment inputs</h2>${rentalGroups.map(([t,k])=>group(t,'rental',k,rentalDefaults)).join('')}</aside><div class="re-results" data-re-results="rental"></div></div></section>
  <section class="re-pane" data-re-pane="analysis"><div class="re-layout"><aside class="re-inputs"><h2>Analysis inputs</h2>${analysisGroups.map(([t,k])=>group(t,'analysis',k,analysisDefaults)).join('')}${yearArray('Rent growth by year','analysis','rentGrowth',analysisDefaults.rentGrowth)}${yearArray('Vacancy by year','analysis','vacancy',analysisDefaults.vacancy)}${yearArray('Property-tax increase by year','analysis','propertyTaxGrowth',analysisDefaults.propertyTaxGrowth)}</aside><div class="re-results" data-re-results="analysis"></div></div></section></div>`;
}
export function mountRealEstate(host){
  if(!host)return;renderInvestment(host);renderAnalysis(host);
  host.addEventListener('click',e=>{const b=e.target.closest('[data-re-tab]');if(!b)return;host.querySelectorAll('.re-tab').forEach(x=>x.classList.toggle('active',x===b));host.querySelectorAll('.re-pane').forEach(x=>x.classList.toggle('active',x.dataset.rePane===b.dataset.reTab));});
  let timer;host.addEventListener('input',e=>{if(!e.target.closest('[data-re-model]'))return;clearTimeout(timer);timer=setTimeout(()=>e.target.dataset.reModel==='rental'?renderInvestment(host):renderAnalysis(host),80);});
  host.addEventListener('change',e=>{if(!e.target.closest('[data-re-model]'))return;e.target.dataset.reModel==='rental'?renderInvestment(host):renderAnalysis(host);});
}
