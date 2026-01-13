import { useState, useEffect } from 'react';
import { getAppointments, deleteAppointment } from '../services/api';
import AppointmentForm from './AppointmentForm';

export default function AppointmentList() {
  const [appointments, setAppointments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingAppointment, setEditingAppointment] = useState<any | null>(null);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const response = await getAppointments();
      console.log('API Response:', response.data);
      setAppointments(response.data.appointments || []);
      setLoading(false);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch appointments');
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this appointment?')) {
      try {
        await deleteAppointment(id);
        fetchAppointments();
      } catch (err: any) {
        alert('Failed to delete appointment: ' + err.message);
      }
    }
  };

  const handleEdit = (appointment: any) => {
    setEditingAppointment(appointment);
    setShowForm(true);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingAppointment(null);
    fetchAppointments();
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingAppointment(null);
  };

  if (loading) return <div className="loading">Loading appointments...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="appointment-list">
      <div className="list-header">
        <h2>Appointments ({appointments.length})</h2>
        <button className="btn-add" onClick={() => setShowForm(true)}>
          + Add Appointment
        </button>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Patient Name</th>
            <th>Doctor Name</th>
            <th>Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {appointments.map((appointment) => (
            <tr key={appointment.id}>
              <td>{appointment.id}</td>
              <td>{appointment.patient_name}</td>
              <td>{appointment.doctor_name}</td>
              <td>{appointment.appointment_date}</td>
              <td>
                <span className={`status status-${appointment.status.toLowerCase()}`}>
                  {appointment.status}
                </span>
              </td>
              <td>
                <div className="action-buttons">
                  <button 
                    onClick={() => handleEdit(appointment)}
                    className="btn-edit"
                  >
                    Edit
                  </button>
                  <button 
                    onClick={() => handleDelete(appointment.id)}
                    className="btn-delete"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {showForm && (
        <AppointmentForm
          onSuccess={handleFormSuccess}
          onCancel={handleFormCancel}
          editAppointment={editingAppointment}
        />
      )}
    </div>
  );
}