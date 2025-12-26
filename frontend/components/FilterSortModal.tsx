import React from 'react';
import { X, ArrowUpDown, Filter, Sun, CloudSun, Snowflake, CableCar, Mountain } from 'lucide-react';

export type SortType = 'proximity' | 'driving' | 'transit';

export interface Filters {
  goodWeather: boolean;
  freshSnow: boolean;
  liftsOpen: boolean;
  minPistes: boolean;
}

interface FilterSortModalProps {
  isOpen: boolean;
  onClose: () => void;
  sortType: SortType;
  onSortChange: (sort: SortType) => void;
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
}

const FilterSortModal: React.FC<FilterSortModalProps> = ({
  isOpen,
  onClose,
  sortType,
  onSortChange,
  filters,
  onFiltersChange,
}) => {
  if (!isOpen) return null;

  const handleFilterToggle = (key: keyof Filters) => {
    onFiltersChange({ ...filters, [key]: !filters[key] });
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const sortOptions: { value: SortType; label: string; description: string }[] = [
    { value: 'proximity', label: 'Proximity', description: 'Distance' },
    { value: 'driving', label: 'Driving time', description: 'By car' },
    { value: 'transit', label: 'Transit time', description: 'Public transport' },
  ];

  const filterOptions: { key: keyof Filters; label: string; description: string; icon: React.ReactNode }[] = [
    {
      key: 'goodWeather',
      label: 'Good weather only',
      description: 'Sunny or partly cloudy',
      icon: <Sun className="w-5 h-5 text-yellow-500" />
    },
    {
      key: 'freshSnow',
      label: 'Fresh snow',
      description: 'New snowfall in past 24h',
      icon: <Snowflake className="w-5 h-5 text-cyan-400" />
    },
    {
      key: 'liftsOpen',
      label: '>85% lifts open',
      description: 'Most lifts operational',
      icon: <CableCar className="w-5 h-5 text-slate-600" />
    },
    {
      key: 'minPistes',
      label: 'More than 20km pistes',
      description: 'Plenty of runs available',
      icon: <Mountain className="w-5 h-5 text-blue-600" />
    },
  ];

  const activeFiltersCount = Object.values(filters).filter(Boolean).length;

  return (
    <div
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md max-h-[90vh] flex flex-col animate-in zoom-in-95 slide-in-from-bottom-4 duration-300">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-100 flex-shrink-0">
          <h2 className="text-xl font-bold text-slate-800">Sort & Filter</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-slate-500" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 space-y-6 overflow-y-auto flex-1 min-h-0">
          {/* Sort Section */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <ArrowUpDown className="w-4 h-4 text-slate-500" />
              <h3 className="font-semibold text-slate-700">Sort by</h3>
            </div>
            <div className="space-y-2">
              {sortOptions.map((option) => (
                <label
                  key={option.value}
                  className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all ${
                    sortType === option.value
                      ? 'bg-blue-50 border-2 border-blue-500'
                      : 'bg-slate-50 border-2 border-transparent hover:bg-slate-100'
                  }`}
                >
                  <input
                    type="radio"
                    name="sortType"
                    value={option.value}
                    checked={sortType === option.value}
                    onChange={() => onSortChange(option.value)}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                  />
                  <div>
                    <div className="font-medium text-slate-800">{option.label}</div>
                    <div className="text-xs text-slate-500">{option.description}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-slate-100" />

          {/* Filter Section */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Filter className="w-4 h-4 text-slate-500" />
              <h3 className="font-semibold text-slate-700">Filter</h3>
              {activeFiltersCount > 0 && (
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">
                  {activeFiltersCount} active
                </span>
              )}
            </div>
            <div className="space-y-2">
              {filterOptions.map((option) => (
                <label
                  key={option.key}
                  className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all ${
                    filters[option.key]
                      ? 'bg-blue-50 border-2 border-blue-500'
                      : 'bg-slate-50 border-2 border-transparent hover:bg-slate-100'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={filters[option.key]}
                    onChange={() => handleFilterToggle(option.key)}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <div className="flex-shrink-0">
                    {option.icon}
                  </div>
                  <div>
                    <div className="font-medium text-slate-800">{option.label}</div>
                    <div className="text-xs text-slate-500">{option.description}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-5 border-t border-slate-100 flex gap-3 flex-shrink-0">
          <button
            onClick={() => {
              onFiltersChange({ goodWeather: false, freshSnow: false, liftsOpen: false, minPistes: false });
            }}
            className="flex-1 px-4 py-2.5 text-slate-600 hover:text-slate-800 hover:bg-slate-100 rounded-xl font-medium transition-colors"
          >
            Clear filters
          </button>
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium transition-colors"
          >
            Apply
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilterSortModal;
