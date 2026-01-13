import { useState, useEffect } from 'react';
import { createAppointment, updateAppointment, getPatients, getDoctors } from '../services/api';
import type { Appointment, Patient, Doctor } from '../types/models';

interface AppointmentFormProps {
  onSuccess: () => void;
  onCancel: () => void;
  editAppointment?: any | null;
}

export default function AppointmentForm({ onSuccess, onCancel, editAppointment }: AppointmentFormProps) {
  const [formData, setFormData] = useState({
    id: '',
    patient_id: '',
    doctor_id: '',
    appointment_date: '',
    status: 'Scheduled'
  });
  const [patients, setPatients] = useState<Patient[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPatientsAndDoctors();
    
    if (editAppointment) {
      setFormData({
        id: editAppointment.id.toString(),
        patient_id: editAppointment.patient_id.toString(),
        doctor_id: editAppointment.doctor_id.toString(),
        appointment_date: editAppointment.appointment_date,
        status: editAppointment.status
      });
    }
  }, [editAppointment]);

  const fetchPatientsAndDoctors = async () => {
    try {
      const [patientsRes, doctorsRes] = await Promise.all([
        getPatients(),
        getDoctors()
      ]);
      setPatients(patientsRes.data.patients || []);
      setDoctors(doctorsRes.data.doctors || []);
    } catch (err) {
      console.error('Failed to fetch patients/doctors', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editAppointment) {
        // Update existing appointment
        await updateAppointment(editAppointment.id, {
          status: formData.status
        });
      } else {
        // Create new appointment
        await createAppointment({
          id: parseInt(formData.id),
          patient_id: parseInt(formData.patient_id),
          doctor_id: parseInt(formData.doctor_id),
          appointment_date: formData.appointment_date,
          status: formData.status
        });
      }
      onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.error || `Failed to ${editAppointment ? 'update' : 'create'} appointment`);
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h3>{editAppointment ? 'Edit Appointment' : 'Add New Appointment'}</h3>
        {error && <div className="form-error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          {!editAppointment && (
            <>
              <div className="form-group">
                <label>ID *</label>
                <input
                  type="number"
                  value={formData.id}
                  onChange={(e) => setFormData({...formData, id: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Patient *</label>
                <select
                  value={formData.patient_id}
                  onChange={(e) => setFormData({...formData, patient_id: e.target.value})}
                  required
                >
                  <option value="">Select Patient</option>
                  {patients.map(patient => (
                    <option key={patient.id} value={patient.id}>
                      {patient.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Doctor *</label>
                <select
                  value={formData.doctor_id}
                  onChange={(e) => setFormData({...formData, doctor_id: e.target.value})}
                  required
                >
                  <option value="">Select Doctor</option>
                  {doctors.map(doctor => (
                    <option key={doctor.id} value={doctor.id}>
                      {doctor.name} - {doctor.specialization}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Appointment Date *</label>
                <input
                  type="date"
                  value={formData.appointment_date}
                  onChange={(e) => setFormData({...formData, appointment_date: e.target.value})}
                  required
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label>Status *</label>
            <select
              value={formData.status}
              onChange={(e) => setFormData({...formData, status: e.target.value})}
              required
            >
              <option value="Scheduled">Scheduled</option>
              <option value="Completed">Completed</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>

          <div className="form-actions">
            <button type="button" onClick={onCancel} className="btn-cancel">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="btn-submit">
              {loading ? (editAppointment ? 'Updating...' : 'Creating...') : (editAppointment ? 'Update Appointment' : 'Create Appointment')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}