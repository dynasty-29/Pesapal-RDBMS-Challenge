import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Patients
export const getPatients = () => api.get('/patients');
export const getPatient = (id: number) => api.get(`/patients/${id}`);
export const createPatient = (data: any) => api.post('/patients', data);
export const updatePatient = (id: number, data: any) => api.put(`/patients/${id}`, data);
export const deletePatient = (id: number) => api.delete(`/patients/${id}`);

// Doctors
export const getDoctors = () => api.get('/doctors');
export const getDoctor = (id: number) => api.get(`/doctors/${id}`);

// Appointments
export const getAppointments = () => api.get('/appointments');
export const createAppointment = (data: any) => api.post('/appointments', data);
export const updateAppointment = (id: number, data: any) => api.put(`/appointments/${id}`, data);
export const deleteAppointment = (id: number) => api.delete(`/appointments/${id}`);

export default api;