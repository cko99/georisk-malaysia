"use strict";

const API = "/api";
const state = { selected: null, marker: null, layers: {}, active: new Set(["administrative","roads","rivers","weather","hazards"]), mapReady: false };
const layerStyle = {
  administrative:{label:"Administrative",color:"#b9c8c6",kind:"line"}, roads:{label:"Major roads",color:"#f0b35b",kind:"line"},
  rivers:{label:"Rivers",color:"#48a9e6",kind:"line"}, weather:{label:"Weather",color:"#24d2c1",kind:"point"}, hazards:{label:"Hazards",color:"#f36c6c",kind:"point"}
};
const el = id => document.getElementById(id);
const safeText = value => value == null || value === "" ? "—" : String(value);

lucide.createIcons({attrs:{"stroke-width":1.7}});

const basemapStyles={
  satellite:{version:8,sources:{imagery:{type:"raster",tiles:["/api/basemaps/imagery/{z}/{x}/{y}"],tileSize:256,attribution:"Tiles © Esri and imagery contributors"}},layers:[{id:"imagery",type:"raster",source:"imagery"}]},
  hybrid:{version:8,sources:{imagery:{type:"raster",tiles:["/api/basemaps/imagery/{z}/{x}/{y}"],tileSize:256,attribution:"Tiles © Esri and imagery contributors"},transport:{type:"raster",tiles:["/api/basemaps/transport/{z}/{x}/{y}"],tileSize:256},places:{type:"raster",tiles:["/api/basemaps/places/{z}/{x}/{y}"],tileSize:256}},layers:[{id:"imagery",type:"raster",source:"imagery"},{id:"transport",type:"raster",source:"transport"},{id:"places",type:"raster",source:"places"}]},
  osm:{version:8,sources:{osm:{type:"raster",tiles:["/api/basemaps/osm/{z}/{x}/{y}"],tileSize:256,attribution:"© OpenStreetMap contributors"}},layers:[{id:"osm",type:"raster",source:"osm",paint:{"raster-saturation":-.25,"raster-brightness-max":.86}}]}
};
const map = new maplibregl.Map({container:"map",style:basemapStyles.satellite,center:[109.5,4.2],zoom:4.15,minZoom:3.6,maxZoom:16,maxBounds:[[98,-1],[121,9]],attributionControl:false});
map.on("styleimagemissing",event=>{if(!map.hasImage(event.id))map.addImage(event.id,{width:1,height:1,data:new Uint8Array([0,0,0,0])});});
map.addControl(new maplibregl.AttributionControl({compact:true,customAttribution:'Map data © <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap contributors</a>'}));
map.addControl(new maplibregl.NavigationControl({visualizePitch:true}),"top-right");
map.addControl(new maplibregl.FullscreenControl(),"top-right");
map.addControl(new maplibregl.ScaleControl({unit:"metric"}),"bottom-right");

async function fetchJSON(url, options){
  const response = await fetch(url, options);
  if(!response.ok) throw new Error(`Request failed (${response.status})`);
  return response.json();
}

async function loadLayerData(){
  const names=["administrative","roads","rivers","hazards"];
  const results=await Promise.all(names.map(async name=>[name,await fetchJSON(`${API}/layers/${name}`)]));
  results.forEach(([name,data])=>state.layers[name]=data);
}

