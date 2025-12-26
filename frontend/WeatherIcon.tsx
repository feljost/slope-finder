import React from 'react';
import { Cloud, CloudRain, CloudSnow, Sun, CloudSun } from 'lucide-react';

interface WeatherIconProps {
  snowfallCm: number;
  rainMm: number;
  cloudCover: number;
  className?: string;
}

const WeatherIcon: React.FC<WeatherIconProps> = ({ snowfallCm, rainMm, cloudCover, className = "w-6 h-6" }) => {
  if (snowfallCm > 0) {
    return <CloudSnow className={`${className} text-cyan-400`} />;
  }
  if (rainMm > 0) {
    return <CloudRain className={`${className} text-blue-400`} />;
  }
  if (cloudCover > 75) {
    return <Cloud className={`${className} text-slate-400`} />;
  }
  if (cloudCover > 25) {
    return <CloudSun className={`${className} text-orange-300`} />;
  }
  return <Sun className={`${className} text-yellow-400`} />;
};

export default WeatherIcon;