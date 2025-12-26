import React, { useState, useCallback, useEffect, useMemo, useRef } from 'react';
import { ResortLocation, Resort } from './types';
import { fetchResorts, geocodeLocation, wakeUpBackend } from './services/api';
import InputSection from './components/InputSection';
import ResortCard from './components/ResortCard';
import FilterSortModal, { SortType, Filters } from './components/FilterSortModal';
import { Snowflake, Loader2, ArrowDown, SlidersHorizontal } from 'lucide-react';

const App: React.FC = () => {
  // State
  const [userLocation, setUserLocation] = useState<ResortLocation | null>(null);
  const [locationInput, setLocationInput] = useState<string>('');
  const [isUsingGPS, setIsUsingGPS] = useState<boolean>(false);
  const [locationStatus, setLocationStatus] = useState<'idle' | 'locating' | 'success' | 'error'>('idle');
  
  // Sort & Filter State
  const [sortType, setSortType] = useState<SortType>('proximity');
  const [filters, setFilters] = useState<Filters>({
    goodWeather: false,
    freshSnow: false,
    liftsOpen: false,
    minPistes: false,
  });
  const [showFilterModal, setShowFilterModal] = useState(false);
  
  // Initialize date to today
  const getToday = () => {
    const d = new Date();
    return d.toISOString().split('T')[0];
  };
  const [date, setDate] = useState<string>(getToday());

  const [resorts, setResorts] = useState<Resort[]>([]);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [searchPerformed, setSearchPerformed] = useState<boolean>(false);
  const [totalResorts, setTotalResorts] = useState<number>(0);
  const [shouldScrollToResults, setShouldScrollToResults] = useState<boolean>(false);

  // Observer reference for infinite scroll
  const observer = useRef<IntersectionObserver | null>(null);

  // Ref for results section
  const resultsRef = useRef<HTMLDivElement>(null);

  // Wake up backend on mount
  useEffect(() => {
    wakeUpBackend();
  }, []);

  // Scroll to results when new search completes
  useEffect(() => {
    if (shouldScrollToResults && resorts.length > 0 && resultsRef.current) {
      // Small delay to ensure content is rendered
      setTimeout(() => {
        const element = resultsRef.current;
        if (element) {
          const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
          const offsetPosition = elementPosition - 80; // 80px gap from top

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });

          // Reset the flag after scrolling
          setShouldScrollToResults(false);
        }
      }, 100);
    }
  }, [shouldScrollToResults, resorts.length]);

  // Request Location (GPS)
  const handleRequestLocation = useCallback(() => {
    if (!navigator.geolocation) {
      setLocationStatus('error');
      setIsUsingGPS(false);
      return;
    }

    setLocationStatus('locating');
    setIsUsingGPS(true);
    setLocationInput("Locating...");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
        setLocationStatus('success');
        setLocationInput("Current Location");
      },
      (error) => {
        console.error("Geolocation error:", error);
        setLocationStatus('error');
        setLocationInput("");
        setIsUsingGPS(false);
      }
    );
  }, []);

  // Handle manual location selection from dropdown
  const handleLocationSelect = (location: { lat: number; lng: number; name: string }) => {
    setUserLocation({ lat: location.lat, lng: location.lng });
    setIsUsingGPS(false);
    setLocationStatus('idle');
  };

  // Fetch Logic
  const loadResorts = async (isNewSearch: boolean) => {
    let targetLocation: ResortLocation | null = userLocation;
    
    setLoading(true);

    try {
      // Logic: If user didn't use GPS and didn't select from dropdown (userLocation might be null or stale)
      // but has typed text, we attempt to geocode the text input.
      if (!isUsingGPS && locationInput && locationInput !== "Current Location") {
         // Only geocode if userLocation is null OR if the input doesn't seem to match a "selected" state.
         // Simpler heuristic: If we have text and no GPS, try to use existing userLocation if available, 
         // otherwise geocode. But user might have typed a NEW address without clicking dropdown.
         // So we should strictly prefer geocoding if the flow allows, but since we have autocomplete,
         // we might assume userLocation is up to date IF they clicked.
         // SAFEGUARD: If userLocation is null, force geocode.
         if (!targetLocation) {
            const geocoded = await geocodeLocation(locationInput);
            if (geocoded) {
              targetLocation = geocoded;
              setUserLocation(geocoded); 
            } else {
               alert("Could not find location: " + locationInput);
               setLoading(false);
               return;
            }
         }
      }

      if (!targetLocation) {
         // Try one last time to geocode what's in the input if present
         if (locationInput && locationInput !== "Current Location" && !isUsingGPS) {
            const geocoded = await geocodeLocation(locationInput);
             if (geocoded) {
              targetLocation = geocoded;
              setUserLocation(geocoded); 
            } else {
              setLoading(false);
              return;
            }
         } else {
            setLoading(false);
            return;
         }
      }

      const pageToFetch = isNewSearch ? 1 : page + 1;
      const data = await fetchResorts(targetLocation.lat, targetLocation.lng, date, pageToFetch);
      
      setResorts(prev => isNewSearch ? data.resorts : [...prev, ...data.resorts]);
      setPage(pageToFetch);
      setHasMore(data.has_more);
      setTotalResorts(data.total_resorts);
      setSearchPerformed(true);
    } catch (error) {
      console.error("Error loading resorts", error);
      // In a real app, set an error state toast here
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    // If user typed something new and hit search without selecting from dropdown, we clear old userLocation to force re-geocode in loadResorts logic above
    // or we can rely on the logic inside loadResorts to handle it.
    // Ideally, we'd clear userLocation if the input text changed, but that adds complexity.
    // For now, loadResorts handles the fallback to geocode if needed.
    setShouldScrollToResults(true);
    loadResorts(true);
  };

  const handleLoadMore = () => {
    loadResorts(false);
  };

  // Ref for the second-to-last element to trigger infinite scroll
  const lastResortElementRef = useCallback((node: HTMLDivElement) => {
    if (loading) return;
    if (observer.current) observer.current.disconnect();
    
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        handleLoadMore();
      }
    });
    
    if (node) observer.current.observe(node);
  }, [loading, hasMore]); // We rely on the closure for handleLoadMore

  // Helper to check if weather is "good" (sunny or partly cloudy, no precipitation)
  const isGoodWeather = (resort: Resort): boolean => {
    const periods = [resort.weather.morning, resort.weather.midday, resort.weather.afternoon];
    return periods.every(p =>
      p.cloud_cover_percent <= 75 && p.snowfall_cm === 0 && p.precipitation_mm === 0
    );
  };

  // Helper to parse lifts string like "10/12" and check if >85% open
  const hasEnoughLiftsOpen = (resort: Resort): boolean => {
    if (!resort.snow_report?.lifts) return false;
    const match = resort.snow_report.lifts.match(/(\d+)\s*\/\s*(\d+)/);
    if (!match) return false;
    const [, open, total] = match;
    const ratio = parseInt(open) / parseInt(total);
    return ratio > 0.85;
  };

  // Helper to parse pistes string like "45 km" or "45km"
  const getPistesKm = (resort: Resort): number => {
    if (!resort.snow_report?.pistes_km) return 0;
    const match = resort.snow_report.pistes_km.match(/(\d+(?:\.\d+)?)/);
    return match ? parseFloat(match[1]) : 0;
  };

  const filteredAndSortedResorts = useMemo(() => {
    // Apply filters first
    let filtered = resorts.filter(resort => {
      if (filters.goodWeather && !isGoodWeather(resort)) return false;
      if (filters.freshSnow && resort.weather.snowfall_prev_24h_cm <= 0) return false;
      if (filters.liftsOpen && !hasEnoughLiftsOpen(resort)) return false;
      if (filters.minPistes && getPistesKm(resort) < 20) return false;
      return true;
    });

    // Then sort
    return filtered.sort((a, b) => {
      let valA: number, valB: number;

      switch (sortType) {
        case 'proximity':
          valA = a.distance_km ?? Infinity;
          valB = b.distance_km ?? Infinity;
          break;
        case 'driving':
          valA = a.duration_driving_minutes ?? Infinity;
          valB = b.duration_driving_minutes ?? Infinity;
          break;
        case 'transit':
          valA = a.duration_transit_minutes ?? Infinity;
          valB = b.duration_transit_minutes ?? Infinity;
          break;
        default:
          valA = Infinity;
          valB = Infinity;
      }
      return valA - valB;
    });
  }, [resorts, sortType, filters]);

  const activeFiltersCount = Object.values(filters).filter(Boolean).length;

  const getButtonLabel = () => {
    const sortLabel = sortType === 'proximity' ? 'proximity' : sortType === 'driving' ? 'driving time' : 'transit time';
    if (activeFiltersCount > 0) {
      return `${activeFiltersCount} filter${activeFiltersCount > 1 ? 's' : ''} · ${sortLabel}`;
    }
    return `Sorted by ${sortLabel}`;
  };

  return (
    <div className="min-h-screen pb-20 bg-slate-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-900 to-slate-900 text-white pt-20 pb-32 px-4 relative overflow-hidden">
        {/* Abstract background snow pattern */}
        <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
           <div className="absolute top-10 left-10"><Snowflake size={64} /></div>
           <div className="absolute bottom-20 right-20"><Snowflake size={128} /></div>
           <div className="absolute top-1/2 left-1/3"><Snowflake size={48} /></div>
        </div>

        <div className="container mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-3 bg-blue-800/50 backdrop-blur-sm px-4 py-2 rounded-full border border-blue-400/30 mb-6">
            <Snowflake className="w-5 h-5 text-blue-200" />
            <span className="text-sm font-medium text-blue-100">Find your perfect powder day</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-6 tracking-tight leading-tight">
            Slope Finder
          </h1>
          <p className="text-lg md:text-xl text-blue-100 max-w-2xl mx-auto font-light leading-relaxed">
            Enter your location and travel date to instantly compare driving distances, 
            real-time snow reports, and weather forecasts for top ski resorts.
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4">
        {/* Input Section */}
        <InputSection 
          date={date}
          setDate={setDate}
          locationInput={locationInput}
          setLocationInput={setLocationInput}
          isUsingGPS={isUsingGPS}
          setIsUsingGPS={setIsUsingGPS}
          locationStatus={locationStatus}
          requestLocation={handleRequestLocation}
          onSearch={handleSearch}
          isLoading={loading}
          onLocationSelect={handleLocationSelect}
        />

        {/* Results Section */}
        {searchPerformed && (
          <div ref={resultsRef} className="mt-12 max-w-5xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold text-slate-800">
                {activeFiltersCount > 0
                  ? `${filteredAndSortedResorts.length}/${totalResorts} Resorts`
                  : `${totalResorts} Resorts`}
              </h2>
              <button
                onClick={() => setShowFilterModal(true)}
                className={`group flex items-center gap-2 text-sm bg-white hover:bg-slate-50 px-3 py-1.5 rounded-full border shadow-sm transition-all hover:shadow-md active:scale-95 cursor-pointer min-w-[160px] justify-center ${
                  activeFiltersCount > 0
                    ? 'border-blue-300 text-blue-700'
                    : 'border-slate-200 text-slate-600'
                }`}
              >
                <SlidersHorizontal className={`w-3.5 h-3.5 transition-colors ${
                  activeFiltersCount > 0 ? 'text-blue-600' : 'group-hover:text-blue-600'
                }`} />
                <span className="group-hover:text-slate-800 transition-colors">
                  {getButtonLabel()}
                </span>
              </button>
            </div>

            <div className="space-y-8">
              {filteredAndSortedResorts.map((resort, index) => {
                if (filteredAndSortedResorts.length > 1 && index === filteredAndSortedResorts.length - 2) {
                  return (
                    <div key={resort.id} ref={lastResortElementRef}>
                      <ResortCard resort={resort} />
                    </div>
                  );
                }
                return <ResortCard key={resort.id} resort={resort} />;
              })}
            </div>

            {/* Loading / Load More */}
            <div className="mt-12 text-center">
              {loading ? (
                <div className="inline-flex items-center gap-3 px-6 py-3 bg-white rounded-full shadow-lg border border-slate-100">
                  <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                  <span className="text-slate-600 font-medium">Scouting mountains...</span>
                </div>
              ) : hasMore ? (
                <button 
                  onClick={handleLoadMore}
                  className="group inline-flex items-center gap-2 px-8 py-3 bg-white text-slate-700 hover:text-blue-600 rounded-full font-semibold shadow-md hover:shadow-lg border border-slate-200 transition-all"
                >
                  Load More Resorts
                  <ArrowDown className="w-4 h-4 group-hover:translate-y-1 transition-transform" />
                </button>
              ) : resorts.length > 0 ? (
                <p className="text-slate-400 text-sm">You've reached the end of the slopes.</p>
              ) : null}
            </div>
          </div>
        )}

        {/* Empty State / Initial Instructions */}
        {!searchPerformed && (
          <div className="mt-20 text-center text-slate-400">
            <div className="inline-block p-6 rounded-full bg-slate-100 mb-4">
              <Snowflake className="w-12 h-12 text-slate-300" />
            </div>
            <p className="max-w-md mx-auto text-lg">
              Enter a location or use GPS to find the best ski conditions.
            </p>
          </div>
        )}
      </div>

      {/* Filter & Sort Modal */}
      <FilterSortModal
        isOpen={showFilterModal}
        onClose={() => setShowFilterModal(false)}
        sortType={sortType}
        onSortChange={setSortType}
        filters={filters}
        onFiltersChange={setFilters}
      />
    </div>
  );
};

export default App;