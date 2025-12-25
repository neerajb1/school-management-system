import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import apiService from '../services/apiService';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const StudentProfile = () => {
    const { id } = useParams();
    const [student, setStudent] = useState(null);
    const [results, setResults] = useState([]);
    const [attendance, setAttendance] = useState([]);
    const [loading, setLoading] = useState(true);
    const printRef = useRef();

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch student data
                const studentsData = await apiService.get('students');
                const students = Array.isArray(studentsData) ? studentsData : [];
                const student = students.find((s) => s.id === parseInt(id));
                setStudent(student);

                // Fetch results data
                const resultsData = await apiService.get('results');
                const studentResults = Array.isArray(resultsData)
                    ? resultsData.filter((result) => result.studentId === parseInt(id))
                    : [];
                setResults(studentResults);

                // Fetch attendance data
                const attendanceData = await apiService.get('attendance');
                const studentAttendance = Array.isArray(attendanceData)
                    ? attendanceData.filter((record) =>
                          record.records.some((r) => r.studentId === student.admissionId)
                      )
                    : [];
                setAttendance(studentAttendance);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-gray-500">Loading Profile...</p>
            </div>
        );
    }

    if (!student) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-red-500 text-lg">Student not found.</p>
            </div>
        );
    }

    // Calculate Overall Attendance Percentage
    const totalAttendanceRecords = attendance.reduce(
        (acc, record) => acc + record.records.length,
        0
    );
    const totalPresent = attendance.reduce(
        (acc, record) =>
            acc +
            record.records.filter((r) => r.status === 'Present').length,
        0
    );
    const attendancePercentage = totalAttendanceRecords
        ? ((totalPresent / totalAttendanceRecords) * 100).toFixed(2)
        : 'No Data';

    // Prepare data for the bar chart
    const performanceData = results.map((result) => ({
        subject: result.subject,
        marks: result.marks,
    }));

    const handlePrint = () => {
        window.print();
    };

    return (
        <div className="min-h-screen bg-slate-50 p-8">
            {/* Header Card */}
            <div className="bg-white rounded-xl shadow-md p-6 flex items-center gap-6 mb-8">
                <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center">
                    <span className="text-gray-500">Photo</span>
                </div>
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">{student.name}</h1>
                    <p className="text-sm text-gray-500">
                        <strong>Roll Number:</strong> {student.admissionId}
                    </p>
                    <p className="text-sm text-gray-500">
                        <strong>Grade:</strong> {student.grade} - {student.section}
                    </p>
                </div>
            </div>

            {/* Academic Summary */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                {/* Marks Table */}
                <div className="bg-white rounded-xl shadow-md p-6">
                    <h2 className="text-xl font-bold text-slate-800 mb-4">Academic Performance</h2>
                    {results.length > 0 ? (
                        <table className="w-full table-auto border-collapse">
                            <thead>
                                <tr className="bg-slate-100">
                                    <th className="px-4 py-2 border">Subject</th>
                                    <th className="px-4 py-2 border">Marks</th>
                                </tr>
                            </thead>
                            <tbody>
                                {results.map((result, index) => (
                                    <tr key={index} className="hover:bg-slate-50">
                                        <td className="px-4 py-2 border">{result.subject}</td>
                                        <td className="px-4 py-2 border">{result.marks}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ) : (
                        <p className="text-gray-500">No academic data available.</p>
                    )}
                </div>

                {/* Performance Chart */}
                <div className="bg-white rounded-xl shadow-md p-6">
                    <h2 className="text-xl font-bold text-slate-800 mb-4">Performance Chart</h2>
                    {performanceData.length > 0 ? (
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={performanceData}>
                                <XAxis dataKey="subject" />
                                <YAxis />
                                <Tooltip />
                                <Bar dataKey="marks" fill="#3b82f6" />
                            </BarChart>
                        </ResponsiveContainer>
                    ) : (
                        <p className="text-gray-500">No performance data available.</p>
                    )}
                </div>
            </div>

            {/* Contact Information */}
            <div className="bg-white rounded-xl shadow-md p-6 mb-8">
                <h2 className="text-xl font-bold text-slate-800 mb-4">Contact Information</h2>
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <p className="font-bold">Father's Name:</p>
                        <p>{student.fatherName || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="font-bold">Mother's Name:</p>
                        <p>{student.motherName || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="font-bold">Contact:</p>
                        <p>{student.contact || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="font-bold">Address:</p>
                        <p>{student.address || 'N/A'}</p>
                    </div>
                </div>
            </div>

            {/* Print Report Card */}
            <div className="text-center">
                <button
                    onClick={handlePrint}
                    className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
                >
                    Download Report Card
                </button>
            </div>

            {/* Print View */}
            <div ref={printRef} className="hidden print:block">
                <div className="border border-gray-300 p-8 bg-white">
                    <h1 className="text-3xl font-bold text-center mb-8">Student Report Card</h1>
                    <div className="mb-8">
                        <p>
                            <strong>Name:</strong> {student.name}
                        </p>
                        <p>
                            <strong>Roll Number:</strong> {student.admissionId}
                        </p>
                        <p>
                            <strong>Grade:</strong> {student.grade} - {student.section}
                        </p>
                    </div>
                    <h2 className="text-xl font-bold mb-4">Academic Performance</h2>
                    <table className="w-full table-auto border-collapse mb-8">
                        <thead>
                            <tr className="bg-slate-100">
                                <th className="px-4 py-2 border">Subject</th>
                                <th className="px-4 py-2 border">Marks</th>
                            </tr>
                        </thead>
                        <tbody>
                            {results.map((result, index) => (
                                <tr key={index}>
                                    <td className="px-4 py-2 border">{result.subject}</td>
                                    <td className="px-4 py-2 border">{result.marks}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <h2 className="text-xl font-bold mb-4">Attendance</h2>
                    <p>Overall Attendance: {attendancePercentage}%</p>
                </div>
            </div>
        </div>
    );
};

export default StudentProfile;