function addOperationalLayers(){
  const definitions=[
    ["administrative",{type:"line",paint:{"line-color":"#b9c8c6","line-width":1.4,"line-dasharray":[3,2],"line-opacity":.8}}],
    ["roads",{type:"line",paint:{"line-color":"#f0b35b","line-width":["interpolate",["linear"],["zoom"],4,1.2,10,3],"line-opacity":.9}}],
    ["rivers",{type:"line",paint:{"line-color":"#48a9e6","line-width":["interpolate",["linear"],["zoom"],4,1.5,10,4],"line-opacity":.88}}],
    ["hazards",{type:"circle",paint:{"circle-radius":["interpolate",["linear"],["zoom"],4,5,10,9],"circle-color":["match",["get","severity"],"high","#f36c6c","moderate","#f0b35b","#24d2c1"],"circle-stroke-color":"#071013","circle-stroke-width":1.5}}]
  ];
  if(!map.getSource("administrative")) map.addSource("administrative",{type:"geojson",data:state.layers.administrative});
  if(!map.getLayer("administrative-fill")) map.addLayer({id:"administrative-fill",source:"administrative",type:"fill",layout:{visibility:state.active.has("administrative")?"visible":"none"},paint:{"fill-color":"#17343a","fill-opacity":.12}});
  definitions.forEach(([name,layer])=>{
    if(!map.getSource(name)) map.addSource(name,{type:"geojson",data:state.layers[name]});
    if(!map.getLayer(name)) map.addLayer({id:name,source:name,layout:{visibility:state.active.has(name)?"visible":"none"},...layer});
  });
  if(!map.getSource("weather")) map.addSource("weather",{type:"geojson",data:{type:"FeatureCollection",features:[]}});
  if(!map.getLayer("weather")) map.addLayer({id:"weather",source:"weather",type:"circle",layout:{visibility:state.active.has("weather")?"visible":"none"},paint:{"circle-radius":10,"circle-color":"#24d2c1","circle-stroke-color":"#d9fffb","circle-stroke-width":3,"circle-opacity":.85}});
  if(!map.getSource("analysis-results")) map.addSource("analysis-results",{type:"geojson",data:{type:"FeatureCollection",features:[]}});
  if(!map.getLayer("analysis-results")) map.addLayer({id:"analysis-results",source:"analysis-results",type:"circle",paint:{"circle-radius":12,"circle-color":"#ffffff","circle-opacity":.18,"circle-stroke-color":"#24d2c1","circle-stroke-width":3}});
  state.mapReady=true; renderLegend(); el("map-loading").hidden=true;
}

map.on("load",async()=>{try{if(!state.layers.hazards)await loadLayerData();addOperationalLayers();renderHazardChart();}catch(error){el("map-loading").textContent="Spatial fallback could not be loaded.";}});
map.on("style.load",()=>{if(state.layers.hazards)addOperationalLayers();});
map.on("mousemove",event=>{el("cursor-coordinates").textContent=`Lat ${event.lngLat.lat.toFixed(4)} · Lon ${event.lngLat.lng.toFixed(4)}`;});
map.on("click","hazards",event=>{const p=event.features[0].properties;const content=document.createElement("div");const title=document.createElement("div");title.className="popup-title";title.textContent=safeText(p.hazard);const place=document.createElement("div");place.className="popup-row";place.textContent=`${safeText(p.state)} · ${safeText(p.severity)}`;const note=document.createElement("div");note.className="popup-row";note.textContent="Synthetic portfolio record";content.append(title,place,note);new maplibregl.Popup().setLngLat(event.lngLat).setDOMContent(content).addTo(map);});
map.on("mouseenter","hazards",()=>map.getCanvas().style.cursor="pointer"); map.on("mouseleave","hazards",()=>map.getCanvas().style.cursor="");

function renderLegend(){
  el("legend").replaceChildren(...[...state.active].map(name=>{const item=document.createElement("div");item.className="legend-item";const sw=document.createElement("span");sw.className=`legend-swatch ${layerStyle[name].kind}`;sw.style.background=layerStyle[name].color;item.append(sw,document.createTextNode(layerStyle[name].label));return item;}));
  el("layer-count").textContent=`${state.active.size} active`;el("kpi-layers").textContent=state.active.size;
}

document.querySelectorAll("[data-layer]").forEach(input=>input.addEventListener("change",event=>{const name=event.target.dataset.layer;event.target.checked?state.active.add(name):state.active.delete(name);const visibility=event.target.checked?"visible":"none";if(map.getLayer(name))map.setLayoutProperty(name,"visibility",visibility);if(name==="administrative"&&map.getLayer("administrative-fill"))map.setLayoutProperty("administrative-fill","visibility",visibility);renderLegend();}));
function changeBasemap(name){
  const next=basemapStyles[name];
  const baseIds=["places","transport","imagery","osm"];
  el("map-loading").hidden=false;el("map-loading").textContent="Changing basemap…";
  baseIds.forEach(id=>{if(map.getLayer(id))map.removeLayer(id);});
  baseIds.forEach(id=>{if(map.getSource(id))map.removeSource(id);});
  Object.entries(next.sources).forEach(([id,source])=>map.addSource(id,JSON.parse(JSON.stringify(source))));
  next.layers.forEach(layer=>map.addLayer(JSON.parse(JSON.stringify(layer)),map.getLayer("administrative-fill")?"administrative-fill":undefined));
  let finished=false;const finish=()=>{if(finished)return;finished=true;el("map-loading").hidden=true;};
  map.once("idle",finish);window.setTimeout(finish,8000);
}
el("basemap-select").addEventListener("change",event=>changeBasemap(event.target.value));

