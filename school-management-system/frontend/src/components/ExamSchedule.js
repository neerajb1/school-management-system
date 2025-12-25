import React, { useState, useEffect } from 'react';
import FilterBar from './FilterBar';
import { Calendar, Clock, MapPin, BookOpen, Plus, X, Printer, GraduationCap, Users } from "lucide-react";

const ExamSchedule = () => {
    const [exams, setExams] = useState([]);
    const [filteredExams, setFilteredExams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);

    // Filter States
    const [searchTerm, setSearchTerm] = useState(""); 
    const [selectedGrade, setSelectedGrade] = useState("All Grades");
    const [selectedSection, setSelectedSection] = useState("All Sections");

    // Form State for the Popup
    const [formData, setFormData] = useState({
        subject: '',
        grade: 'Grade 10',
        section: 'A',
        date: '',
        time: '',
        room: '',
        duration: '3 Hours'
    });

    useEffect(() => {
        const fetchExams = async () => {
            setLoading(true);
            try {
                const response = await fetch("/api/exams.json");
                const data = await response.json();
                setExams(data);
                setFilteredExams(data);
                setLoading(false);
            } catch (err) {
                setLoading(false);
            }
        };
        fetchExams();
    }, []);

    useEffect(() => {
        let result = exams;
        if (searchTerm) result = result.filter(ex => ex.subject.toLowerCase().includes(searchTerm.toLowerCase()));
        if (selectedGrade !== "All Grades") result = result.filter(ex => ex.grade === selectedGrade);
        if (selectedSection !== "All Sections") result = result.filter(ex => ex.section === selectedSection);
        setFilteredExams(result);
    }, [searchTerm, selectedGrade, selectedSection, exams]);

    const filtersConfig = [
        { label: "Grade", value: selectedGrade, options: ["All Grades", "Grade 10", "Grade 11", "Grade 12"], onChange: setSelectedGrade, defaultValue: "All Grades" },
        { label: "Section", value: selectedSection, options: ["All Sections", "A", "B", "C"], onChange: setSelectedSection, defaultValue: "All Sections" }
    ];

    return (
        <div className="p-6 bg-slate-50 min-h-screen">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-slate-800">Exam Schedule</h1>
                <div className="flex gap-3">
                    <button onClick={() => window.print()} className="flex items-center gap-2 bg-white border px-4 py-2 rounded-lg hover:bg-slate-50">
                        <Printer size={18} /> Print
                    </button>
                    <button onClick={() => setShowModal(true)} className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 shadow-md">
                        <Plus size={18} /> Add New
                    </button>
                </div>
            </div>

            <FilterBar 
                searchTerm={searchTerm} 
                onSearchChange={setSearchTerm} 
                filters={filtersConfig} 
                onReset={() => { setSearchTerm(""); setSelectedGrade("All Grades"); setSelectedSection("All Sections"); }} 
            />

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
                {filteredExams.map((exam) => (
                    <div key={exam.id} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 transition-all hover:border-indigo-200">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-2 bg-indigo-50 rounded-lg text-indigo-600">
                                <BookOpen size={24} />
                            </div>
                            <span className="text-xs font-bold px-2 py-1 bg-slate-100 text-slate-600 rounded">
                                {exam.grade} - {exam.section}
                            </span>
                        </div>
                        <h3 className="text-xl font-bold text-slate-800 mb-4">{exam.subject}</h3>
                        <div className="space-y-3 text-sm text-slate-600">
                            <div className="flex items-center gap-3"><Calendar size={16} /> {exam.date}</div>
                            <div className="flex items-center gap-3"><Clock size={16} /> {exam.time}</div>
                            <div className="flex items-center gap-3"><MapPin size={16} /> {exam.room}</div>
                        </div>
                    </div>
                ))}
            </div>

            {/* ADD EXAM MODAL - UPDATED WITH GRADE/SECTION DROPDOWNS */}
            {showModal && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="bg-white p-8 rounded-2xl w-full max-w-lg shadow-2xl relative">
                        <button onClick={() => setShowModal(false)} className="absolute top-4 right-4 text-slate-400 hover:text-slate-600"><X size={24}/></button>
                        
                        <h2 className="text-2xl font-bold mb-6 text-slate-800">Add New Exam</h2>
                        
                        <form className="space-y-5" onSubmit={(e) => { e.preventDefault(); setShowModal(false); }}>
                            {/* Subject Input */}
                            <div>
                                <label className="block text-sm font-semibold text-slate-700 mb-2">Subject Name</label>
                                <input 
                                    type="text" 
                                    className="w-full border border-slate-200 p-3 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none" 
                                    placeholder="e.g. Physics" 
                                    required 
                                />
                            </div>

                            {/* Grade and Section Selection */}
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold text-slate-700 mb-2">Grade</label>
                                    <div className="relative">
                                        <select className="w-full border border-slate-200 p-3 rounded-xl appearance-none bg-white focus:ring-2 focus:ring-indigo-500 outline-none">
                                            <option>Grade 10</option>
                                            <option>Grade 11</option>
                                            <option>Grade 12</option>
                                        </select>
                                        <GraduationCap className="absolute right-3 top-3.5 text-slate-400" size={18} />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-slate-700 mb-2">Section</label>
                                    <div className="relative">
                                        <select className="w-full border border-slate-200 p-3 rounded-xl appearance-none bg-white focus:ring-2 focus:ring-indigo-500 outline-none">
                                            <option>A</option>
                                            <option>B</option>
                                            <option>C</option>
                                        </select>
                                        <Users className="absolute right-3 top-3.5 text-slate-400" size={18} />
                                    </div>
                                </div>
                            </div>

                            {/* Date and Time Selection */}
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold text-slate-700 mb-2">Date</label>
                                    <input type="date" className="w-full border border-slate-200 p-3 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none" required />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-slate-700 mb-2">Start Time</label>
                                    <input type="time" className="w-full border border-slate-200 p-3 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none" required />
                                </div>
                            </div>

                            {/* Room Selection */}
                            <div>
                                <label className="block text-sm font-semibold text-slate-700 mb-2">Exam Hall / Room</label>
                                <input type="text" className="w-full border border-slate-200 p-3 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none" placeholder="e.g. Hall A-1" required />
                            </div>

                            <div className="pt-4 flex gap-3">
                                <button type="button" onClick={() => setShowModal(false)} className="flex-1 py-3 bg-slate-100 text-slate-600 rounded-xl font-bold hover:bg-slate-200 transition-colors">Cancel</button>
                                <button type="submit" className="flex-1 py-3 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all">Save Schedule</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ExamSchedule;