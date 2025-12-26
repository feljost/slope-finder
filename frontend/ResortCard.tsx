import React, { useState } from 'react';
import { Resort, WeatherPeriod } from '../types';
import WeatherIcon from './WeatherIcon';
import { Car, Clock, Mountain, Thermometer, Ruler, CableCar, ChevronDown, ChevronUp, Cloud, Snowflake, Train, ExternalLink, MapPin } from 'lucide-react';

interface ResortCardProps {
  resort: Resort;
}

const formatDuration = (minutes: number) => {
  if (minutes === undefined || minutes === null) return '--';
  const h = Math.floor(minutes / 60);
  const m = Math.round(minutes % 60);
  if (h === 0) return `${m} min`;
  return `${h}h ${m}m`;
};

const WeatherSlot: React.FC<{ label: string; data: WeatherPeriod }> = ({ label, data }) => (
  <div className="flex flex-col items-center justify-center p-3 rounded-lg bg-slate-50 border border-slate-100 min-w-[90px] text-center">
    <span className="text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">{label}</span>
    <WeatherIcon 
      snowfallCm={data.snowfall_cm} 
      rainMm={data.precipitation_mm} 
      cloudCover={data.cloud_cover_percent} 
      className="w-8 h-8 mb-2"
    />
    <div className="flex items-center justify-center gap-1 mb-1">
      <Thermometer className="w-3 h-3 text-slate-400" />
      <span className="text-sm font-bold text-slate-700">{data.temperature_celsius.toFixed(1)}°</span>
    </div>
    <div className="flex items-center justify-center gap-1">
      <Cloud className="w-3 h-3 text-slate-400" />
      <span className="text-sm font-bold text-slate-700">{data.cloud_cover_percent}%</span>
    </div>
  </div>
);

