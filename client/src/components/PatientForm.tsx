import { useState, useEffect } from 'react';
import { createPatient, updatePatient } from '../services/api';
import type { Patient } from '../types/models';

interface PatientFormProps {
  onSuccess: () => void;
  onCancel: () => void;
  editPatient?: Patient | null;
}

export default function PatientForm({ onSuccess, onCancel, editPatient }: PatientFormProps) {
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    email: '',
    phone: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (editPatient) {
      setFormData({
        id: editPatient.id.toString(),
        name: editPatient.name,
        email: editPatient.email,
        phone: editPatient.phone || ''
      });
    }
  }, [editPatient]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editPatient) {
        // Update existing patient
        await updatePatient(editPatient.id, {
          name: formData.name,
          email: formData.email,
          phone: formData.phone
        });
      } else {
        // Create new patient
        await createPatient({
          id: parseInt(formData.id),
          name: formData.name,
          email: formData.email,
          phone: formData.phone
        });
      }
      onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.error || `Failed to ${editPatient ? 'update' : 'create'} patient`);
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h3>{editPatient ? 'Edit Patient' : 'Add New Patient'}</h3>
        {error && <div className="form-error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          {!editPatient && (
            <div className="form-group">
              <label>ID *</label>
              <input
                type="number"
                value={formData.id}
                onChange={(e) => setFormData({...formData, id: e.target.value})}
                required
              />
            </div>
          )}

          <div className="form-group">
            <label>Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Phone</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
            />
          </div>

          <div className="form-actions">
            <button type="button" onClick={onCancel} className="btn-cancel">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="btn-submit">
              {loading ? (editPatient ? 'Updating...' : 'Creating...') : (editPatient ? 'Update Patient' : 'Create Patient')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}