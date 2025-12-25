import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import StudentList from './components/StudentList';
import AttendanceManager from './components/AttendanceManager';
import StudentDetail from './components/StudentDetail';
import Sidebar from './components/Sidebar';
import Login from './components/Login';
import MarksEntry from './components/MarksEntry';
import ExamSchedule from './components/ExamSchedule'; 
import PerformanceAnalytics from './components/PerformanceAnalytics';
import TeacherList from './components/TeacherList';
import ErrorBoundary from './components/ErrorBoundary';

const App = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const admin = localStorage.getItem('loggedInAdmin');
        const student = localStorage.getItem('loggedInStudent');
        if (admin) setUser('Admin');
        else if (student) setUser('Student');
    }, []);

    const handleLogout = () => {
        localStorage.clear();
        setUser(null);
    };

    return (
        <div className="flex min-h-screen bg-slate-50">
            {user && (
                <div className="w-64 fixed inset-y-0 z-50">
                    <Sidebar onLogout={handleLogout} />
                </div>
            )}
            <div className={`flex-1 ${user ? 'ml-64' : ''}`}>
                <Router>
                    <ErrorBoundary>
                        <Routes>
                            <Route path="/login" element={<Login setUser={setUser} />} />
                            <Route path="/dashboard" element={<Dashboard />} />
                            <Route path="/students" element={<StudentList />} />
                            <Route path="/students/:studentId" element={<StudentDetail />} />
                            <Route path="/attendance" element={<AttendanceManager />} />
                            <Route path="/marks-entry" element={<MarksEntry />} />
                            <Route path="/exam-schedule" element={<ExamSchedule />} />
                            <Route path="/performance-analytics" element={<PerformanceAnalytics />} />
                            <Route path="/teachers" element={<TeacherList />} />
                            <Route path="/" element={<Navigate to="/dashboard" />} />
                        </Routes>
                    </ErrorBoundary>
                </Router>
            </div>
        </div>
    );
};

export default App;