import React, { useState } from 'react';
import apiService from '../services/apiService';

const MarksEntry = () => {
    const grades = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'];
    const sections = ['A', 'B', 'C', 'D'];
    const subjects = ['Math', 'Science', 'English', 'History', 'Geography'];

    const [selectedGrade, setSelectedGrade] = useState('');
    const [selectedSection, setSelectedSection] = useState('');
    const [selectedSubject, setSelectedSubject] = useState('');
    const [students, setStudents] = useState([]);
    const [marksData, setMarksData] = useState({});
    const [maxMarks] = useState(100); // Removed `setMaxMarks` as it is unused
    const [loading, setLoading] = useState(false);
    const [alertMessage, setAlertMessage] = useState('');

    const handleLoadStudents = async () => {
        setLoading(true);
        try {
            const allStudents = await apiService.get('students'); // Fetch students from the mock API
            if (!Array.isArray(allStudents)) throw new Error('Invalid data format');

            const filteredStudents = allStudents.filter(
                (student) => student.grade === selectedGrade && student.section === selectedSection
            );

            // Initialize marksData with empty or existing marks
            const existingMarks = await apiService.get('results'); // Mock API call for existing marks
            const prefilledMarks = {};
            filteredStudents.forEach((student) => {
                const existingMark = existingMarks.find(
                    (mark) => mark.studentId === student.id && mark.subject === selectedSubject
                );
                prefilledMarks[student.id] = existingMark ? existingMark.marks : '';
            });

            setStudents(filteredStudents);
            setMarksData(prefilledMarks);
        } catch (error) {
            console.error('Error loading students:', error);
            alert('Failed to load students. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    const handleMarksChange = (studentId, value) => {
        const numericValue = parseInt(value, 10);
        if (isNaN(numericValue) || numericValue < 0 || numericValue > maxMarks) {
            setMarksData((prev) => ({ ...prev, [studentId]: 'Invalid' }));
        } else {
            setMarksData((prev) => ({ ...prev, [studentId]: numericValue }));
        }
    };

    const handleBulkUpdate = (defaultMark) => {
        const updatedMarks = {};
        students.forEach((student) => {
            updatedMarks[student.id] = defaultMark;
        });
        setMarksData(updatedMarks);
    };

    const handleSaveMarks = async () => {
        const results = students.map((student) => ({
            studentId: student.id,
            grade: selectedGrade,
            section: selectedSection,
            subject: selectedSubject,
            marks: marksData[student.id] || '',
            date: new Date().toISOString(),
        }));

        try {
            await apiService.post('results', results); // Mock API call
            console.log('Saved results:', results); // Log for testing
            setAlertMessage('Marks saved successfully!');
            setTimeout(() => setAlertMessage(''), 3000); // Clear alert after 3 seconds
        } catch (error) {
            console.error('Error saving marks:', error);
        }
    };

    const calculateGrade = (mark) => {
        if (mark > 90) return 'A';
        if (mark > 80) return 'B';
        if (mark > 70) return 'C';
        if (mark > 60) return 'D';
        if (mark > 50) return 'E';
        return 'F';
    };

    return (
        <div className="p-6 bg-slate-50 min-h-screen">
            {/* Success Alert */}
            {alertMessage && (
                <div className="mb-4 p-4 bg-green-100 text-green-800 rounded-lg">
                    {alertMessage}
                </div>
            )}

            {/* Header UI */}
            <div className="flex items-center gap-4 mb-6">
                <select
                    value={selectedGrade}
                    onChange={(e) => setSelectedGrade(e.target.value)}
                    className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                    <option value="">Select Grade</option>
                    {grades.map((grade) => (
                        <option key={grade} value={grade}>
                            {grade}
                        </option>
                    ))}
                </select>
                <select
                    value={selectedSection}
                    onChange={(e) => setSelectedSection(e.target.value)}
                    className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                    <option value="">Select Section</option>
                    {sections.map((section) => (
                        <option key={section} value={section}>
                            {section}
                        </option>
                    ))}
                </select>
                <select
                    value={selectedSubject}
                    onChange={(e) => setSelectedSubject(e.target.value)}
                    className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                    <option value="">Select Subject</option>
                    {subjects.map((subject) => (
                        <option key={subject} value={subject}>
                            {subject}
                        </option>
                    ))}
                </select>
                <button
                    onClick={handleLoadStudents}
                    className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
                    disabled={loading}
                >
                    {loading ? 'Loading...' : 'Load Students'}
                </button>
                <button
                    onClick={() => handleBulkUpdate(0)}
                    className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition"
                >
                    Set All to 0
                </button>
            </div>

            {/* Student Marks Table */}
            {students.length > 0 && (
                <div className="bg-white shadow-md rounded-lg p-4 overflow-x-auto">
                    <table className="w-full table-auto border-collapse">
                        <thead className="sticky top-0 bg-slate-100">
                            <tr className="text-left">
                                <th className="px-4 py-2 border">Roll Number</th>
                                <th className="px-4 py-2 border">Student Name</th>
                                <th className="px-4 py-2 border">Marks</th>
                                <th className="px-4 py-2 border">Grade</th>
                            </tr>
                        </thead>
                        <tbody>
                            {students.map((student) => {
                                const mark = marksData[student.id];
                                const isInvalid = mark === 'Invalid';
                                return (
                                    <tr key={student.id} className="hover:bg-slate-50">
                                        <td className="px-4 py-2 border">{student.rollNumber}</td>
                                        <td className="px-4 py-2 border">{student.name}</td>
                                        <td className="px-4 py-2 border">
                                            <input
                                                type="number"
                                                value={isInvalid ? '' : mark}
                                                onChange={(e) => handleMarksChange(student.id, e.target.value)}
                                                className={`w-20 px-2 py-1 border rounded ${isInvalid ? 'border-red-500' : ''}`}
                                                title={isInvalid ? 'Invalid Mark' : ''}
                                            />
                                        </td>
                                        <td className="px-4 py-2 border">{!isInvalid && mark !== '' ? calculateGrade(mark) : '-'}</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Save Button */}
            {students.length > 0 && (
                <div className="mt-6">
                    <button
                        onClick={handleSaveMarks}
                        className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
                    >
                        Save All Marks
                    </button>
                </div>
            )}
        </div>
    );
};

export default MarksEntry;
