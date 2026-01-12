import { useState, useEffect } from 'react';
import { getDoctors } from '../services/api';
import type { Doctor } from '../types/models';

export default function DoctorList() {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDoctors();
  }, []);

  const fetchDoctors = async () => {
    try {
      const response = await getDoctors();
      setDoctors(response.data.doctors || []);
      setLoading(false);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch doctors');
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading doctors...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="doctor-list">
      <h2>Doctors ({doctors.length})</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Specialization</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor) => (
            <tr key={doctor.id}>
              <td>{doctor.id}</td>
              <td>{doctor.name}</td>
              <td>{doctor.specialization || 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}