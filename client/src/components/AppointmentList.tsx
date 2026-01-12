import { useState, useEffect } from 'react';
import { getAppointments } from '../services/api';

export default function AppointmentList() {
  const [appointments, setAppointments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

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

  if (loading) return <div className="loading">Loading appointments...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="appointment-list">
      <h2>Appointments ({appointments.length})</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Patient Name</th>
            <th>Doctor Name</th>
            <th>Date</th>
            <th>Status</th>
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
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}