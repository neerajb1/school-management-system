import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, User, Phone, Mail, MapPin, Calendar, Heart, Shield } from "lucide-react";

const StudentDetail = () => {
  // Use 'id' to match your App.js route: /students/:id
  const { id } = useParams(); 
  const navigate = useNavigate();
  
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStudentData = async () => {
      try {
        setLoading(true);
        // 1. Fetch the single source of truth: students.json
        const response = await fetch("/api/students.json");
        
        if (!response.ok) {
          throw new Error("Student database file not found. Ensure public/api/students.json exists.");
        }
        
        const allStudents = await response.json();
        
        // 2. Find the specific student in the array using the ID from the URL
        // We compare against 'admissionId' which matches your JSON structure
        const foundStudent = allStudents.find(s => s.id === Number(id));
        
        if (foundStudent) {
          setStudent(foundStudent);
        } else {
          setError(`Student with ID ${id} not found in the database.`);
        }
      } catch (err) {
        console.error("Fetch error:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchStudentData();
  }, [id]);

  if (loading) return <div className="p-10 text-center text-slate-500">Loading student profile...</div>;
  
  if (error) return (
    <div className="p-10 text-center">
      <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-4 inline-block border border-red-100">
        {error}
      </div>
      <br />
      <button onClick={() => navigate('/students')} className="text-blue-500 hover:underline flex items-center justify-center gap-2 mx-auto">
        <ArrowLeft size={16} /> Return to Student List
      </button>
    </div>
  );

  return (
    <div className="p-6 bg-slate-50 min-h-screen">
      <button 
        onClick={() => navigate('/students')} 
        className="mb-6 flex items-center gap-2 text-slate-600 hover:text-blue-600 transition-colors font-medium"
      >
        <ArrowLeft size={20} /> Back to Student List
      </button>

      <div className="max-w-5xl mx-auto bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {/* Header Section */}
        <div className="bg-slate-900 p-8 text-white">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="w-32 h-32 bg-white/10 rounded-full flex items-center justify-center border-4 border-white/20 shadow-inner">
              <User size={64} className="text-white/80" />
            </div>
            <div className="text-center md:text-left">
              <h1 className="text-4xl font-bold mb-2">{student.name}</h1>
              <div className="flex flex-wrap justify-center md:justify-start gap-3">
                <span className="px-4 py-1 bg-blue-500 rounded-full text-sm font-semibold">{student.grade}</span>
                <span className="px-4 py-1 bg-indigo-500 rounded-full text-sm font-semibold">Section {student.section}</span>
                <span className={`px-4 py-1 rounded-full text-sm font-semibold ${student.status === 'Active' ? 'bg-green-500' : 'bg-red-500'}`}>
                  {student.status}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Content Grid */}
        <div className="p-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Column 1: Academic & Personal */}
          <div className="space-y-8">
            <section>
              <h3 className="flex items-center gap-2 text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">
                <Shield size={16} /> Academic Info
              </h3>
              <InfoBox label="Admission ID" value={student.admissionId} />
              <InfoBox label="Roll Number" value={student.rollNumber} />
              <InfoBox label="Admission Date" value={student.admissionDate} />
            </section>

            <section>
              <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Family</h3>
              <InfoBox label="Father's Name" value={student.fatherName} />
              <InfoBox label="Mother's Name" value={student.motherName} />
            </section>
          </div>

          {/* Column 2: Contact Details */}
          <div className="space-y-8">
            <section>
              <h3 className="flex items-center gap-2 text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">
                <Phone size={16} /> Contact Details
              </h3>
              <InfoBox icon={<Phone size={14}/>} label="Phone" value={student.contact} />
              <InfoBox icon={<Mail size={14}/>} label="Email" value={student.email} />
              <div className="py-3">
                <span className="text-slate-400 text-xs block mb-1">Address</span>
                <span className="text-slate-800 font-medium text-sm leading-relaxed">{student.address}</span>
              </div>
            </section>
          </div>

          {/* Column 3: Health & Transport */}
          <div className="space-y-8">
            <section className="bg-slate-50 p-5 rounded-xl border border-slate-100">
              <h3 className="text-sm font-bold text-slate-800 mb-4">Other Information</h3>
              <InfoBox icon={<Heart size={14} className="text-red-500"/>} label="Blood Group" value={student.bloodGroup} />
              <InfoBox icon={<Calendar size={14}/>} label="Date of Birth" value={student.dob} />
              <InfoBox label="Transport" value={student.transport} />
              <InfoBox label="Medical" value={student.medicalConditions} />
            </section>
          </div>

        </div>
      </div>
    </div>
  );
};

// Reusable mini-component
const InfoBox = ({ label, value, icon }) => (
  <div className="flex justify-between items-center py-3 border-b border-slate-100 last:border-0">
    <span className="text-slate-500 text-sm flex items-center gap-2">
      {icon} {label}
    </span>
    <span className="text-slate-900 font-bold text-sm">{value || "—"}</span>
  </div>
);

export default StudentDetail;