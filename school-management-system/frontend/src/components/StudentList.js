import React, { useState, useEffect, useRef } from 'react';
import Papa from 'papaparse';
import { Download, Upload, Trash2, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';
import QuickViewModal from "./QuickViewModal";
import AddStudentModal from "./AddStudentModal";
import FilterBar from "./FilterBar";
import { fetchStudents, getGrades, getSections } from "../services/dataService";

const StudentList = () => {
    const [students, setStudents] = useState([]);
    const [grades, setGrades] = useState([]);
    const [sections, setSections] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedGrade, setSelectedGrade] = useState('All Grades');
    const [selectedSection, setSelectedSection] = useState('All Sections');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [importing, setImporting] = useState(false);
    const [showAddStudentModal, setShowAddStudentModal] = useState(false);
    const [newStudent, setNewStudent] = useState({
        admissionId: '',
        name: '',
        fatherName: '',
        grade: '',
        section: '',
        status: 'Active',
    });
    const fileInputRef = useRef(null);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        const loadInitialData = async () => {
            try {
                const [studentsData, gradesData, sectionsData] = await Promise.all([
                    fetchStudents(),
                    getGrades(),
                    getSections(),
                ]);
                setStudents(studentsData);
                setGrades(['All Grades', ...gradesData]);
                setSections(['All Sections', ...sectionsData]);
            } catch (err) {
                console.error("Error loading data:", err);
                setError("Failed to load data.");
            } finally {
                setLoading(false);
            }
        };

        loadInitialData();
    }, []);

    const filteredStudents = students.filter((student) => {
        const matchesSearch = student.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            student.admissionId?.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesGrade = selectedGrade === 'All Grades' || student.grade === selectedGrade;
        const matchesSection = selectedSection === 'All Sections' || student.section === selectedSection;

        return matchesSearch && matchesGrade && matchesSection;
    });

    const handleResetFilters = () => {
        setSearchTerm('');
        setSelectedGrade('All Grades');
        setSelectedSection('All Sections');
    };

    const filtersConfig = [
        {
            value: selectedGrade,
            onChange: setSelectedGrade,
            options: grades,
            defaultValue: 'All Grades',
        },
        {
            value: selectedSection,
            onChange: setSelectedSection,
            options: sections,
            defaultValue: 'All Sections',
        },
    ];

    const handleAddStudent = () => {
        setStudents((prevStudents) => [...prevStudents, newStudent]);
        setShowAddStudentModal(false);
        setNewStudent({
            admissionId: '',
            name: '',
            fatherName: '',
            grade: '',
            section: '',
            status: 'Active',
        });
    };

    const deleteStudent = (id) => {
        if (window.confirm('Are you sure you want to delete this student?')) {
            setStudents((prevStudents) => prevStudents.filter((student) => student.id !== id));
        }
    };

    const openModal = (student) => {
        setSelectedStudent(student);
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setSelectedStudent(null);
        setIsModalOpen(false);
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-gray-500">Loading...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-red-500">{error}</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50 p-8">
            {/* Header */}
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
                <h1 className="text-3xl font-bold text-slate-800 mb-4">Student Directory</h1>
                <FilterBar
                    searchTerm={searchTerm}
                    onSearchChange={setSearchTerm}
                    filters={filtersConfig}
                    onReset={handleResetFilters}
                />
            </div>

            {/* Importing State */}
            {importing && (
                <div className="mb-4 p-4 bg-yellow-100 text-yellow-700 rounded-lg">
                    Importing students... Please wait.
                </div>
            )}

            {/* Student Table */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <table className="w-full table-auto divide-y divide-slate-200">
                    <thead>
                        <tr className="text-left text-slate-500 bg-slate-50 uppercase text-sm">
                            <th className="py-4 px-6">Admission ID</th>
                            <th className="py-4 px-6">Name</th>
                            <th className="py-4 px-6">Grade/Section</th>
                            <th className="py-4 px-6">Status</th>
                            <th className="py-4 px-6">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {filteredStudents.length > 0 ? (
                            filteredStudents.map((student) => (
                                <tr key={student.id} className="hover:bg-slate-50 transition-colors">
                                    <td className="py-4 px-6 font-mono text-sm text-slate-500">{student.admissionId}</td>
                                    <td className="py-4 px-6">
                                        <Link to={`/students/${student.id}`} className="text-blue-600 hover:underline">
                                            {student.name}
                                        </Link>
                                    </td>
                                    <td className="py-4 px-6">{`${student.grade} / ${student.section}`}</td>
                                    <td className="py-4 px-6">
                                        <span
                                            className={`px-3 py-1 rounded-full text-sm ${
                                                student.status === 'Active'
                                                    ? 'bg-green-100 text-green-700'
                                                    : 'bg-gray-100 text-gray-700'
                                            }`}
                                        >
                                            {student.status}
                                        </span>
                                    </td>
                                    <td className="py-4 px-6 flex gap-2">
                                        <button
                                            onClick={() => deleteStudent(student.id)}
                                            className="text-red-500 hover:text-red-700"
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                        <button
                                            onClick={() => openModal(student)}
                                            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
                                        >
                                            Quick View
                                        </button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="5" className="py-4 px-6 text-center text-gray-500">
                                    No students found.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Add Student Modal */}
            <AddStudentModal
                show={showAddStudentModal}
                onClose={() => setShowAddStudentModal(false)}
                onSave={handleAddStudent}
                newStudent={newStudent}
                setNewStudent={setNewStudent}
            />

            {/* Quick View Modal */}
            <QuickViewModal
                student={selectedStudent}
                isOpen={isModalOpen}
                onClose={closeModal}
            />
        </div>
    );
};

export default StudentList;