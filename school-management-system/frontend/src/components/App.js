import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Import your custom components
import Dashboard from './Dashboard';
import StudentList from './StudentList';
import AttendanceManager from './AttendanceManager';
import StudentDetail from './StudentDetail';
import Sidebar from './Sidebar';
import MarksEntry from './MarksEntry';
import ExamSchedule from './ExamSchedule'; 
import PerformanceAnalytics from './PerformanceAnalytics';
import TeacherList from './TeacherList';
import FeeManagement from './FeeManagement';

const App = () => {
    return (
        <Router>
            <div className="flex min-h-screen bg-slate-50">
                {/* Sidebar - Fixed width */}
                <div className="w-64 fixed inset-y-0">
                    <Sidebar />
                </div>

                {/* Main Content - Offset by sidebar width */}
                <div className="flex-1 ml-64">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/dashboard" element={<Dashboard />} />
                        <Route path="/students" element={<StudentList />} />
                        <Route path="/students/:id" element={<StudentDetail />} />
                        <Route path="/attendance" element={<AttendanceManager />} />
                        <Route path="/marks-entry" element={<MarksEntry />} />
                        <Route path="/exam-schedule" element={<ExamSchedule />} />
                        <Route path="/performance-analytics" element={<PerformanceAnalytics />} />
                        <Route path="/teachers" element={<TeacherList />} />
                        <Route path="/fees" element={<FeeManagement />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

// CRITICAL: This line fixes the "export 'default' was not found" error
export default App;