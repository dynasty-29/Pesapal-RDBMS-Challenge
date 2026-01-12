export interface Patient {
  id: number;
  name: string;
  email: string;
  phone?: string;
}

export interface Doctor {
  id: number;
  name: string;
  specialization?: string;
}

export interface Appointment {
  id: number;
  patient_id: number;
  doctor_id: number;
  appointment_date: string;
  status: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}