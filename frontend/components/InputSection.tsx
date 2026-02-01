import React, { useState, useEffect, useRef, useMemo, forwardRef } from 'react';
import { Calendar, MapPin, Loader2, Search, LocateFixed, X } from 'lucide-react';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { searchLocations } from '../services/api';

// Custom "Shell" component - renders our Tailwind input but receives MUI's props
// We destructure MUI-specific props to prevent them from being spread onto the DOM
const TailwindDateInput = forwardRef<HTMLDivElement, any>(
  (props, ref) => {
    // Extract only what we need, ignore MUI-specific props
    const {
      value,
      onClick,
      InputProps,
      // Destructure and discard MUI-specific props that shouldn't go to DOM
      ownerState,
      fullWidth,
      error,
      inputProps,
      inputRef,
      slots,
      slotProps,
      ...other
    } = props;

    return (
      <div ref={ref} className="relative w-full">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none z-10">
          <Calendar className="h-5 w-5 text-slate-400" />
        </div>
        <input
          ref={inputRef}
          type="text"
          value={value || ''}
          onClick={onClick}
          onKeyDown={(e) => e.preventDefault()}
          readOnly
          className="block w-full h-12 pl-10 pr-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none transition-all cursor-pointer"
        />
      </div>
    );
  }
);

interface InputSectionProps {
  date: string;
  setDate: (date: string) => void;
  locationInput: string;
  setLocationInput: (val: string) => void;
  isUsingGPS: boolean;
  setIsUsingGPS: (val: boolean) => void;
  locationStatus: 'idle' | 'locating' | 'success' | 'error';
  requestLocation: () => void;
  onSearch: () => void;
  isLoading: boolean;
  onLocationSelect: (location: { lat: number; lng: number; name: string }) => void;
}

