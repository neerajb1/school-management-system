import React from 'react';
import { X } from 'lucide-react';

const AddStudentModal = ({ show, onClose, onSave, newStudent, setNewStudent }) => {
  if (!show) return null;

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 space-y-4 w-96 shadow-xl">
        <div className="flex justify-between items-center border-b pb-2">
          <h2 className="text-lg font-bold text-gray-800">Add New Student</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X size={20} />
          </button>
        </div>
        
        <div className="space-y-3">
          <input
            type="text"
            placeholder="Admission ID"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            value={newStudent.admissionId || ''}
            onChange={(e) => setNewStudent({ ...newStudent, admissionId: e.target.value })}
          />
          <input
            type="text"
            placeholder="Name"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            value={newStudent.name || ''}
            onChange={(e) => setNewStudent({ ...newStudent, name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Father's Name"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            value={newStudent.fatherName || ''}
            onChange={(e) => setNewStudent({ ...newStudent, fatherName: e.target.value })}
          />
          <input
            type="text"
            placeholder="Grade"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            value={newStudent.grade || ''}
            onChange={(e) => setNewStudent({ ...newStudent, grade: e.target.value })}
          />
        </div>

        <div className="flex gap-3 pt-2">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            onClick={onSave}
            className="flex-1 px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600"
          >
            Save Student
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddStudentModal;