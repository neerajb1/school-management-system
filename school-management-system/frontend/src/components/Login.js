import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = ({ setUser }) => {
    const [role, setRole] = useState('');
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const navigate = useNavigate();

    const handleLogin = () => {
        if (role === 'Admin') {
            localStorage.setItem('loggedInAdmin', 'true');
            setUser('Admin');
            navigate('/dashboard');
        } else if (role === 'Student') {
            localStorage.setItem('loggedInStudent', 'true');
            setUser('Student');
            navigate('/student/portal');
        } else {
            alert('Invalid role or credentials');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6">Login</h2>
                <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    className="w-full mb-4 p-2 border rounded"
                >
                    <option value="">Select Role</option>
                    <option value="Admin">Admin</option>
                    <option value="Student">Student</option>
                </select>
                <input
                    type="text"
                    placeholder="Username"
                    value={credentials.username}
                    onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                    className="w-full mb-4 p-2 border rounded"
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={credentials.password}
                    onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                    className="w-full mb-4 p-2 border rounded"
                />
                <button
                    onClick={handleLogin}
                    className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                >
                    Login
                </button>
            </div>
        </div>
    );
};

export default Login;
