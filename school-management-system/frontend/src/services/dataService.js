import axios from "axios";

let configData = null;

const loadConfig = async () => {
    if (!configData) {
        const response = await fetch("/api/config.json");
        if (!response.ok) throw new Error("Failed to load config.json");
        configData = await response.json();
    }
    return configData;
};

// --- Configuration Data ---
export const getGrades = async () => {
    const config = await loadConfig();
    return config.grades;
};

export const getSections = async () => {
    const config = await loadConfig();
    return config.sections;
};

export const getSubjects = () => configData.subjects;

// --- Data Fetching ---
export const getDashboardData = () => fetch("/api/dashboard.json").then((res) => res.json());
export const getExams = () => fetch("/api/exams.json").then((res) => res.json());
export const getResults = () => fetch("/api/results.json").then((res) => res.json());

export const fetchStudents = async () => {
    const response = await fetch("/api/students.json");
    if (!response.ok) throw new Error("Failed to fetch students.");
    return await response.json();
};

export const fetchNotices = async () => {
    const response = await fetch("/api/notices.json");
    if (!response.ok) throw new Error("Failed to fetch notices.");
    return await response.json();
};