import React, { useState, useEffect } from "react";
// 1. Ensure this path is correct based on your folder structure
import FilterBar from "./FilterBar";

const TeacherList = () => {
    const [teachers, setTeachers] = useState([]);
    const [filteredTeachers, setFilteredTeachers] = useState([]);
    const [subjects, setSubjects] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState("All Subjects");
    const [searchQuery, setSearchQuery] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTeachers = async () => {
            setLoading(true);
            try {
                const response = await fetch("/api/teachers.json");
                const data = await response.json();
                setTeachers(data);
                setFilteredTeachers(data);
                setLoading(false);
            } catch (err) {
                console.error("Error fetching teachers:", err);
                setError("Failed to load teacher data.");
                setLoading(false);
            }
        };

        const loadSubjects = async () => {
            try {
                // If you don't have a subjects.json, you can hardcode them here
                const response = await fetch("/api/subjects.json");
                const data = await response.json();
                setSubjects(["All Subjects", ...data]);
            } catch (err) {
                // Fallback subjects if API fails
                setSubjects(["All Subjects", "Mathematics", "Science", "English", "History", "Physics"]);
            }
        };

        fetchTeachers();
        loadSubjects();
    }, []);

    // 2. Combined Filter Logic (Search + Subject)
    useEffect(() => {
        let filtered = teachers;

        if (searchQuery) {
            filtered = filtered.filter((t) =>
                t.name.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        if (selectedSubject !== "All Subjects") {
            filtered = filtered.filter((t) => t.subject === selectedSubject);
        }

        setFilteredTeachers(filtered);
    }, [searchQuery, selectedSubject, teachers]);

    const handleResetFilters = () => {
        setSearchQuery("");
        setSelectedSubject("All Subjects");
    };

    // 3. Configuration for the shared FilterBar
    const filtersConfig = [
        {
            label: "Subject",
            value: selectedSubject,
            options: subjects,
            onChange: setSelectedSubject,
            defaultValue: "All Subjects",
        },
    ];

    if (loading) return <div className="p-10 text-center">Loading Teachers...</div>;
    if (error) return <div className="p-10 text-center text-red-500">{error}</div>;

    return (
        <div className="p-6 bg-slate-50 min-h-screen">
            <h1 className="text-2xl font-bold text-slate-800 mb-6">Teacher Directory</h1>

            {/* 4. THE FILTER BAR */}
            <FilterBar 
                searchTerm={searchQuery}
                onSearchChange={setSearchQuery}
                filters={filtersConfig}
                onReset={handleResetFilters}
            />

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mt-4">
                <table className="w-full border-collapse">
                    <thead className="bg-slate-50">
                        <tr className="text-left text-xs font-bold text-slate-500 uppercase tracking-wider">
                            <th className="py-4 px-6 border-b">Name</th>
                            <th className="py-4 px-6 border-b">Subject</th>
                            <th className="py-4 px-6 border-b">Email</th>
                            <th className="py-4 px-6 border-b">Phone</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {filteredTeachers.length > 0 ? (
                            filteredTeachers.map((teacher, index) => (
                                <tr key={index} className="hover:bg-slate-50 transition-colors">
                                    <td className="py-4 px-6 text-sm font-medium text-slate-700">{teacher.name}</td>
                                    <td className="py-4 px-6 text-sm text-slate-600">
                                        <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs font-semibold">
                                            {teacher.subject}
                                        </span>
                                    </td>
                                    <td className="py-4 px-6 text-sm text-slate-600">{teacher.email}</td>
                                    <td className="py-4 px-6 text-sm text-slate-600">{teacher.phone}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="4" className="py-10 text-center text-slate-400">
                                    No teachers found matching your search.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TeacherList;