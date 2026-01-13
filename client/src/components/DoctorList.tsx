import { useState, useEffect } from 'react';
import { getDoctors, deleteDoctor } from '../services/api';
import type { Doctor } from '../types/models';
import DoctorForm from './DoctorForm';

export default function DoctorList() {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingDoctor, setEditingDoctor] = useState<Doctor | null>(null);

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

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this doctor?')) {
      try {
        await deleteDoctor(id);
        fetchDoctors();
      } catch (err: any) {
        alert('Failed to delete doctor: ' + err.message);
      }
    }
  };

  const handleEdit = (doctor: Doctor) => {
    setEditingDoctor(doctor);
    setShowForm(true);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingDoctor(null);
    fetchDoctors();
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingDoctor(null);
  };

  if (loading) return <div className="loading">Loading doctors...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="doctor-list">
      <div className="list-header">
        <h2>Doctors ({doctors.length})</h2>
        <button className="btn-add" onClick={() => setShowForm(true)}>
          + Add Doctor
        </button>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Specialization</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor) => (
            <tr key={doctor.id}>
              <td>{doctor.id}</td>
              <td>{doctor.name}</td>
              <td>{doctor.specialization || 'N/A'}</td>
              <td>
                <div className="action-buttons">
                  <button 
                    onClick={() => handleEdit(doctor)}
                    className="btn-edit"
                  >
                    Edit
                  </button>
                  <button 
                    onClick={() => handleDelete(doctor.id)}
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
        <DoctorForm
          onSuccess={handleFormSuccess}
          onCancel={handleFormCancel}
          editDoctor={editingDoctor}
        />
      )}
    </div>
  );
}