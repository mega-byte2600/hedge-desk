// Deterministic real-estate decision models derived from the user's Excel workbooks.
// Money calculations are deterministic JS numbers here; Analysis mode reproduces Excel's $100 rounding cadence.

export const rentalDefaults = {
  purchasePrice: 20000000, initialCapex: 500000, purchaseCosts: 200000, purchaseDate: '2009-12-15',
  loanAmount: 9500000, interestRate: 0.055, amortMonths: 360, monthlyRent: 160000,
  rentInterval: '2-Yrs', rentIncrease: 0.17, vacancy: 0.05, improvementRatio: 0.6,
  depreciationYears: 39, capRate: 0.08, appreciationRate: 0.05, saleCost: 0.04,
  terminalOption: 2, incomeTax: 0.30, capitalGainsTax: 0.20, financeRate: 0.0125,
  reinvestmentRate: 0.015, selectMonth: 36,
  propertyTax: 47000, propertyTaxStart: 2, propertyTaxIncrease: 0.035,
  insurance: 12000, insuranceStart: 6, insuranceIncrease: 0.0275,
  utilities: 450, utilitiesStart: 4, utilitiesIncrease: 0.0325,
  advertising: 11500, advertisingStart: 7, advertisingIncrease: 0.0567,
  other1: 4500, other1Start: 5, other1Increase: 0.04,
  other2: 550, other2Start: 1, other2Increase: 0.025,
  mgmtFee: 0.009, mgmtStart: 4, repairs: 0.011, repairsStart: 1,
  other3: 0.0128, other3Start: 2, months: 132
};

export const analysisDefaults = {
  holdYears: 6,
  unit2br: 50, rent2br: 858, unit1br: 150, rent1br: 704, unitStudio: 80, rentStudio: 528,
  nonResidentialSqFt: 0, nonResidentialRentPerSf: 0,
  rentGrowth: [0.025,0.05,0.05,0.035,0.035,0.035,0,0,0,0],
  vacancy: [0.075,0.04,0.04,0.06,0.06,0.06,0,0,0,0],
  otherIncomePct: 0.047, expenseGrowth: 0.035, managementFee: 0.05,
  salary: 197100, utilities: 105300, insurance: 35500, supplies: 21000,
  advertising: 32000, maintenance: 181900, propertyTaxes: 300000,
  propertyTaxGrowth: [0,0,0,0.25,0,0,0,0,0,0],
  mortgageAmount: 8000000, mortgageTermYears: 20, mortgageRate: 0.08, paymentsPerYear: 12,
  marginalTaxRate: 0.40, depreciableBasis: 9300000, recoveryYears: 27.5,
  purchasePrice: 11444500, transactionCosts: 150000, sellingPrice: 17800000, sellingCosts: 890000,
  capitalGainsTax: 0.20, recaptureTax: 0.25,
  grmInput: 5, gimInput: 5, nimInput: 9, capRateInput: 0.10,
  discountRate: 0.10, noiVariation: 0.10, salePriceVariation: 0.10
};

const intervalMonths = {'6-Mthly':6,'Annually':12,'2-Yrs':24,'3-Yrs':36,'4-Yrs':48,'5-Yrs':60};
const safe = n => Number.isFinite(Number(n)) ? Number(n) : 0;
export const round100 = x => Math.round((safe(x)/1000)*10)/10*1000;

