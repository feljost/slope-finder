export interface WeatherPeriod {
  time: string;
  temperature_celsius: number;
  precipitation_mm: number;
  snowfall_cm: number;
  cloud_cover_percent: number;
  visibility_m: number;
}

export interface WeatherData {
  snowfall_prev_24h_cm: number;
  morning: WeatherPeriod;
  midday: WeatherPeriod;
  afternoon: WeatherPeriod;
}

export interface SnowReport {
  pistes_km: string;
  lifts: string;
  snow_depth_cm: string;
  updated_on: string;
}

export interface ResortLocation {
  lat: number;
  lng: number;
}

export interface Resort {
  id: string;
  name: string;
  location: ResortLocation;
  elevation: string;
  snowreport_url: string;
  air_distance_km: number;
  distance_km: number;
  duration_driving_minutes: number;
  duration_transit_minutes: number;
  maps_directions_url_driving?: string;
  maps_directions_url_transit?: string;
  snow_report: SnowReport | null;
  weather: WeatherData;
  image_url: string;
}

export interface ResortsResponse {
  page: number;
  page_size: number;
  total_resorts: number;
  has_more: boolean;
  resorts: Resort[];
}

export interface SearchParams {
  lat: number;
  lng: number;
  date: string;
  page: number;
  pageSize: number;
}