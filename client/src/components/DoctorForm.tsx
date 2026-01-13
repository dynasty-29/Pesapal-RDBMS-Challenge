import { useState, useEffect } from 'react';
import { createDoctor, updateDoctor } from '../services/api';
import type { Doctor } from '../types/models';

interface DoctorFormProps {
  onSuccess: () => void;
  onCancel: () => void;
  editDoctor?: Doctor | null;
}

export default function DoctorForm({ onSuccess, onCancel, editDoctor }: DoctorFormProps) {
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    specialization: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (editDoctor) {
      setFormData({
        id: editDoctor.id.toString(),
        name: editDoctor.name,
        specialization: editDoctor.specialization || ''
      });
    }
  }, [editDoctor]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editDoctor) {
        // Update existing doctor
        await updateDoctor(editDoctor.id, {
          name: formData.name,
          specialization: formData.specialization
        });
      } else {
        // Create new doctor
        await createDoctor({
          id: parseInt(formData.id),
          name: formData.name,
          specialization: formData.specialization
        });
      }
      onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.error || `Failed to ${editDoctor ? 'update' : 'create'} doctor`);
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h3>{editDoctor ? 'Edit Doctor' : 'Add New Doctor'}</h3>
        {error && <div className="form-error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          {!editDoctor && (
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
            <label>Specialization</label>
            <input
              type="text"
              value={formData.specialization}
              onChange={(e) => setFormData({...formData, specialization: e.target.value})}
              placeholder="e.g., Cardiology, Pediatrics"
            />
          </div>

          <div className="form-actions">
            <button type="button" onClick={onCancel} className="btn-cancel">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="btn-submit">
              {loading ? (editDoctor ? 'Updating...' : 'Creating...') : (editDoctor ? 'Update Doctor' : 'Create Doctor')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}