export function pmt(rate,nper,pv){
  if(!nper) return 0;
  if(Math.abs(rate) < 1e-15) return -pv/nper;
  const a=(1+rate)**nper;
  return -(rate*pv*a)/(a-1);
}
export function pv(rate,nper,payment){
  if(!nper) return 0;
  if(Math.abs(rate) < 1e-15) return -payment*nper;
  return -payment*(1-(1+rate)**(-nper))/rate;
}
export function irr(values, guess=0.1){
  const vals=values.map(safe);
  let x=guess;
  for(let k=0;k<100;k++){
    if(x<=-0.999999999) x=-0.9999;
    let f=0,df=0;
    for(let i=0;i<vals.length;i++){const d=(1+x)**i;f+=vals[i]/d;if(i)df-=i*vals[i]/((1+x)**(i+1));}
    if(Math.abs(df)<1e-14) break;
    const nx=x-f/df;
    if(!Number.isFinite(nx)) break;
    if(Math.abs(nx-x)<1e-12) return nx;
    x=nx;
  }
  let lo=-0.9999, hi=10, flo=npv0(vals,lo), fhi=npv0(vals,hi);
  if(flo*fhi>0) return NaN;
  for(let k=0;k<200;k++){const mid=(lo+hi)/2,f=npv0(vals,mid);if(Math.abs(f)<1e-10)return mid;if(flo*f<=0){hi=mid;fhi=f}else{lo=mid;flo=f}}
  return (lo+hi)/2;
}
function npv0(vals,r){return vals.reduce((s,v,i)=>s+v/((1+r)**i),0)}
export function xirr(values,dates,guess=0.1){
  if(values.length!==dates.length||values.length<2)return NaN;
  const t0=new Date(dates[0]).getTime();
  const years=dates.map(d=>(new Date(d).getTime()-t0)/86400000/365);
  let x=guess;
  for(let k=0;k<100;k++){
    if(x<=-0.999999)x=-0.9999;
    let f=0,df=0;
    for(let i=0;i<values.length;i++){const p=(1+x)**years[i];f+=safe(values[i])/p;df-=years[i]*safe(values[i])/((1+x)**(years[i]+1));}
    if(Math.abs(df)<1e-14)break;
    const nx=x-f/df;if(!Number.isFinite(nx))break;if(Math.abs(nx-x)<1e-12)return nx;x=nx;
  }
  return NaN;
}
export function mirr(values,finance,reinvest){
  const n=values.length;if(n<2)return NaN;
  let pvNeg=0,fvPos=0;
  values.forEach((v,i)=>{v=safe(v);if(v<0)pvNeg+=v/((1+finance)**i);else if(v>0)fvPos+=v*((1+reinvest)**(n-1-i));});
  if(pvNeg===0||fvPos===0)return NaN;
  return (fvPos/(-pvNeg))**(1/(n-1))-1;
}
function addMonths(iso,m){const d=new Date(iso+'T00:00:00Z');d.setUTCMonth(d.getUTCMonth()+m);return d.toISOString().slice(0,10)}
function annualExpense(month,start,base,incr,carry=false,prev=0){
  start=safe(start); if(!start||month<start) return 0;
  const delta=month-start;
  if(delta%12===0 && delta<=120) return safe(base)*((1+safe(incr))**(delta/12));
  return carry ? prev : 0;
}
function mortgageSchedule(principal,annualRate,nper,months){
  const r=annualRate/12, pay=principal>0&&nper>0?-pmt(r,nper,principal):0;
  let bal=principal, out=[];
  for(let m=1;m<=months;m++){
    if(principal<=0||m>nper){out.push({payment:0,interest:0,principal:0,balance:Math.max(0,bal)});continue;}
    const interest=bal*r, princ=Math.min(bal,pay-interest);bal=Math.max(0,bal-princ);
    out.push({payment:pay,interest,principal:princ,balance:bal});
  }
  return out;
}
export function calcRental(input={}){
  const p={...rentalDefaults,...input};
  const total=safe(p.purchasePrice)+safe(p.initialCapex)+safe(p.purchaseCosts);
  const leveraged=safe(p.loanAmount)>0 && safe(p.interestRate)>0 && safe(p.amortMonths)>0;
  const down=leveraged?total-safe(p.loanAmount):total;
  const improvement=total*safe(p.improvementRatio), depAnnual=safe(p.depreciationYears)?improvement/safe(p.depreciationYears):0;
  const debt=mortgageSchedule(safe(p.loanAmount),safe(p.interestRate),safe(p.amortMonths),safe(p.months));
  const rows=[];let rent=safe(p.monthlyRent), utilPrev=0,other2Prev=0, appreciationAccum=0;
  for(let m=1;m<=safe(p.months);m++){
    if(m>1){const intv=intervalMonths[p.rentInterval]||0;if(intv && m%intv===1)rent*=1+safe(p.rentIncrease);}
    const vacancy=rent*safe(p.vacancy), gross=rent-vacancy;
    const prop=annualExpense(m,p.propertyTaxStart,p.propertyTax,p.propertyTaxIncrease,false,0);
    const ins=annualExpense(m,p.insuranceStart,p.insurance,p.insuranceIncrease,false,0);
    const util=annualExpense(m,p.utilitiesStart,p.utilities,p.utilitiesIncrease,true,utilPrev);utilPrev=util;
    const adv=annualExpense(m,p.advertisingStart,p.advertising,p.advertisingIncrease,false,0);
    const o1=annualExpense(m,p.other1Start,p.other1,p.other1Increase,false,0);
    const o2=annualExpense(m,p.other2Start,p.other2,p.other2Increase,true,other2Prev);other2Prev=o2;
    const mgmt=m>=safe(p.mgmtStart)?gross*safe(p.mgmtFee):0;
    const repairs=m>=safe(p.repairsStart)?gross*safe(p.repairs):0;
    const o3=(m>=safe(p.other3Start)&&((m-safe(p.other3Start))%12===0)&&m<=safe(p.other3Start)+120)?gross*safe(p.other3):0;
    const op=prop+ins+util+adv+o1+o2+mgmt+repairs+o3, noi=gross-op;
    appreciationAccum += total*safe(p.appreciationRate)/12;
    rows.push({month:m,date:addMonths(p.purchaseDate,m),rent,vacancy,gross,propertyTax:prop,insurance:ins,utilities:util,advertising:adv,other1:o1,other2:o2,mgmt,repairs,other3:o3,opEx:op,noi,...debt[m-1],depreciation:depAnnual/12,appreciation:appreciationAccum});
  }
  for(let i=0;i<rows.length;i++){
    const r=rows[i], future=rows.slice(i+1,i+13).reduce((s,x)=>s+x.noi,0);
    const appreciated=(total+r.appreciation)*(1-safe(p.saleCost));
    const capValue=safe(p.capRate)?future/safe(p.capRate)*(1-safe(p.saleCost)):0;
    r.terminalBeforeTax=safe(p.terminalOption)===1?appreciated:capValue;
    r.taxableIncome=r.noi-r.interest-r.depreciation;
    r.incomeTax=r.taxableIncome*safe(p.incomeTax);
    const accumDep=rows.slice(0,i+1).reduce((s,x)=>s+x.depreciation,0);
    r.capitalGain=r.terminalBeforeTax-(total-accumDep);
    r.capGainsTax=r.capitalGain*safe(p.capitalGainsTax);
    r.terminalAfterTax=r.terminalBeforeTax-r.capGainsTax;
    r.netGain=r.terminalAfterTax-total;
    r.cfbt=r.noi-r.payment;
    r.terminalCfbt=r.cfbt+r.terminalBeforeTax-r.balance;
    const bt=[-down,...rows.slice(0,i).map(x=>x.cfbt),r.terminalCfbt];
    r.irrMonthly=down>0?irr(bt):NaN;r.irrAnnual=Number.isFinite(r.irrMonthly)?(1+r.irrMonthly)**12-1:NaN;
    r.mirrMonthly=down>0?mirr(bt,safe(p.financeRate),safe(p.reinvestmentRate)):NaN;r.mirrAnnual=Number.isFinite(r.mirrMonthly)?(1+r.mirrMonthly)**12-1:NaN;
    r.cfat=r.noi-r.payment-r.incomeTax;
  }
  const sm=Math.max(1,Math.min(rows.length,Math.trunc(safe(p.selectMonth)||36)));
  const cfat=[-down,...rows.slice(0,sm-1).map(x=>x.cfat),rows[sm-1].cfat+rows[sm-1].terminalAfterTax-rows[sm-1].balance];
  const dates=[p.purchaseDate,...rows.slice(0,sm).map(x=>x.date)];
  const selected=rows[sm-1];
  const capScenarios=Array.from({length:7},(_,i)=>safe(p.capRate)+(i-3)*0.0025).map(rate=>{
    const f=rows.slice(sm,sm+12).reduce((s,x)=>s+x.noi,0);
    const terminal=selected.cfbt+(rate?f/rate*(1-safe(p.saleCost)):0)-selected.balance;
    const stream=[-down,...rows.slice(0,sm-1).map(x=>x.cfbt),terminal];
    const mr=irr(stream);return {rate,irrMonthly:mr,irrAnnual:Number.isFinite(mr)?(1+mr)**12-1:NaN};
  });
  const rateScenarios=Array.from({length:7},(_,i)=>safe(p.interestRate)+(i-3)*0.0025).map(rate=>{
    const ds=mortgageSchedule(safe(p.loanAmount),rate,safe(p.amortMonths),safe(p.months));
    const stream=[-down];
    for(let i=0;i<sm-1;i++)stream.push(rows[i].noi-ds[i].payment);
    const term=rows[sm-1].noi-ds[sm-1].payment+rows[sm-1].terminalBeforeTax-ds[sm-1].balance;stream.push(term);
    const mr=irr(stream);return {rate,irrMonthly:mr,irrAnnual:Number.isFinite(mr)?(1+mr)**12-1:NaN};
  });
  return {inputs:p,totalInitialCost:total,downPayment:down,improvementValue:improvement,landValue:total-improvement,annualDepreciation:depAnnual,rows,selectedMonth:sm,xirr:xirr(cfat,dates),cfat,dates,capScenarios,rateScenarios};
}

