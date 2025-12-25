import React from "react";
import { X, User } from "lucide-react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

const QuickViewModal = ({ student, isOpen, onClose }) => {
  if (!student) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="bg-white rounded-lg shadow-lg w-96 p-6 relative"
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0.9 }}
          >
            {/* Close Button */}
            <button
              onClick={onClose}
              className="absolute top-4 right-4 text-slate-500 hover:text-slate-800 transition"
            >
              <X size={20} />
            </button>

            {/* Modal Content */}
            <div className="text-center">
              {/* Photo Placeholder */}
              <div className="w-24 h-24 mx-auto bg-slate-100 rounded-full flex items-center justify-center mb-4">
                <User size={48} className="text-slate-400" />
              </div>

              {/* Student Info */}
              <h2 className="text-xl font-bold text-slate-800 mb-2">{student.name}</h2>
              <p className="text-sm text-slate-500 mb-4">Admission ID: {student.admissionId}</p>
              <p className="text-sm text-slate-500">Contact: {student.contact || "N/A"}</p>
            </div>

            {/* Actions */}
            <div className="mt-6 flex justify-center gap-4">
              <Link
                to={`/students/${student.id}`}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
              >
                View Full Profile
              </Link>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-gray-200 text-slate-700 rounded-lg hover:bg-gray-300 transition"
              >
                Close
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default QuickViewModal;
