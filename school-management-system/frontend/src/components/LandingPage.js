import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50">
            <h1 className="text-3xl font-bold text-slate-800 mb-8">Welcome to the School System</h1>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <button
                    onClick={() => navigate('/login?role=admin')}
                    className="px-6 py-4 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition"
                >
                    Admin
                </button>
                <button
                    onClick={() => navigate('/login?role=teacher')}
                    className="px-6 py-4 bg-green-500 text-white rounded-lg shadow-md hover:bg-green-600 transition"
                >
                    Teacher
                </button>
                <button
                    onClick={() => navigate('/login?role=student')}
                    className="px-6 py-4 bg-indigo-500 text-white rounded-lg shadow-md hover:bg-indigo-600 transition"
                >
                    Student
                </button>
            </div>
        </div>
    );
};

export default LandingPage;
