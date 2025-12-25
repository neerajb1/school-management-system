import React, { useState, useEffect } from 'react';
import { Users, GraduationCap, DollarSign, Bell } from 'lucide-react';
import { getDashboardData, getExams } from '../services/dataService';
import NoticeBoard from './NoticeBoard';
import FilterBar from './FilterBar';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [exams, setExams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            setLoading(true);
            try {
                const dashboard = await getDashboardData();
                const examsData = await getExams();
                console.log('DEBUG DASHBOARD:', dashboard);
                console.log('DEBUG EXAMS:', examsData);
                setDashboardData(dashboard);
                setExams(examsData);
                setLoading(false);
            } catch (err) {
                console.error("Error fetching dashboard data or exams:", err);
                setError("Failed to load dashboard data.");
                setLoading(false);
            }
        };
        fetchDashboardData();
    }, []);

    if (loading) return <div className="p-8 text-center text-slate-500">Loading Dashboard...</div>;
    if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

    // Destructure data from the dashboardData object
    const { 
        summary = {}, 
        attendanceTrends = [], 
        monthlyStats = [] 
    } = dashboardData || {};

    return (
        <div className="p-6 bg-slate-50 min-h-screen">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-800">School Overview</h1>
                <p className="text-slate-500">Welcome back, here is what's happening today.</p>
            </div>

            {/* Filter Bar */}
            <div className="mb-8">
                <FilterBar onFilterChange={(filters) => console.log('FilterBar Filters:', filters)} />
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                <StatCard 
                    icon={<Users className="text-blue-600" />} 
                    label="Total Students" 
                    value={summary.totalStudents} 
                    bgColor="bg-blue-50" 
                />
                <StatCard 
                    icon={<GraduationCap className="text-purple-600" />} 
                    label="Active Students" 
                    value={summary.activeStudents} 
                    bgColor="bg-purple-50" 
                />
                <StatCard 
                    icon={<Bell className="text-green-600" />} 
                    label="New Admissions" 
                    value={summary.newAdmissions} 
                    bgColor="bg-green-50" 
                />
                <StatCard 
                    icon={<DollarSign className="text-orange-600" />} 
                    label="Avg Attendance" 
                    value={`${summary.avgAttendance}%`} 
                    bgColor="bg-orange-50" 
                />
            </div>

            {/* Attendance Trends */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 mb-8">
                <h2 className="text-lg font-bold text-slate-800 mb-4">Attendance Trends</h2>
                <div className="space-y-4">
                    {attendanceTrends.map((trend, index) => (
                        <div key={index}>
                            <div className="flex justify-between text-sm mb-1">
                                <span className="text-slate-600 font-medium">{trend.label}</span>
                                <span className="text-slate-800 font-bold">{trend.percentage}%</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                <div 
                                    className="bg-blue-500 h-full rounded-full" 
                                    style={{ width: `${trend.percentage}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Recent Exams */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 mb-8">
                <h2 className="text-lg font-bold text-slate-800 mb-4">Recent Exams</h2>
                <ul>
                    {exams.map((exam, index) => (
                        <li key={index} className="py-2 border-b">
                            <div className="flex justify-between">
                                <span className="font-bold">{exam.subject}</span>
                                <span className="text-sm text-slate-500">{exam.date}</span>
                            </div>
                            <div className="text-sm text-slate-600">
                                {exam.grade} - {exam.section} | {exam.time} | Room: {exam.room}
                            </div>
                        </li>
                    ))}
                    {exams.length === 0 && (
                        <p className="text-gray-500 text-center">No recent exams available.</p>
                    )}
                </ul>
            </div>

            {/* Notice Board */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <NoticeBoard />
            </div>
        </div>
    );
};

// Reusable Stat Card Component
const StatCard = ({ icon, label, value, bgColor }) => (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4">
        <div className={`p-3 rounded-lg ${bgColor}`}>
            {icon}
        </div>
        <div>
            <p className="text-sm text-slate-500 font-medium">{label}</p>
            <p className="text-2xl font-bold text-slate-800">{value || 0}</p>
        </div>
    </div>
);

export default Dashboard;