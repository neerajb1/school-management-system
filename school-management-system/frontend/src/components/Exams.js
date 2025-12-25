import React, { useState, useEffect } from "react";
import FilterBar from "./FilterBar";
import { Calendar, Clock, MapPin, BookOpen, Plus, X } from "lucide-react";

const Exams = () => {
  const [allExams, setAllExams] = useState([]);
  const [filteredExams, setFilteredExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);

  // Filter States - Must match DefaultValue exactly
  const [searchTerm, setSearchTerm] = useState(""); 
  const [selectedGrade, setSelectedGrade] = useState("All Grades");
  const [selectedSection, setSelectedSection] = useState("All Sections");

  useEffect(() => {
    const fetchExams = async () => {
      setLoading(true);
      try {
        // FORCE LOCAL FETCH: Avoids the 5001 error
        const response = await fetch("/api/exams.json"); 
        const data = await response.json();
        setAllExams(data);
        setFilteredExams(data);
        setLoading(false);
      } catch (err) {
        console.error("Local fetch failed:", err);
        setLoading(false);
      }
    };
    fetchExams();
  }, []);

  // Filter Logic
  useEffect(() => {
    let result = allExams;
    if (searchTerm) {
      result = result.filter(ex => ex.subject.toLowerCase().includes(searchTerm.toLowerCase()));
    }
    if (selectedGrade !== "All Grades") {
      result = result.filter(ex => ex.grade === selectedGrade);
    }
    if (selectedSection !== "All Sections") {
      result = result.filter(ex => ex.section === selectedSection);
    }
    setFilteredExams(result);
  }, [searchTerm, selectedGrade, selectedSection, allExams]);

  const filtersConfig = [
    { 
      label: "Grade", 
      value: selectedGrade, 
      options: ["All Grades", "Grade 10", "Grade 11", "Grade 12"], 
      onChange: setSelectedGrade, 
      defaultValue: "All Grades" 
    },
    { 
      label: "Section", 
      value: selectedSection, 
      options: ["All Sections", "A", "B", "C"], 
      onChange: setSelectedSection, 
      defaultValue: "All Sections" 
    }
  ];

  if (loading) return <div className="p-10 text-center text-slate-500">Connecting to local data...</div>;

  return (
    <div className="p-6 bg-slate-50 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <div>
            <h1 className="text-2xl font-bold text-slate-800">Exam Schedule</h1>
            <p className="text-sm text-slate-500">Local JSON Data Active</p>
        </div>
        <button 
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 shadow-md transition-all"
        >
          <Plus size={20} /> Add New Exam
        </button>
      </div>

      <FilterBar 
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm} 
        filters={filtersConfig} 
        onReset={() => { setSearchTerm(""); setSelectedGrade("All Grades"); setSelectedSection("All Sections"); }} 
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        {filteredExams.map((exam) => (
          <div key={exam.id} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 hover:border-indigo-200 transition-all">
            <div className="flex justify-between items-start mb-4">
                <div className="p-2 bg-indigo-50 rounded-lg text-indigo-600">
                  <BookOpen size={24} />
                </div>
                <span className="text-xs font-bold px-2 py-1 bg-slate-100 text-slate-600 rounded">
                  {exam.duration || '3 Hours'}
                </span>
            </div>
            <h3 className="text-xl font-bold text-slate-800 mb-4">{exam.subject}</h3>
            <div className="space-y-3 text-sm text-slate-600">
              <div className="flex items-center gap-3"><Calendar size={16} className="text-indigo-500"/> {exam.date}</div>
              <div className="flex items-center gap-3"><Clock size={16} className="text-indigo-500"/> {exam.time}</div>
              <div className="flex items-center gap-3"><MapPin size={16} className="text-indigo-500"/> Room: {exam.room}</div>
            </div>
          </div>
        ))}
      </div>

      {/* ADD EXAM MODAL */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-2xl w-full max-w-md shadow-2xl relative animate-in fade-in zoom-in duration-200">
            <button onClick={() => setShowAddModal(false)} className="absolute top-4 right-4 text-slate-400 hover:text-slate-600">
              <X size={24} />
            </button>
            <h2 className="text-xl font-bold text-slate-800 mb-6">Schedule New Exam</h2>
            <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); setShowAddModal(false); }}>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Subject</label>
                <input type="text" placeholder="Mathematics" className="w-full border border-slate-200 p-2.5 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500" required />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Date</label>
                    <input type="date" className="w-full border border-slate-200 p-2.5 rounded-lg" required />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Time</label>
                    <input type="time" className="w-full border border-slate-200 p-2.5 rounded-lg" required />
                </div>
              </div>
              <button type="submit" className="w-full bg-indigo-600 text-white py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors mt-4">
                Add to Schedule
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Exams;