const ResortCard: React.FC<ResortCardProps> = ({ resort }) => {
  const { snow_report, weather } = resort;
  const [isMeteogramOpen, setIsMeteogramOpen] = useState(false);

  // Calculate General Day Weather
  const periods = [weather.morning, weather.midday, weather.afternoon];
  const avgTemp = periods.reduce((acc, curr) => acc + curr.temperature_celsius, 0) / periods.length;
  const avgCloudCover = Math.round(periods.reduce((acc, curr) => acc + curr.cloud_cover_percent, 0) / periods.length);
  // Use midday icon as representative
  const representativePeriod = weather.midday;

  return (
    <div className="bg-white rounded-2xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden border border-slate-200 relative">
      
      {/* Fresh Snow Badge */}
      {weather.snowfall_prev_24h_cm > 0 && (
        <div className="absolute top-4 right-4 z-10 bg-cyan-500 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-lg flex items-center gap-1.5 border border-cyan-400/50 animate-in fade-in zoom-in duration-300">
          <Snowflake className="w-3.5 h-3.5 fill-current" />
          {weather.snowfall_prev_24h_cm}cm Fresh (24h)
        </div>
      )}

      <div className="relative h-48 overflow-hidden">
        <img
          src={`/assets/resort_images/${resort.id.toLowerCase()}.jpg`}
          alt={resort.name} 
          className="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 to-transparent"></div>
        <div className="absolute bottom-4 left-4 text-white">
          <h2 className="text-2xl font-bold tracking-tight mb-1">{resort.name}</h2>
          <div className="flex flex-col gap-1">
             <div className="flex items-center gap-2 text-sm font-medium text-slate-200">
                <Mountain className="w-4 h-4 text-slate-300" />
                <span>{resort.elevation}</span>
             </div>
             <div className="flex items-center gap-2 text-sm font-medium text-slate-200">
                <MapPin className="w-4 h-4 text-slate-300" />
                <span>{resort.distance_km.toFixed(0)} km away</span>
             </div>
          </div>
        </div>
      </div>

      <div className="p-5">
        {/* Travel Info */}
        <div className="flex flex-wrap gap-3 mb-6 pb-6 border-b border-slate-100">
          {/* Driving Time */}
          {resort.maps_directions_url_driving ? (
            <a 
              href={resort.maps_directions_url_driving}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-2 text-blue-700 bg-blue-50 hover:bg-blue-100 hover:shadow-sm px-3 py-1.5 rounded-full text-sm font-medium transition-all"
              title="View Driving Directions on Google Maps"
            >
              <Car className="w-4 h-4 text-blue-500 group-hover:text-blue-600 transition-colors" />
              <span>{formatDuration(resort.duration_driving_minutes)}</span>
            </a>
          ) : (
            <div className="flex items-center gap-2 text-blue-700 bg-blue-50 px-3 py-1.5 rounded-full text-sm font-medium" title="Driving Duration">
              <Car className="w-4 h-4 text-blue-500" />
              <span>{formatDuration(resort.duration_driving_minutes)}</span>
            </div>
          )}

          {/* Public Transit Time */}
          {resort.maps_directions_url_transit ? (
            <a 
              href={resort.maps_directions_url_transit}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-2 text-emerald-700 bg-emerald-50 hover:bg-emerald-100 hover:shadow-sm px-3 py-1.5 rounded-full text-sm font-medium transition-all"
              title="View Transit Directions on Google Maps"
            >
              <Train className="w-4 h-4 text-emerald-600 group-hover:text-emerald-700 transition-colors" />
              <span>{formatDuration(resort.duration_transit_minutes)}</span>
            </a>
          ) : (
            <div className="flex items-center gap-2 text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-full text-sm font-medium" title="Public Transit Duration">
              <Train className="w-4 h-4 text-emerald-600" />
              <span>{formatDuration(resort.duration_transit_minutes)}</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Snow Report Section */}
          <div className="flex flex-col h-full">
            <h3 className="text-sm font-semibold text-slate-900 mb-3 flex items-center gap-2">
              Conditions
              {snow_report && <span className="text-[10px] font-normal text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">{snow_report.updated_on}</span>}
            </h3>
            
            {snow_report ? (
              <div className="grid grid-cols-2 gap-3 flex-1">
                <div className="p-3 bg-slate-50 rounded-lg flex flex-col justify-center">
                  <div className="flex items-center gap-2 text-slate-500 text-xs mb-1">
                    <Ruler className="w-3 h-3" /> Snow
                  </div>
                  <div className="font-semibold text-slate-800">{snow_report.snow_depth_cm}</div>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg flex flex-col justify-center">
                  <div className="flex items-center gap-2 text-slate-500 text-xs mb-1">
                    <CableCar className="w-3 h-3" /> Lifts
                  </div>
                  <div className="font-semibold text-slate-800">{snow_report.lifts}</div>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg col-span-2 flex flex-col justify-center">
                   <div className="flex items-center gap-2 text-slate-500 text-xs mb-1">
                    <Mountain className="w-3 h-3" /> Pistes
                  </div>
                  <div className="font-semibold text-slate-800">{snow_report.pistes_km}</div>
                </div>
              </div>
            ) : (
               <div className="flex-1 flex flex-col items-center justify-center p-4 bg-slate-50 rounded-lg border border-dashed border-slate-300">
                <span className="text-sm text-slate-500">Report unavailable</span>
              </div>
            )}
          </div>

          {/* Weather Forecast Section */}
          <div className="flex flex-col">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">Weather</h3>
            
            {/* General Summary Card */}
            <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg border border-slate-100 mb-3">
              <WeatherIcon 
                  snowfallCm={representativePeriod.snowfall_cm} 
                  rainMm={representativePeriod.precipitation_mm} 
                  cloudCover={avgCloudCover} 
                  className="w-10 h-10 shrink-0"
              />
              <div className="flex flex-wrap gap-x-6 gap-y-1">
                <div className="flex items-center gap-2">
                  <Thermometer className="w-5 h-5 text-slate-400" />
                  <span className="text-lg font-bold text-slate-800">{avgTemp.toFixed(1)}°C</span>
                </div>
                <div className="flex items-center gap-2">
                   <Cloud className="w-5 h-5 text-slate-400" />
                   <span className="text-lg font-bold text-slate-800">{avgCloudCover}%</span>
                </div>
              </div>
            </div>

            {/* Meteogram Dropdown */}
            <div className="">
              <button 
                onClick={() => setIsMeteogramOpen(!isMeteogramOpen)}
                className="w-full flex items-center justify-between px-3 py-2 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs font-semibold text-slate-700 transition-colors"
              >
                <span>Meteogram</span>
                {isMeteogramOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
              
              {isMeteogramOpen && (
                <div className="mt-2 grid grid-cols-3 gap-2 animate-in fade-in slide-in-from-top-2 duration-200">
                  <WeatherSlot label="Morning" data={resort.weather.morning} />
                  <WeatherSlot label="Midday" data={resort.weather.midday} />
                  <WeatherSlot label="Afternoon" data={resort.weather.afternoon} />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResortCard;