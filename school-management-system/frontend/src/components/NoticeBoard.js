import React, { useState, useEffect } from "react";
import apiService from "../services/apiService";

const NoticeBoard = ({ isAdmin = false }) => {
    const [notices, setNotices] = useState([]);
    const [newNotice, setNewNotice] = useState({ title: '', content: '', priority: 'Low' });
    const [showForm, setShowForm] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNotices = async () => {
            try {
                // Fetch JSON data from /public/api/notices.json
                const response = await fetch("/api/notices.json");
                if (!response.ok) throw new Error("Failed to load notices.");
                const data = await response.json();
                console.log("DEBUG NOTICES:", data); // Debugging log
                setNotices(data);
            } catch (err) {
                console.error("Error fetching notices:", err);
                setError("Failed to load notices.");
            }
        };

        fetchNotices();
    }, []);

    const handleAddNotice = async () => {
        try {
            setNotices((prev) => [newNotice, ...prev]); // Update the list locally
            setNewNotice({ title: '', content: '', priority: 'Low' }); // Reset form
            setShowForm(false); // Close the form
        } catch (error) {
            console.error('Error adding notice:', error);
        }
    };

    const priorityColors = {
        High: 'bg-red-500',
        Medium: 'bg-yellow-500',
        Low: 'bg-blue-500',
    };

    if (error) {
        return <div className="text-red-500">{error}</div>;
    }

    if (!notices.length) {
        return <div className="text-gray-500 text-center">No notices available.</div>;
    }

    return (
        <div className="p-4 bg-white shadow-md rounded-lg max-h-[400px] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">Notice Board</h2>

            {/* Admin Add Notice Button */}
            {isAdmin && !showForm && (
                <button
                    onClick={() => setShowForm(true)}
                    className="mb-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
                >
                    Add Notice
                </button>
            )}

            {/* Add Notice Form */}
            {isAdmin && showForm && (
                <div className="mb-4 p-4 border rounded-lg bg-gray-50">
                    <h3 className="text-lg font-bold mb-2">Add New Notice</h3>
                    <input
                        type="text"
                        placeholder="Title"
                        value={newNotice.title}
                        onChange={(e) => setNewNotice({ ...newNotice, title: e.target.value })}
                        className="w-full mb-2 px-3 py-2 border rounded-lg"
                    />
                    <textarea
                        placeholder="Content"
                        value={newNotice.content}
                        onChange={(e) => setNewNotice({ ...newNotice, content: e.target.value })}
                        className="w-full mb-2 px-3 py-2 border rounded-lg"
                        rows="3"
                    ></textarea>
                    <select
                        value={newNotice.priority}
                        onChange={(e) => setNewNotice({ ...newNotice, priority: e.target.value })}
                        className="w-full mb-2 px-3 py-2 border rounded-lg"
                    >
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                    </select>
                    <div className="flex gap-2">
                        <button
                            onClick={handleAddNotice}
                            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
                        >
                            Save
                        </button>
                        <button
                            onClick={() => setShowForm(false)}
                            className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            )}

            {/* Notices List */}
            {notices.map((notice, index) => (
                <div
                    key={index}
                    className="p-4 mb-4 border rounded-lg shadow-sm bg-gray-50"
                >
                    <div className="flex items-center gap-2 mb-2">
                        <span
                            className={`w-3 h-3 rounded-full ${priorityColors[notice.priority]}`}
                        ></span>
                        <h3 className="font-bold">{notice.title}</h3>
                        <span className="text-sm text-gray-500 ml-auto">{notice.date || 'N/A'}</span>
                    </div>
                    <p className="text-gray-700">{notice.content}</p>
                </div>
            ))}
        </div>
    );
};

export default NoticeBoard;