function parseCoordinates(value){const match=value.trim().match(/^(-?\d+(?:\.\d+)?)\s*[, ]\s*(-?\d+(?:\.\d+)?)$/);if(!match)return null;const lat=Number(match[1]),lon=Number(match[2]);return lat>=-1&&lat<=8&&lon>=99&&lon<=120?{lat,lon,label:`${lat.toFixed(5)}, ${lon.toFixed(5)}`} : null;}

el("search-form").addEventListener("submit",async event=>{
  event.preventDefault(); const value=el("search-input").value.trim(); if(!value)return;
  const coords=parseCoordinates(value); if(coords){selectLocation(coords);el("search-results").replaceChildren();return;}
  el("search-results").textContent="Searching…";
  try{const body=await fetchJSON(`${API}/locations/search?q=${encodeURIComponent(value)}&limit=5`);const features=body.data?.features||[];const buttons=features.map(feature=>{const b=document.createElement("button");b.type="button";b.className="search-result";b.textContent=feature.properties.display_name;b.addEventListener("click",()=>{const [lon,lat]=feature.geometry.coordinates;selectLocation({lat,lon,label:feature.properties.display_name});el("search-results").replaceChildren();});return b;});el("search-results").replaceChildren(...buttons);if(!buttons.length)el("search-results").textContent="No Malaysian place found.";}catch(error){el("search-results").textContent="Place search is temporarily unavailable.";}
});

function selectLocation(location){
  state.selected=location;if(state.marker)state.marker.remove();state.marker=new maplibregl.Marker({color:"#24d2c1"}).setLngLat([location.lon,location.lat]).addTo(map);map.flyTo({center:[location.lon,location.lat],zoom:10,essential:true});
  el("analysis-location").textContent=location.label;el("insight-title").textContent=location.label;el("insight-text").textContent="Location selected. Loading coordinate weather and ready for proximity analysis.";loadCurrentWeather(location);
}

async function loadCurrentWeather(location){
  el("source-meteo").textContent="Loading";
  try{const body=await fetchJSON(`${API}/weather/current?latitude=${location.lat}&longitude=${location.lon}`);const current=body.data?.current||{};const units=body.data?.current_units||{};el("kpi-rain").textContent=`${safeText(current.rain)} ${units.rain||"mm"}`;el("rain-note").textContent=current.time?`Observed ${current.time.replace("T"," ")}`:"Open-Meteo";el("weather-temp").textContent=`${safeText(current.temperature_2m)} ${units.temperature_2m||"°C"}`;el("weather-wind").textContent=`${safeText(current.wind_speed_10m)} ${units.wind_speed_10m||"km/h"}`;el("weather-code").textContent=safeText(current.weather_code);el("weather-time").textContent=safeText(current.time?.split("T")[1]);el("weather-strip").hidden=false;el("source-meteo").textContent="Live";if(map.getSource("weather"))map.getSource("weather").setData({type:"FeatureCollection",features:[{type:"Feature",properties:current,geometry:{type:"Point",coordinates:[location.lon,location.lat]}}]});}catch(error){el("kpi-rain").textContent="N/A";el("rain-note").textContent="Weather feed degraded";el("source-meteo").textContent="Degraded";}
}

async function loadSystem(){
  try{await fetchJSON(`${API}/health`);el("api-dot").className="status-dot ok";el("api-status").textContent="API operational";}catch(error){el("api-dot").className="status-dot bad";el("api-status").textContent="API unavailable";}
  try{const body=await fetchJSON(`${API}/weather/warning?limit=100`);const warnings=Array.isArray(body.data)?body.data:[];el("kpi-warnings").textContent=warnings.length;el("warnings-note").textContent=warnings.length?"Official records returned":"No active records";el("source-gov").textContent="Live";}catch(error){el("kpi-warnings").textContent="N/A";el("warnings-note").textContent="Feed degraded";el("source-gov").textContent="Degraded";}
  el("source-updated").textContent=new Intl.DateTimeFormat("en-MY",{dateStyle:"medium",timeStyle:"short"}).format(new Date());
}

