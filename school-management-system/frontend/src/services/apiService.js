import axios from 'axios';

const apiService = axios.create({
    baseURL: 'http://localhost:5001/api', // Backend API URL
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: false, // Include credentials in requests
});

export default apiService;