function mortgageAnnual(p){
  const r=safe(p.mortgageRate)/safe(p.paymentsPerYear), n=safe(p.mortgageTermYears)*safe(p.paymentsPerYear);
  const monthly=p.mortgageAmount>0?pmt(r,n,-safe(p.mortgageAmount)):0;
  const annual=monthly*safe(p.paymentsPerYear), out=[];let bal=safe(p.mortgageAmount);
  for(let y=1;y<=10;y++){
    let interest=0,principal=0;
    for(let k=0;k<safe(p.paymentsPerYear);k++){const int=bal*r;const pr=Math.min(bal,monthly-int);interest+=int;principal+=pr;bal=Math.max(0,bal-pr);}
    out.push({year:y,debtService:annual,interest,principal,balance:bal});
  }
  return {monthly,annual:round100(annual),years:out};
}
function proforma(p){
  const years=[];let pgr=round100((safe(p.nonResidentialSqFt)*safe(p.nonResidentialRentPerSf)+safe(p.unit2br)*safe(p.rent2br)*12+safe(p.unit1br)*safe(p.rent1br)*12+safe(p.unitStudio)*safe(p.rentStudio)*12)*(1+safe(p.rentGrowth[0])));
  let ex={salary:round100(safe(p.salary)*(1+safe(p.expenseGrowth))),utilities:round100(safe(p.utilities)*(1+safe(p.expenseGrowth))),insurance:round100(safe(p.insurance)*(1+safe(p.expenseGrowth))),supplies:round100(safe(p.supplies)*(1+safe(p.expenseGrowth))),advertising:round100(safe(p.advertising)*(1+safe(p.expenseGrowth))),maintenance:round100(safe(p.maintenance)*(1+safe(p.expenseGrowth))),propertyTaxes:round100(safe(p.propertyTaxes)*(1+safe(p.propertyTaxGrowth[0])))};
  for(let y=1;y<=10;y++){
    const active=y<=safe(p.holdYears);
    if(y>1){pgr=active?round100(pgr*(1+safe(p.rentGrowth[y-1]))):0;for(const k of ['salary','utilities','insurance','supplies','advertising','maintenance'])ex[k]=active?round100(ex[k]*(1+safe(p.expenseGrowth))):0;ex.propertyTaxes=active?round100(ex.propertyTaxes*(1+safe(p.propertyTaxGrowth[y-1]))):0;}
    if(!active){years.push({year:y,pgr:0,vacancy:0,collectable:0,otherIncome:0,egi:0,management:0,...Object.fromEntries(Object.keys(ex).map(k=>[k,0])),totalExpenses:0,noi:0,expenseRatio:0});continue;}
    const vac=round100(safe(p.vacancy[y-1])*pgr), collect=pgr-vac, other=round100(collect*safe(p.otherIncomePct)), egi=collect+other, management=round100(egi*safe(p.managementFee));
    const total=management+Object.values(ex).reduce((s,v)=>s+v,0), noi=egi-total;
    years.push({year:y,pgr,vacancy:vac,collectable:collect,otherIncome:other,egi,management,...ex,totalExpenses:total,noi,expenseRatio:egi?total/egi:0});
  }
  return years;
}
export function calcAnalysis(input={}){
  const p={...analysisDefaults,...input, rentGrowth:[...(input.rentGrowth||analysisDefaults.rentGrowth)], vacancy:[...(input.vacancy||analysisDefaults.vacancy)], propertyTaxGrowth:[...(input.propertyTaxGrowth||analysisDefaults.propertyTaxGrowth)]};
  const op=proforma(p), mort=mortgageAnnual(p), fullDep=round100(safe(p.depreciableBasis)/safe(p.recoveryYears)), partialDep=round100(fullDep*11.5/12);
  const years=op.map((o,i)=>{
    const active=o.year<=safe(p.holdYears), m=mort.years[i];
    const btcf=o.noi-round100(m.debtService);
    const dep=!active?0:(o.year===1||o.year===safe(p.holdYears)?partialDep:fullDep);
    const taxable=o.noi-round100(m.interest)-dep, taxes=round100(taxable*safe(p.marginalTaxRate)), atcf=btcf-taxes;
    return {...o,debtService:round100(m.debtService),interest:round100(m.interest),principal:round100(m.principal),mortgageBalance:m.balance,btcf,depreciation:dep,taxableIncome:taxable,incomeTaxes:taxes,atcf};
  });
  const hold=Math.max(1,Math.min(10,Math.trunc(safe(p.holdYears)||1))), hy=years[hold-1];
  const cumDep=years.reduce((s,y)=>s+y.depreciation,0), initialBasis=safe(p.purchasePrice)+safe(p.transactionCosts), adjustedBasis=initialBasis-cumDep+safe(p.sellingCosts);
  const gain=safe(p.sellingPrice)-adjustedBasis, recapture=cumDep, ltGain=gain-recapture, saleTax=round100(recapture*safe(p.recaptureTax))+round100(ltGain*safe(p.capitalGainsTax));
  const mortgageBalance=hy.mortgageBalance, netSales=safe(p.sellingPrice)-safe(p.sellingCosts), bter=netSales-round100(mortgageBalance), ater=bter-saleTax;
  const initialEquity=initialBasis-safe(p.mortgageAmount);
  const bt=[-initialEquity],at=[-initialEquity];
  for(let y=1;y<=10;y++){bt.push(years[y-1].btcf+(y===hold?bter:0));at.push(years[y-1].atcf+(y===hold?ater:0));}
  const beforeTaxIrr=irr(bt),afterTaxIrr=irr(at), npv=at.slice(1).reduce((s,v,i)=>s+v/((1+safe(p.discountRate))**(i+1)),0);
  const y1=years[0], purchase=safe(p.purchasePrice);
  const ratios={grm:y1.pgr?purchase/y1.pgr:NaN,gim:y1.egi?purchase/y1.egi:NaN,nim:y1.noi?purchase/y1.noi:NaN,operating:y1.egi?y1.totalExpenses/y1.egi:NaN,breakEven:y1.egi?(y1.totalExpenses+mort.annual)/y1.egi:NaN,dscr:mort.annual?y1.noi/mort.annual:NaN,ltv:purchase?safe(p.mortgageAmount)/purchase:NaN,capRate:purchase?y1.noi/purchase:NaN,beforeTaxEquityDividend:initialEquity?y1.btcf/initialEquity:NaN,afterTaxEquityDividend:initialEquity?y1.atcf/initialEquity:NaN,grmValue:y1.pgr*safe(p.grmInput),gimValue:y1.egi*safe(p.gimInput),nimValue:y1.noi*safe(p.nimInput),capValue:safe(p.capRateInput)?y1.noi/safe(p.capRateInput):NaN};
  const variedNoiYears=years.map(y=>({...y,noi:y.noi*(1+safe(p.noiVariation))}));
  const atNoi=[-initialEquity,...variedNoiYears.map((y,i)=>{const taxes=round100((y.noi-y.interest-y.depreciation)*safe(p.marginalTaxRate));const acf=(y.noi-y.debtService)-taxes;return acf+((i+1)===hold?ater:0)})];
  const npvNoi=atNoi.slice(1).reduce((s,v,i)=>s+v/((1+safe(p.discountRate))**(i+1)),0);
  const variedSell=safe(p.sellingPrice)*(1+safe(p.salePriceVariation)), variedCosts=safe(p.sellingCosts)*(variedSell/safe(p.sellingPrice)||1), variedGain=variedSell-(initialBasis-cumDep+variedCosts), variedTax=round100(cumDep*safe(p.recaptureTax))+round100((variedGain-cumDep)*safe(p.capitalGainsTax)), variedAter=(variedSell-variedCosts-round100(mortgageBalance))-variedTax;
  const atSale=[-initialEquity,...years.map((y,i)=>y.atcf+((i+1)===hold?variedAter:0))],npvSale=atSale.slice(1).reduce((s,v,i)=>s+v/((1+safe(p.discountRate))**(i+1)),0);
  let cumulative=-initialEquity,payback=NaN;for(let i=0;i<hold;i++){const prev=cumulative,cash=at[i+1];cumulative+=cash;if(cumulative>=0&&!Number.isFinite(payback)){payback=i+(cash?(-prev/cash):0);break;}}
  return {inputs:p,years,mortgage:mort,initialEquity,fullDepreciation:fullDep,partialDepreciation:partialDep,sale:{cumDep,adjustedBasis,gain,recapture,ltGain,saleTax,mortgageBalance,bter,ater},beforeTaxIrr,afterTaxIrr,npv,payback,ratios,risk:{noiVariation:safe(p.noiVariation),noiNpv:npvNoi,noiChange:npvNoi-npv,noiElasticity:npv?(npvNoi-npv)/npv:NaN,saleVariation:safe(p.salePriceVariation),saleNpv:npvSale,saleChange:npvSale-npv,saleElasticity:npv?(npvSale-npv)/npv:NaN,downsideNoi:npv-(npvNoi-npv),upsideNoi:npv+(npvNoi-npv),downsideSale:npv-(npvSale-npv),upsideSale:npv+(npvSale-npv)}};
}