function circleGeoJSON(lon,lat,radius){const coords=[];const earth=6371008.8;for(let i=0;i<=64;i++){const bearing=i/64*Math.PI*2;const dx=Math.cos(bearing)*radius,dy=Math.sin(bearing)*radius;coords.push([lon+dx/(earth*Math.cos(lat*Math.PI/180))*180/Math.PI,lat+dy/earth*180/Math.PI]);}return{type:"Feature",properties:{},geometry:{type:"Polygon",coordinates:[coords]}};}

el("analysis-form").addEventListener("submit",async event=>{
  event.preventDefault();if(!state.selected){el("result-summary").textContent="Select a place or coordinates first.";return;}
  const radius=Number(new FormData(event.currentTarget).get("radius"));const layer=el("analysis-layer").value;el("result-summary").textContent="Running bounded spatial query…";
  try{const body=await fetchJSON(`${API}/analysis/proximity`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({latitude:state.selected.lat,longitude:state.selected.lon,radius_m:radius,layer})});const result=body.data;el("result-count").textContent=result.count;el("kpi-hazards").textContent=layer==="hazards"?result.count:el("kpi-hazards").textContent;const nearest=result.nearest?.properties;el("result-nearest").textContent=nearest?`${nearest.name||nearest.hazard||nearest.id} · ${nearest.distance_m>=1000?(nearest.distance_m/1000).toFixed(1)+" km":Math.round(nearest.distance_m)+" m"}`:"None";el("result-summary").textContent=result.insight;el("insight-text").textContent=result.insight+(Number(el("kpi-rain").textContent.split(" ")[0])>5?" Current rainfall is elevated.":"");if(map.getSource("analysis-results"))map.getSource("analysis-results").setData(result.result_geojson);if(map.getSource("analysis-radius"))map.getSource("analysis-radius").setData(circleGeoJSON(state.selected.lon,state.selected.lat,radius));else{map.addSource("analysis-radius",{type:"geojson",data:circleGeoJSON(state.selected.lon,state.selected.lat,radius)});map.addLayer({id:"analysis-radius",source:"analysis-radius",type:"fill",paint:{"fill-color":"#24d2c1","fill-opacity":.07,"fill-outline-color":"#24d2c1"}},"analysis-results");}}catch(error){el("result-summary").textContent="Analysis is temporarily unavailable.";}
});

function renderHazardChart(){const counts={};state.layers.hazards.features.forEach(feature=>counts[feature.properties.state]=(counts[feature.properties.state]||0)+1);new Chart(el("hazard-chart"),{type:"bar",data:{labels:Object.keys(counts),datasets:[{data:Object.values(counts),backgroundColor:"rgba(36,210,193,.55)",borderColor:"#24d2c1",borderWidth:1,borderRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{afterLabel:()=>"Synthetic demo records"}}},scales:{x:{ticks:{color:"#8fa5a5",font:{size:9}},grid:{display:false}},y:{beginAtZero:true,ticks:{stepSize:1,color:"#8fa5a5"},grid:{color:"rgba(143,165,165,.12)"}}}}});}

const sidebar=el("sidebar"),analysis=el("analysis-panel"),scrim=el("scrim");
function syncScrim(){const show=sidebar.classList.contains("open")||analysis.classList.contains("open");scrim.hidden=!show;scrim.classList.toggle("show",show);}
el("open-sidebar").addEventListener("click",()=>{sidebar.classList.add("open");syncScrim();});el("close-sidebar").addEventListener("click",()=>{sidebar.classList.remove("open");syncScrim();});el("open-analysis").addEventListener("click",()=>{analysis.classList.add("open");syncScrim();});el("close-analysis").addEventListener("click",()=>{analysis.classList.remove("open");syncScrim();});scrim.addEventListener("click",()=>{sidebar.classList.remove("open");analysis.classList.remove("open");syncScrim();});

loadSystem();renderLegend();
