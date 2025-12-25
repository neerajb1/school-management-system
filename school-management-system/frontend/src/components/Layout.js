import React from 'react';
import { useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import { User } from 'lucide-react';

const Layout = ({ children }) => {
    const location = useLocation();

    // Map routes to page titles
    const pageTitles = {
        '/dashboard': 'Dashboard',
        '/students': 'Student Directory',
    };

    const pageTitle = pageTitles[location.pathname] || 'School Management System';

    return (
        <div className="flex">
            {/* Sidebar */}
            <Sidebar />

            {/* Main Content */}
            <div className="flex-1 bg-slate-50 min-h-screen">
                {/* Top Bar */}
                <div className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
                    <h1 className="text-xl font-bold text-gray-800">{pageTitle}</h1>
                    <div className="flex items-center space-x-4">
                        <User className="text-gray-500" size={24} />
                    </div>
                </div>

                {/* Page Content */}
                <div className="p-6">{children}</div>
            </div>
        </div>
    );
};

export default Layout;
