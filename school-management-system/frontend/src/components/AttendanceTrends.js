import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Calendar, TrendingUp, TrendingDown } from 'lucide-react';

const AttendanceTrends = () => {
    const [grade, setGrade] = useState('Grade 10'); // Default grade
    const [attendanceData, setAttendanceData] = useState([]);
    const [processedData, setProcessedData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAttendance = async () => {
            setLoading(true);
            try {
                const data = await apiService.get('attendance'); // Fetch attendance.json
                setAttendanceData(data);
            } catch (err) {
                console.error('Error fetching attendance data:', err);
                setError('Failed to load attendance data.');
            } finally {
                setLoading(false);
            }
        };
        fetchAttendance();
    }, []);

    useEffect(() => {
        if (attendanceData.length > 0) {
            // Filter data for the selected grade
            const filteredData = attendanceData.filter((item) => item.grade === grade);

            // Group by date and calculate daily attendance percentage
            const groupedData = filteredData.reduce((acc, item) => {
                const total = item.records.length;
                const present = item.records.filter((record) => record.status === 'Present').length;
                const percentage = Math.round((present / total) * 100);

                acc.push({ date: item.date, percentage });
                return acc;
            }, []);

            setProcessedData(groupedData);
        }
    }, [attendanceData, grade]);

    // Calculate aggregate stats
    const averageAttendance =
        processedData.length > 0
            ? Math.round(processedData.reduce((sum, item) => sum + item.percentage, 0) / processedData.length)
            : 0;

    const bestDay = processedData.reduce((best, item) => (item.percentage > best.percentage ? item : best), {
        date: 'N/A',
        percentage: 0,
    });

    const worstDay = processedData.reduce((worst, item) => (item.percentage < worst.percentage ? item : worst), {
        date: 'N/A',
        percentage: 100,
    });

    return (
        <div className="min-h-screen bg-slate-50 p-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-slate-800">Monthly Attendance Trends</h1>
                <p className="text-slate-500">Analyze daily attendance percentages for the selected grade.</p>
            </div>

            {/* Grade Selector */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-8">
                <label className="flex items-center gap-2 text-sm font-semibold text-slate-600">
                    <Calendar size={16} /> Select Grade
                </label>
                <select
                    value={grade}
                    onChange={(e) => setGrade(e.target.value)}
                    className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                >
                    <option value="Grade 9">Grade 9</option>
                    <option value="Grade 10">Grade 10</option>
                    <option value="Grade 11">Grade 11</option>
                    <option value="Grade 12">Grade 12</option>
                </select>
            </div>

            {/* Aggregate Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                    <div>
                        <p className="text-slate-500 text-xs font-bold uppercase tracking-wider">Average Attendance</p>
                        <h3 className="text-2xl font-bold text-blue-600">{averageAttendance}%</h3>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-full text-blue-600">
                        <TrendingUp size={24} />
                    </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                    <div>
                        <p className="text-slate-500 text-xs font-bold uppercase tracking-wider">Best Attendance Day</p>
                        <h3 className="text-lg font-bold text-green-600">{bestDay.date}</h3>
                        <p className="text-sm text-slate-500">{bestDay.percentage}%</p>
                    </div>
                    <div className="bg-green-50 p-3 rounded-full text-green-600">
                        <TrendingUp size={24} />
                    </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                    <div>
                        <p className="text-slate-500 text-xs font-bold uppercase tracking-wider">Worst Attendance Day</p>
                        <h3 className="text-lg font-bold text-red-600">{worstDay.date}</h3>
                        <p className="text-sm text-slate-500">{worstDay.percentage}%</p>
                    </div>
                    <div className="bg-red-50 p-3 rounded-full text-red-600">
                        <TrendingDown size={24} />
                    </div>
                </div>
            </div>

            {/* Attendance Chart */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <h2 className="text-lg font-bold text-slate-800 mb-4">Daily Attendance Percentage</h2>
                {processedData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={processedData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="date" />
                            <YAxis domain={[0, 100]} />
                            <Tooltip />
                            <Line type="monotone" dataKey="percentage" stroke="#3b82f6" strokeWidth={2} />
                        </LineChart>
                    </ResponsiveContainer>
                ) : (
                    <div className="p-20 text-center text-slate-500">No data available for the selected grade.</div>
                )}
            </div>
        </div>
    );
};

export default AttendanceTrends;
