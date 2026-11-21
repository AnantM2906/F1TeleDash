const $ = id => document.getElementById(id);
const colors = ['#55d8f3','#be9bfb','#f7c36b','#83e7b3'];
let data = null; let plots = {};
function chart(id,type,labels,datasets,options={}){
  if(plots[id]) plots[id].destroy();
  plots[id] = new Chart($(id), {type,data:{labels,datasets},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#c9d5e8'}}},scales:{x:{ticks:{color:'#9ba9c2'},grid:{color:'#25314a'}},y:{ticks:{color:'#9ba9c2'},grid:{color:'#25314a'}}},...options}});
}
function lineData(rows,key,name,color){return {label:name,data:rows.map(r=>r[key]),borderColor:color,backgroundColor:color+'22',pointRadius:2,tension:.25,fill:true};}
function render(){
 const driver=$('driver').value; const rows=data.records.filter(r=>r.driver===driver);
 if(!rows.length) return;
 $('best').textContent=Math.min(...rows.map(r=>r.lap_time)).toFixed(3)+' s';
 $('speed').textContent=(rows.reduce((s,r)=>s+r.speed_kph,0)/rows.length).toFixed(1)+' km/h';
 $('wear').textContent=rows.at(-1).tire_wear_pct.toFixed(1)+'%';
 $('count').textContent=rows.length;
 const labels=rows.map(r=>`Lap ${r.lap}`);
 chart('speedChart','line',labels,[lineData(rows,'speed_kph','Top speed (km/h)',colors[0])]);
 chart('lapChart','line',labels,[lineData(rows,'lap_time','Lap time (s)',colors[1])]);
 chart('wearChart','line',labels,[lineData(rows,'tire_wear_pct','Tire wear (%)',colors[3])]);
 const datasets=['s1','s2','s3'].map((k,i)=>({label:`Sector ${i+1}`,data:rows.map(r=>r[k]),backgroundColor:colors[i],borderRadius:3}));
 chart('sectorChart','bar',labels,datasets);
 $('standings').replaceChildren(...data.standings.map((entry,i)=>{
   const tr=document.createElement('tr');
   [i+1,entry.driver,entry.team,entry.best_lap.toFixed(3)+' s',entry.total_time.toFixed(3)+' s'].forEach(v=>{const td=document.createElement('td');td.textContent=v;tr.appendChild(td);});
   return tr;
 }));
}
async function load(){
 $('status').textContent='Loading…';
 try{
   const laps=Number($('laps').value);
   if(!Number.isInteger(laps)||laps<1||laps>100) throw new Error('Laps must be between 1 and 100');
   const resp=await fetch(`/api/telemetry?laps=${laps}`);
   if(!resp.ok) throw new Error(`API returned ${resp.status}`);
   data=await resp.json();
   const previous=$('driver').value;
   $('driver').replaceChildren(...data.drivers.map(d=>{const o=document.createElement('option');o.value=d;o.textContent=d;return o;}));
   if(data.drivers.includes(previous)) $('driver').value=previous;
   render(); $('status').textContent='Synthetic session ready';
 }catch(e){$('status').textContent=`Error: ${e.message}`;}
}
$('refresh').addEventListener('click',load);$('driver').addEventListener('change',render);
window.addEventListener('DOMContentLoaded',load);
