import React, { useState, useEffect, useCallback } from 'react';
import FilterBar from './FilterBar';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const PerformanceAnalytics = () => {
    const [results, setResults] = useState([]);
    const [students, setStudents] = useState([]);
    const [filteredResults, setFilteredResults] = useState([]);
    const [gradeDistribution, setGradeDistribution] = useState({ A: 0, B: 0, C: 0, D: 0, F: 0 });
    const [averageScores, setAverageScores] = useState([]);
    const [topPerformers, setTopPerformers] = useState([]);
    
    // Set initial values to match the "Default" strings so Reset stays hidden
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedGrade, setSelectedGrade] = useState('All Grades');
    const [selectedSection, setSelectedSection] = useState('All Sections');
    
    const [error, setError] = useState(null);

    // Fetch Data
    useEffect(() => {
        const fetchData = async () => {
            try {
                const [resRes, studRes] = await Promise.all([
                    fetch("/api/results.json"),
                    fetch("/api/students.json")
                ]);
                const resData = await resRes.json();
                const studData = await studRes.json();
                setResults(resData);
                setStudents(studData);
            } catch (err) {
                setError("Failed to load analytics data.");
            }
        };
        fetchData();
    }, []);

    // Filter and Calculation Logic
    useEffect(() => {
        let filtered = results.filter(item => {
            const matchesGrade = selectedGrade === 'All Grades' || item.grade === selectedGrade;
            const matchesSection = selectedSection === 'All Sections' || item.section === selectedSection;
            
            // Search by name logic
            const student = students.find(s => s.id === item.studentId);
            const matchesSearch = !searchQuery || (student && student.name.toLowerCase().includes(searchQuery.toLowerCase()));
            
            return matchesGrade && matchesSection && matchesSearch;
        });

        setFilteredResults(filtered);

        // Grade Distribution
        const dist = { A: 0, B: 0, C: 0, D: 0, F: 0 };
        filtered.forEach(r => {
            if (r.marks >= 90) dist.A++;
            else if (r.marks >= 80) dist.B++;
            else if (r.marks >= 70) dist.C++;
            else if (r.marks >= 60) dist.D++;
            else dist.F++;
        });
        setGradeDistribution(dist);

        // Top Performers
        const studentMap = {};
        filtered.forEach(r => {
            if (!studentMap[r.studentId]) studentMap[r.studentId] = { total: 0, count: 0 };
            studentMap[r.studentId].total += r.marks;
            studentMap[r.studentId].count++;
        });

        const performers = Object.keys(studentMap).map(id => {
            const student = students.find(s => s.id === parseInt(id));
            const avg = (studentMap[id].total / studentMap[id].count).toFixed(1);
            return { id, name: student ? student.name : `ID: ${id}`, average: parseFloat(avg) };
        }).sort((a, b) => b.average - a.average).slice(0, 5);

        setTopPerformers(performers);

        // Subject Averages
        const subjectMap = {};
        filtered.forEach(r => {
            if (!subjectMap[r.subject]) subjectMap[r.subject] = { total: 0, count: 0 };
            subjectMap[r.subject].total += r.marks;
            subjectMap[r.subject].count++;
        });

        const chartData = Object.keys(subjectMap).map(sub => ({
            subject: sub,
            average: parseFloat((subjectMap[sub].total / subjectMap[sub].count).toFixed(1))
        }));
        setAverageScores(chartData);

    }, [results, students, searchQuery, selectedGrade, selectedSection]);

    // Configuration for FilterBar
    const filtersConfig = [
        {
            label: 'Grade',
            value: selectedGrade,
            options: ['All Grades', 'Grade 10', 'Grade 11'],
            onChange: setSelectedGrade,
            defaultValue: 'All Grades'
        },
        {
            label: 'Section',
            value: selectedSection,
            options: ['All Sections', 'A', 'B'],
            onChange: setSelectedSection,
            defaultValue: 'All Sections'
        }
    ];

    const handleReset = () => {
        setSearchQuery('');
        setSelectedGrade('All Grades');
        setSelectedSection('All Sections');
    };

    if (error) return <div className="p-10 text-red-500">{error}</div>;

    return (
        <div className="p-6 bg-slate-50 min-h-screen">
            <h1 className="text-2xl font-bold mb-6 text-slate-800">Performance Analytics</h1>

            <FilterBar 
                searchTerm={searchQuery}
                onSearchChange={setSearchQuery}
                filters={filtersConfig}
                onReset={handleReset}
            />

            {/* Summary Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-5 gap-4 mb-8">
                {Object.entries(gradeDistribution).map(([grade, count]) => (
                    <div key={grade} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 text-center">
                        <div className="text-3xl font-bold text-indigo-600 mb-1">{grade}</div>
                        <div className="text-xs text-slate-400 uppercase font-bold tracking-widest">{count} Students</div>
                    </div>
                ))}
            </div>

            {/* Chart Area */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-8" style={{ height: '400px' }}>
                <h3 className="text-lg font-bold mb-6 text-slate-800">Subject Performance</h3>
                <ResponsiveContainer width="100%" height="90%">
                    <BarChart data={averageScores} margin={{ bottom: 20 }}>
                        <XAxis dataKey="subject" axisLine={false} tickLine={false} />
                        <YAxis axisLine={false} tickLine={false} domain={[0, 100]} />
                        <Tooltip cursor={{fill: '#f8fafc'}} />
                        <Bar dataKey="average" radius={[6, 6, 0, 0]} barSize={50}>
                            {averageScores.map((entry, index) => (
                                <Cell 
                                    key={`cell-${index}`} 
                                    // RESTORE COLORS: Green for high scores, Red for low scores
                                    fill={entry.average > 80 ? '#22c55e' : entry.average > 60 ? '#facc15' : '#ef4444'} 
                                />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Table */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b border-slate-100">
                        <tr>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Rank</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Student Name</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Avg Marks</th>
                        </tr>
                    </thead>
                    <tbody>
                        {topPerformers.map((p, i) => (
                            <tr key={p.id} className="border-b last:border-0 hover:bg-slate-50 transition-colors">
                                <td className="px-6 py-4 font-bold text-slate-300"># {i + 1}</td>
                                <td className="px-6 py-4 font-medium text-slate-700">{p.name}</td>
                                <td className="px-6 py-4 text-indigo-600 font-bold">{p.average}%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PerformanceAnalytics;