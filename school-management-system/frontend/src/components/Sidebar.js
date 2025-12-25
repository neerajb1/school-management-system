import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Users, CheckCircle, LogOut, Calendar, BarChart2, IndianRupee } from 'lucide-react';

const Sidebar = ({ onLogout }) => {
    const [showLogoutModal, setShowLogoutModal] = useState(false);

    const handleLogout = () => {
        setShowLogoutModal(false); // Close the modal immediately
        if (typeof onLogout === 'function') {
            console.log('Calling onLogout...');
            onLogout(); // Trigger the logout logic passed from App.js
        } else {
            console.error('onLogout is not a function. Ensure it is passed as a prop from App.js.');
        }
    };

    const menuItems = [
        { name: 'Dashboard', path: '/dashboard', icon: <Home size={20} /> },
        { name: 'Students', path: '/students', icon: <Users size={20} /> },
        { name: 'Attendance', path: '/attendance', icon: <CheckCircle size={20} /> },
        { name: 'Marks Entry', path: '/marks-entry', icon: <CheckCircle size={20} /> },
        { name: 'Exam Schedule', path: '/exam-schedule', icon: <Calendar size={20} /> }, 
        { name: 'Performance Analytics', path: '/performance-analytics', icon: <BarChart2 size={20} /> },
        { name: 'Teachers', path: '/teachers', icon: <Users size={20} /> },
        { name: 'Fees', path: '/fees', icon: <IndianRupee size={20} /> }
    ];

    return (
        <div className="w-64 bg-slate-900 text-white h-screen p-6">
            <h1 className="text-2xl font-bold mb-8">School System</h1>
            <ul className="space-y-4">
                {menuItems.map((item) => (
                    <li key={item.name}>
                        <NavLink
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center space-x-3 px-4 py-2 rounded-lg transition ${
                                    isActive
                                        ? 'bg-blue-600 text-white'
                                        : 'hover:bg-slate-700 text-slate-300'
                                }`
                            }
                        >
                            <span>{item.icon}</span>
                            <span>{item.name}</span>
                        </NavLink>
                    </li>
                ))}
            </ul>
            <button
                onClick={() => setShowLogoutModal(true)}
                className="flex items-center space-x-3 px-4 py-2 mt-8 border border-red-500 text-red-500 rounded-lg hover:bg-red-500 hover:text-white transition"
            >
                <LogOut size={20} />
                <span>Logout</span>
            </button>

            {showLogoutModal && (
                <div className="fixed inset-0 bg-slate-900/50 z-[9998] flex items-center justify-center">
                    <div className="bg-white rounded-lg p-6 space-y-4 z-[9999] shadow-lg">
                        <h2 className="text-lg font-bold text-gray-800">Confirm Logout</h2>
                        <p className="text-sm text-gray-600">Are you sure you want to log out?</p>
                        <div className="flex justify-end space-x-4">
                            <button
                                onClick={() => setShowLogoutModal(false)}
                                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleLogout}
                                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Sidebar;
