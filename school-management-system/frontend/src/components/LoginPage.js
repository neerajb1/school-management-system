import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = () => {
        setLoading(true);
        setTimeout(() => {
            if (email === 'admin@school.com' && password === 'admin123') {
                const user = { name: 'Admin User', role: 'admin', token: 'mock-jwt-123' };
                localStorage.setItem('user', JSON.stringify(user));
                navigate('/dashboard');
            } else {
                alert('Invalid email or password');
            }
            setLoading(false);
        }, 1000);
    };

    return (
        <div
            className="h-screen w-screen bg-cover bg-center flex items-center justify-center"
            style={{ backgroundImage: "url('/hero.jpg')" }}
        >
            <div className="bg-white/20 backdrop-blur-xl p-8 rounded-2xl shadow-2xl border border-white/30 w-96">
                <h1 className="text-3xl font-bold text-white text-center mb-4">Welcome Back</h1>
                <p className="text-sm text-gray-300 text-center mb-6">Please enter your school credentials</p>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
                    <input
                        type="email"
                        className="w-full p-3 rounded-lg bg-white/60 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                    />
                </div>
                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
                    <input
                        type="password"
                        className="w-full p-3 rounded-lg bg-white/60 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                    />
                </div>
                <button
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                    onClick={handleLogin}
                    disabled={loading}
                >
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </div>
        </div>
    );
};

export default LoginPage;
