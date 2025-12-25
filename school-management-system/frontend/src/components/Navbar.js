import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="fixed top-0 left-0 w-full bg-slate-900 text-white px-6 py-4 flex justify-between items-center shadow-lg z-50">
            <div className="text-2xl font-bold">School System</div>
            <ul className="flex space-x-6 list-none">
                <li>
                    <Link to="/" className="hover:text-blue-400">Home</Link>
                </li>
                <li>
                    <Link to="/about" className="hover:text-blue-400">About</Link>
                </li>
                <li>
                    <Link to="/news" className="hover:text-blue-400">News</Link>
                </li>
                <li>
                    <Link to="/contact" className="hover:text-blue-400">Contact</Link>
                </li>
            </ul>
            <Link
                to="/login"
                className="bg-blue-600 px-4 py-2 rounded-lg text-white hover:bg-blue-700 transition"
            >
                Login
            </Link>
        </nav>
    );
};

export default Navbar;
