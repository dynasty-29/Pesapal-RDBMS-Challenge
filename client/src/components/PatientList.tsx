import { useState, useEffect } from 'react';
import { getPatients, deletePatient } from '../services/api';
import type { Patient } from '../types/models';
import PatientForm from './PatientForm';

export default function PatientList() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await getPatients();
      setPatients(response.data.patients || []);
      setLoading(false);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch patients');
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this patient?')) {
      try {
        await deletePatient(id);
        fetchPatients();
      } catch (err: any) {
        alert('Failed to delete patient: ' + err.message);
      }
    }
  };

  const handleEdit = (patient: Patient) => {
    setEditingPatient(patient);
    setShowForm(true);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingPatient(null);
    fetchPatients();
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingPatient(null);
  };

  if (loading) return <div className="loading">Loading patients...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="patient-list">
      <div className="list-header">
        <h2>Patients ({patients.length})</h2>
        <button className="btn-add" onClick={() => setShowForm(true)}>
          + Add Patient
        </button>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id}>
              <td>{patient.id}</td>
              <td>{patient.name}</td>
              <td>{patient.email}</td>
              <td>{patient.phone || 'N/A'}</td>
              <td>
                <div className="action-buttons">
                  <button 
                    onClick={() => handleEdit(patient)}
                    className="btn-edit"
                  >
                    Edit
                  </button>
                  <button 
                    onClick={() => handleDelete(patient.id)}
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
        <PatientForm
          onSuccess={handleFormSuccess}
          onCancel={handleFormCancel}
          editPatient={editingPatient}
        />
      )}
    </div>
  );
}