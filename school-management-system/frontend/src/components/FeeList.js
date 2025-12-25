import React, { useState, useEffect } from "react";
import FilterBar from "./FilterBar";

const FeeList = () => {
    const [fees, setFees] = useState([]);
    const [filteredFees, setFilteredFees] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedGrade, setSelectedGrade] = useState('All Grades');
    const [error, setError] = useState(null);

    // 1. Fetch data from the API
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

    // 2. Filter logic: This handles both the search bar and the grade dropdown
    useEffect(() => {
        let filtered = fees;

        if (searchQuery) {
            filtered = filtered.filter((fee) =>
                fee.studentName.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        if (selectedGrade !== 'All Grades' && selectedGrade !== '') {
            filtered = filtered.filter((fee) => fee.grade === selectedGrade);
        }

        setFilteredFees(filtered);
    }, [searchQuery, selectedGrade, fees]);

    // 3. Configuration for the shared FilterBar component
    const filtersConfig = [
        {
            label: 'Grade',
            value: selectedGrade,
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
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-slate-800">Fee Management</h1>
            </div>

            {/* Shared Filter Component */}
            <FilterBar 
                searchTerm={searchQuery}
                onSearchChange={setSearchQuery}
                filters={filtersConfig}
                onReset={handleReset}
            />

            {/* Table Section */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full border-collapse">
                    <thead>
                        <tr className="bg-slate-50">
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">Student Name</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">Grade</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">Fee Type</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">Amount</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">Due Date</th>
                            <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredFees.length > 0 ? (
                            filteredFees.map((fee, index) => (
                                <tr key={index} className="hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0">
                                    <td className="px-6 py-4 text-sm text-slate-700">{fee.studentName}</td>
                                    <td className="px-6 py-4 text-sm text-slate-600">{fee.grade}</td>
                                    <td className="px-6 py-4 text-sm text-slate-600">{fee.feeType}</td>
                                    <td className="px-6 py-4 text-sm font-medium text-slate-800">{fee.amount}</td>
                                    <td className="px-6 py-4 text-sm text-slate-600">{fee.dueDate}</td>
                                    <td className="px-6 py-4">
                                        <span
                                            className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                                                fee.status === 'Paid'
                                                    ? 'bg-green-100 text-green-700'
                                                    : 'bg-red-100 text-red-700'
                                            }`}
                                        >
                                            {fee.status}
                                        </span>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="6" className="px-6 py-10 text-center text-slate-400">
                                    No fee records found matching your filters.
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