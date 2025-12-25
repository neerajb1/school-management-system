import React from "react";
import { Search } from "lucide-react";

const FilterBar = ({ searchTerm = '', onSearchChange, filters = [], onReset }) => {
    // 1. Safety Check: prevent 'some' error if filters is undefined
    const safeFilters = filters || [];
    
    // 2. Logic: Only show Reset if there's actually something to reset
    // It checks if search is typed OR if any dropdown is not at its default value
    const isResetVisible = searchTerm !== '' || safeFilters.some((f) => 
        f.value && f.value !== (f.defaultValue || 'All Grades' || 'All Sections' || '')
    );

    return (
        <div className="flex flex-wrap gap-4 items-center mb-6">
            {/* Search Input - only shows if onSearchChange is provided */}
            {onSearchChange && (
                <div className="relative">
                    <input
                        type="text"
                        placeholder="Search by name..."
                        className="w-full md:w-64 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                        value={searchTerm}
                        onChange={(e) => onSearchChange(e.target.value)}
                    />
                    <Search className="absolute top-2.5 right-3 text-slate-400" size={20} />
                </div>
            )}

            {/* Dynamic Dropdowns for Grade, Section, Subject, etc. */}
            {safeFilters.map((filter, index) => (
                <select
                    key={index}
                    value={filter.value}
                    onChange={(e) => filter.onChange(e.target.value)}
                    className="px-4 py-2 border border-slate-300 rounded-lg bg-white focus:ring-2 focus:ring-indigo-500 outline-none cursor-pointer text-slate-700"
                >
                    {/* Map through options like ['All Grades', 'Grade 9', etc.] */}
                    {(filter.options || []).map((option) => (
                        <option key={option} value={option}>{option}</option>
                    ))}
                </select>
            ))}

            {/* Conditional Reset Button */}
            {isResetVisible && onReset && (
                <button 
                    onClick={onReset} 
                    className="text-sm text-indigo-600 hover:text-indigo-800 font-semibold ml-2 transition-colors"
                >
                    Reset Filters
                </button>
            )}
        </div>
    );
};

export default FilterBar;