import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000/api', // Adjust the base URL as needed
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getStudents = async () => {
    try {
        const response = await api.get('/students');
        return response.data;
    } catch (error) {
        console.error('Error fetching students:', error);
        throw error;
    }
};

export const addStudent = async (studentData) => {
    try {
        const response = await api.post('/students', studentData);
        return response.data;
    } catch (error) {
        console.error('Error adding student:', error);
        throw error;
    }
};

// Add more API functions as needed for other resources (e.g., courses, teachers)