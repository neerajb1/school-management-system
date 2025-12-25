import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { QRCodeCanvas } from 'qrcode.react';
import apiService from '../services/apiService';

const StudentPortal = () => {
    const [student, setStudent] = useState(null);
    const [attendance, setAttendance] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const loggedInStudent = JSON.parse(localStorage.getItem('loggedInStudent'));
        if (!loggedInStudent) {
            navigate('/student/login');
            return;
        }

        setStudent(loggedInStudent);

        const fetchAttendance = async () => {
            try {
                const attendanceData = await apiService.get('attendance');
                const studentAttendance = attendanceData
                    .flatMap((item) => item.records)
                    .filter((record) => record.studentId === loggedInStudent.admissionId);
                setAttendance(studentAttendance);
            } catch (err) {
                console.error('Error fetching attendance:', err);
            }
        };

        fetchAttendance();
    }, [navigate]);

    useEffect(() => {
        console.log('StudentPortal component rendered'); // Debug log
    }, []);

    if (!student) {
        return null;
    }

    return (
        <div className="min-h-screen bg-slate-50 p-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Profile Card */}
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <h2 className="text-2xl font-bold text-slate-800 mb-4">{student.name}</h2>
                    <p className="text-sm text-gray-500 mb-2">
                        <strong>Student ID:</strong> {student.admissionId}
                    </p>
                    <p className="text-sm text-gray-500 mb-2">
                        <strong>Grade:</strong> {student.grade}
                    </p>
                    <p className="text-sm text-gray-500 mb-2">
                        <strong>Section:</strong> {student.section}
                    </p>
                    <QRCodeCanvas value={student.admissionId} size={64} />
                </div>

                {/* Attendance History */}
                <div className="col-span-2 bg-white rounded-xl shadow-sm p-6">
                    <h2 className="text-xl font-bold text-slate-800 mb-4">Attendance History</h2>
                    {attendance.length > 0 ? (
                        <table className="w-full table-auto divide-y divide-slate-200">
                            <thead>
                                <tr className="text-left text-slate-500 bg-slate-50 uppercase text-sm">
                                    <th className="py-4 px-6">Date</th>
                                    <th className="py-4 px-6">Status</th>
                                    <th className="py-4 px-6">Remarks</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {attendance.map((record, index) => (
                                    <tr key={index} className="hover:bg-slate-50 transition-colors">
                                        <td className="py-4 px-6">{record.date}</td>
                                        <td className="py-4 px-6">{record.status}</td>
                                        <td className="py-4 px-6">{record.remarks || 'N/A'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ) : (
                        <p className="text-gray-500">No attendance records available.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default StudentPortal; // Ensure this is present
