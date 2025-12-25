import React, { useState, useEffect } from "react";
// 1. Ensure this path matches exactly where your FilterBar.js is located
import FilterBar from "./FilterBar";

const FeeList = () => {
    const [fees, setFees] = useState([]);
    const [filteredFees, setFilteredFees] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedGrade, setSelectedGrade] = useState('All Grades');
    const [error, setError] = useState(null);

    // Fetch Fees Data
    useEffect(() => {
        const fetchFees = async () => {
            try {
                const response = await fetch("/api/fees.json");
                if (!response.ok) throw new Error("Failed to load fees.");
                const data = await response.json();
                setFees(data);
                setFilteredFees(data);
            } catch (err) {
                console.error("Error fetching fees:", err);
                setError("Failed to load fee list.");
            }
        };
        fetchFees();
    }, []);

    // 2. Filter Logic (This makes the filters actually work)
    useEffect(() => {
        let filtered = fees;

        if (searchQuery) {
            filtered = filtered.filter((fee) =>
                fee.studentName.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        if (selectedGrade !== 'All Grades') {
            filtered = filtered.filter((fee) => fee.grade === selectedGrade);
        }

        setFilteredFees(filtered);
    }, [searchQuery, selectedGrade, fees]);

    // 3. This array defines WHAT filters appear in the FilterBar
    const filtersConfig = [
        {
            label: 'Grade',
            value: selectedGrade,
            // Customize these options to match your school's grades
            options: ['All Grades', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'],
            onChange: setSelectedGrade,
            defaultValue: 'All Grades'
        }
    ];

    const handleReset = () => {
        setSearchQuery('');
        setSelectedGrade('All Grades');
    };

    if (error) return <div className="p-6 text-red-500">{error}</div>;

    return (
        <div className="p-6 bg-slate-50 min-h-screen">
            <h1 className="text-2xl font-bold text-slate-800 mb-6">Fee Management</h1>

            {/* 4. THE FILTER BAR COMPONENT */}
            <FilterBar 
                searchTerm={searchQuery}
                onSearchChange={setSearchQuery}
                filters={filtersConfig}
                onReset={handleReset}
            />

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mt-4">
                <table className="w-full border-collapse">
                    <thead className="bg-slate-50">
                        <tr>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase text-slate-500 border-b">Student Name</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase text-slate-500 border-b">Grade</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase text-slate-500 border-b">Amount</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase text-slate-500 border-b">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredFees.length > 0 ? (
                            filteredFees.map((fee, index) => (
                                <tr key={index} className="hover:bg-slate-50 border-b border-slate-100 last:border-0">
                                    <td className="px-6 py-4 text-sm text-slate-700 font-medium">{fee.studentName}</td>
                                    <td className="px-6 py-4 text-sm text-slate-600">{fee.grade}</td>
                                    <td className="px-6 py-4 text-sm text-slate-800 font-bold">{fee.amount}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                                            fee.status === 'Paid' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                        }`}>
                                            {fee.status}
                                        </span>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="4" className="px-6 py-10 text-center text-slate-400">
                                    No records found matching your filters.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default FeeList;