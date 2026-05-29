import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Automatically attach Token to every request if it exists in localStorage
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

// ------------------------------------
// AUTHENTICATION APIs
// ------------------------------------
export const loginUser = async (username, password) => {
    const response = await api.post('auth/login/', { username, password });
    return response.data; 
};

export const registerUser = async (userData) => {
    const response = await api.post('auth/register/', userData);
    return response.data;
};

// ------------------------------------
// SCHOLARSHIP PROGRAMS APIs
// ------------------------------------
export const getPrograms = async () => {
    const response = await api.get('programs/');
    return response.data;
};

// ------------------------------------
// SCHOLARSHIP APPLICATIONS APIs
// ------------------------------------
export const getApplications = async () => {
    const response = await api.get('applications/');
    return response.data;
};

export const createApplication = async (applicationData) => {
    const response = await api.post('applications/', applicationData);
    return response.data;
};

export const updateApplication = async (id, updatedData) => {
    const response = await api.patch(`applications/${id}/`, updatedData);
    return response.data;
};
// ... existing imports and functions ...

// NEW: Fetch all registered students
export const getStudents = async () => {
    const response = await api.get('students/');
    return response.data;
};

// NEW: Delete a student and their login credentials
export const deleteStudent = async (id) => {
    const response = await api.delete(`students/${id}/`);
    return response.data;
};

export default api;