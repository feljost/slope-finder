import { ResortsResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const RESORTS_URL = `${API_BASE_URL}/resorts-info`;

export const wakeUpBackend = async () => {
  try {
    await fetch(`${API_BASE_URL}/health`);
  } catch (error) {
    console.debug('Backend wake-up ping sent');
  }
};

export const fetchResorts = async (
  lat: number,
  lng: number,
  date: string,
  page: number = 1,
  pageSize: number = 15
): Promise<ResortsResponse> => {
  const url = new URL(RESORTS_URL);
  url.searchParams.append('lat', lat.toString());
  url.searchParams.append('lng', lng.toString());
  url.searchParams.append('date', date);
  url.searchParams.append('page', page.toString());
  url.searchParams.append('page_size', pageSize.toString());

  try {
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    const data = await response.json();
    return data as ResortsResponse;
  } catch (error) {
    console.error("Failed to fetch resort data:", error);
    throw error;
  }
};

export const geocodeLocation = async (query: string): Promise<{ lat: number; lng: number } | null> => {
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`);
    const data = await response.json();
    if (data && data.length > 0) {
      return {
        lat: parseFloat(data[0].lat),
        lng: parseFloat(data[0].lon)
      };
    }
    return null;
  } catch (error) {
    console.error("Geocoding error:", error);
    return null;
  }
};

export const searchLocations = async (query: string): Promise<Array<{ display_name: string; lat: string; lon: string }>> => {
  try {
    if (query.length < 3) return [];
    
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&addressdetails=1&limit=5&featuretype=city`
    );
    
    if (!response.ok) return [];
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Location search error:", error);
    return [];
  }
};