from flask import Blueprint, jsonify, request
from ..services.rdbms_client import RDBMSClient

patients_bp = Blueprint('patients', __name__)

def get_client():
    """Get or create RDBMS client"""
    if not hasattr(get_client, 'client'):
        get_client.client = RDBMSClient()
    return get_client.client

@patients_bp.route('/patients', methods=['GET'])
def get_all_patients():
    """Get all patients"""
    result = get_client().execute_query("SELECT * FROM patients")
    
    if result['success']:
        return jsonify({
            'success': True,
            'patients': result['data'].get('rows', []),
            'count': result['data'].get('row_count', 0)
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@patients_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient by ID"""
    sql = f"SELECT * FROM patients WHERE id = {patient_id}"
    result = get_client().execute_query(sql)
    
    if result['success']:
        rows = result['data'].get('rows', [])
        if rows:
            return jsonify({
                'success': True,
                'patient': rows[0]
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Patient not found'
            }), 404
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@patients_bp.route('/patients', methods=['POST'])
def create_patient():
    """Create a new patient"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name') or not data.get('email'):
        return jsonify({
            'success': False,
            'error': 'Name and email are required'
        }), 400
    
    # Build INSERT query
    sql = f"INSERT INTO patients (id, name, email, phone) VALUES ({data['id']}, '{data['name']}', '{data['email']}', '{data.get('phone', '')}')"
    
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Patient created successfully',
            'patient': data
        }), 201
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@patients_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update a patient"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({
            'success': False,
            'error': 'Name is required'
        }), 400
    
    # Update name
    sql_name = f"UPDATE patients SET name = '{data['name']}' WHERE id = {patient_id}"
    result = get_client().execute_query(sql_name)
    
    if not result['success']:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500
    
    # Update email if provided
    if 'email' in data and data['email']:
        sql_email = f"UPDATE patients SET email = '{data['email']}' WHERE id = {patient_id}"
        result = get_client().execute_query(sql_email)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
    
    # Update phone if provided
    if 'phone' in data:
        sql_phone = f"UPDATE patients SET phone = '{data['phone']}' WHERE id = {patient_id}"
        result = get_client().execute_query(sql_phone)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
    
    return jsonify({
        'success': True,
        'message': 'Patient updated successfully'
    }), 200

@patients_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient"""
    sql = f"DELETE FROM patients WHERE id = {patient_id}"
    
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Patient deleted successfully'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500