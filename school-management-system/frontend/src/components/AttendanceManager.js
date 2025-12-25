import React, { useState, useEffect } from 'react';
import FilterBar from './FilterBar';
import { Calendar, Users, GraduationCap, CheckCircle, XCircle, Clock, Save, Search } from "lucide-react";

const AttendanceManager = () => {
    const [attendanceData, setAttendanceData] = useState([]);
    const [filteredRecords, setFilteredRecords] = useState([]);
    const [stats, setStats] = useState({ present: 0, absent: 0, late: 0 });
    const [loading, setLoading] = useState(true);

    // Filters State
    const [selectedDate, setSelectedDate] = useState("2025-12-20"); // Set to your data date to test
    const [selectedGrade, setSelectedGrade] = useState("Grade 10");
    const [selectedSection, setSelectedSection] = useState("A");

    useEffect(() => {
        const fetchAttendance = async () => {
            setLoading(true);
            try {
                const response = await fetch("/api/attendance.json");
                const data = await response.json();
                setAttendanceData(data);
                setLoading(false);
            } catch (err) {
                console.error("Error loading attendance:", err);
                setLoading(false);
            }
        };
        fetchAttendance();
    }, []);

    // CRITICAL: Logic to find and display data for the specific Date/Grade/Section
    useEffect(() => {
        if (attendanceData.length === 0) return;

        const recordFound = attendanceData.find(item => 
            item.date === selectedDate && 
            item.grade === selectedGrade && 
            item.section === selectedSection
        );

        if (recordFound) {
            setFilteredRecords(recordFound.records);
            setStats(recordFound.stats);
        } else {
            setFilteredRecords([]);
            setStats({ present: 0, absent: 0, late: 0 });
        }
    }, [selectedDate, selectedGrade, selectedSection, attendanceData]);

    const filtersConfig = [
        { 
            label: "Grade", 
            value: selectedGrade, 
            options: ["Grade 10", "Grade 11", "Grade 12"], 
            onChange: setSelectedGrade 
        },
        { 
            label: "Section", 
            value: selectedSection, 
            options: ["A", "B", "C"], 
            onChange: setSelectedSection 
        }
    ];

    if (loading) return <div className="p-10 text-center">Loading Attendance Data...</div>;

    return (
        <div className="p-6 bg-slate-50 min-h-screen">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-slate-800">Attendance Management</h1>
                <button className="flex items-center gap-2 bg-indigo-600 text-white px-6 py-2 rounded-xl font-bold shadow-lg shadow-indigo-200">
                    <Save size={18} /> Save Attendance
                </button>
            </div>

            {/* MAIN FILTER SECTION - Date moved up/prominent */}
            <div className="bg-white p-6 rounded-2xl shadow-sm mb-8 border border-slate-100">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                        <label className="block text-sm font-bold text-slate-500 uppercase mb-2 ml-1">Select Date</label>
                        <div className="relative">
                            <input 
                                type="date" 
                                value={selectedDate}
                                onChange={(e) => setSelectedDate(e.target.value)}
                                className="w-full border border-slate-200 p-3 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50"
                            />
                            <Calendar className="absolute right-4 top-3.5 text-slate-400 pointer-events-none" size={18} />
                        </div>
                    </div>
                    
                    <div>
                        <label className="block text-sm font-bold text-slate-500 uppercase mb-2 ml-1">Grade</label>
                        <select 
                            value={selectedGrade}
                            onChange={(e) => setSelectedGrade(e.target.value)}
                            className="w-full border border-slate-200 p-3 rounded-xl bg-slate-50 outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                            <option>Grade 10</option>
                            <option>Grade 11</option>
                            <option>Grade 12</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-bold text-slate-500 uppercase mb-2 ml-1">Section</label>
                        <select 
                            value={selectedSection}
                            onChange={(e) => setSelectedSection(e.target.value)}
                            className="w-full border border-slate-200 p-3 rounded-xl bg-slate-50 outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                            <option>A</option>
                            <option>B</option>
                            <option>C</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-2xl border-l-4 border-emerald-500 shadow-sm">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl"><CheckCircle /></div>
                        <div>
                            <p className="text-sm text-slate-500 font-medium">Present</p>
                            <h3 className="text-2xl font-bold text-slate-800">{stats.present}</h3>
                        </div>
                    </div>
                </div>
                <div className="bg-white p-6 rounded-2xl border-l-4 border-rose-500 shadow-sm">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-rose-50 text-rose-600 rounded-xl"><XCircle /></div>
                        <div>
                            <p className="text-sm text-slate-500 font-medium">Absent</p>
                            <h3 className="text-2xl font-bold text-slate-800">{stats.absent}</h3>
                        </div>
                    </div>
                </div>
                <div className="bg-white p-6 rounded-2xl border-l-4 border-amber-500 shadow-sm">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-amber-50 text-amber-600 rounded-xl"><Clock /></div>
                        <div>
                            <p className="text-sm text-slate-500 font-medium">Late</p>
                            <h3 className="text-2xl font-bold text-slate-800">{stats.late}</h3>
                        </div>
                    </div>
                </div>
            </div>

            {/* Student Table */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b border-slate-100">
                        <tr>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Student ID</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Name</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Status</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Remarks</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {filteredRecords.length > 0 ? (
                            filteredRecords.map((student) => (
                                <tr key={student.studentId} className="hover:bg-slate-50 transition-colors">
                                    <td className="px-6 py-4 text-sm font-medium text-slate-600">{student.studentId}</td>
                                    <td className="px-6 py-4 text-sm font-bold text-slate-800">{student.name}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                                            student.status === 'Present' ? 'bg-emerald-100 text-emerald-700' : 
                                            student.status === 'Absent' ? 'bg-rose-100 text-rose-700' : 
                                            'bg-amber-100 text-amber-700'
                                        }`}>
                                            {student.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-sm text-slate-500 italic">{student.remarks || '-'}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="4" className="px-6 py-20 text-center text-slate-400 italic">
                                    No attendance records found for this date and section.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AttendanceManager;