const InputSection: React.FC<InputSectionProps> = ({ 
  date, 
  setDate, 
  locationInput,
  setLocationInput,
  isUsingGPS,
  setIsUsingGPS,
  locationStatus,
  requestLocation,
  onSearch,
  isLoading,
  onLocationSelect
}) => {
  const [suggestions, setSuggestions] = useState<Array<{ display_name: string; lat: string; lon: string }>>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isSearchingLocation, setIsSearchingLocation] = useState(false);
  const [datePickerOpen, setDatePickerOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const datePickerRef = useRef<HTMLDivElement>(null);

  // Get today's date for min attribute and max date (10 days from now)
  const today = useMemo(() => {
    const d = new Date();
    d.setHours(0, 0, 0, 0);
    return d;
  }, []);

  const maxDate = useMemo(() => {
    const d = new Date();
    d.setDate(d.getDate() + 5);
    d.setHours(23, 59, 59, 999);
    return d;
  }, []);

  // Convert string date (YYYY-MM-DD) to Date object for the picker
  const selectedDate = useMemo(() => {
    if (!date) return today;
    const [y, m, d] = date.split('-').map(Number);
    // Create date treating input as local time components
    return new Date(y, m - 1, d);
  }, [date, today]);

  const handleDateChange = (date: Date | null) => {
    if (date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        setDate(`${year}-${month}-${day}`);
    }
  };

  useEffect(() => {
    // Debounce search
    const timer = setTimeout(async () => {
      if (locationInput.length > 2 && !isUsingGPS && locationInput !== "Current Location") {
        setIsSearchingLocation(true);
        const results = await searchLocations(locationInput);
        setSuggestions(results);
        setShowSuggestions(results.length > 0);
        setIsSearchingLocation(false);
      } else {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    }, 400);

    return () => clearTimeout(timer);
  }, [locationInput, isUsingGPS]);

  // Handle clicking outside to close suggestions
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocationInput(e.target.value);
    if (isUsingGPS) {
      setIsUsingGPS(false);
    }
  };

  const handleSuggestionClick = (place: { display_name: string; lat: string; lon: string }) => {
    const formattedName = place.display_name.split(',')[0]; // Keep it simple
    setLocationInput(formattedName);
    setShowSuggestions(false);
    onLocationSelect({
      lat: parseFloat(place.lat),
      lng: parseFloat(place.lon),
      name: formattedName
    });
  };

  const handleGPSClick = () => {
    setShowSuggestions(false);
    requestLocation();
  };
  
  const handleClear = () => {
      setLocationInput('');
      setIsUsingGPS(false);
      setShowSuggestions(false);
  };

  const canSearch = !isLoading && (
    (locationInput.trim().length > 2 && !isUsingGPS) || 
    (isUsingGPS && locationStatus === 'success')
  );

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6 md:p-8 -mt-20 relative z-10 border border-slate-100 max-w-4xl mx-auto">
      <div className="flex flex-col md:flex-row gap-4 items-end">
        
        {/* Location Input */}
        <div className="flex-1 w-full relative" ref={wrapperRef}>
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            Starting Location
          </label>
          <div className="relative">
             <input
              type="text"
              value={locationInput}
              onChange={handleInputChange}
              onFocus={() => { if(suggestions.length > 0) setShowSuggestions(true); }}
              placeholder="Enter City or Address"
              className="block w-full h-12 pl-10 pr-24 rounded-xl border bg-slate-50 border-slate-200 text-slate-900 focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none transition-all appearance-none"
            />
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MapPin className="h-5 w-5 text-slate-400" />
            </div>
            
            <div className="absolute inset-y-0 right-0 flex items-center">
              {locationInput && !isUsingGPS && (
                 <button onClick={handleClear} className="p-2 text-slate-400 hover:text-slate-600 mr-1">
                    <X className="w-4 h-4" />
                 </button>
              )}
              
              <button
                onClick={handleGPSClick}
                title="Use current location"
                className={`h-full px-3 flex items-center justify-center rounded-r-xl border-l transition-colors bg-slate-100 border-slate-200 text-slate-500 hover:bg-slate-200 hover:text-blue-600 ${
                   isUsingGPS && locationStatus === 'success' 
                   ? 'text-blue-600 bg-slate-200' 
                   : ''
                }`}
              >
                {locationStatus === 'locating' ? (
                  <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
                ) : (
                  <LocateFixed className={`w-5 h-5 ${isUsingGPS && locationStatus === 'success' ? 'text-blue-600' : ''}`} />
                )}
              </button>
            </div>
          </div>
          
          {/* Autocomplete Dropdown */}
          {showSuggestions && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-xl shadow-2xl border border-slate-100 overflow-hidden z-50 animate-in fade-in zoom-in-95 duration-200">
               <ul className="max-h-60 overflow-y-auto">
                 {suggestions.map((place, index) => (
                   <li key={index}>
                     <button
                        onClick={() => handleSuggestionClick(place)}
                        className="w-full text-left px-4 py-3 hover:bg-blue-50 transition-colors flex items-center gap-3 border-b border-slate-50 last:border-0"
                     >
                       <MapPin className="w-4 h-4 text-slate-400 shrink-0" />
                       <span className="text-sm text-slate-700 truncate">{place.display_name}</span>
                     </button>
                   </li>
                 ))}
               </ul>
            </div>
          )}
          {isSearchingLocation && !showSuggestions && locationInput.length > 2 && (
             <div className="absolute top-full left-0 mt-1 text-xs text-slate-400 pl-2">Searching...</div>
          )}
        </div>

        {/* Date Input */}
        <div className="flex-1 w-full">
           <label className="block text-sm font-semibold text-slate-700 mb-2">
            Travel Date
          </label>
          <div ref={datePickerRef}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                value={selectedDate}
                onChange={handleDateChange}
                minDate={today}
                maxDate={maxDate}
                format="EEE, MMM d, yyyy"
                enableAccessibleFieldDOMStructure={false}
                open={datePickerOpen}
                onOpen={() => setDatePickerOpen(true)}
                onClose={() => setDatePickerOpen(false)}
                slots={{
                  // The "Trojan Horse" - MUI uses our component instead of its TextField
                  textField: TailwindDateInput,
                }}
                slotProps={{
                  textField: {
                    onClick: () => setDatePickerOpen(true),
                  },
                  popper: {
                    sx: { zIndex: 1300 },
                    placement: 'bottom-start',
                    anchorEl: () => datePickerRef.current,
                  },
                }}
              />
            </LocalizationProvider>
          </div>
        </div>

        {/* Search Button */}
        <div className="w-full md:w-auto">
          <button
            onClick={onSearch}
            disabled={!canSearch}
            className={`h-12 w-full md:w-auto px-8 rounded-xl font-bold text-white flex items-center justify-center gap-2 transition-all shadow-lg ${
              canSearch 
                ? 'bg-blue-600 hover:bg-blue-700 hover:shadow-blue-200 hover:-translate-y-0.5' 
                : 'bg-slate-300 cursor-not-allowed shadow-none'
            }`}
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
            Find Slopes
          </button>
        </div>
      </div>
      {locationStatus === 'error' && isUsingGPS && (
        <p className="text-red-500 text-xs mt-2">
          Could not access location. Please enter manually.
        </p>
      )}
    </div>
  );
};

export default InputSection;