from flask import Blueprint, jsonify, request
from ..services.rdbms_client import RDBMSClient

doctors_bp = Blueprint('doctors', __name__)

def get_client():
    """Get or create RDBMS client"""
    if not hasattr(get_client, 'client'):
        get_client.client = RDBMSClient()
    return get_client.client

@doctors_bp.route('/doctors', methods=['GET'])
def get_all_doctors():
    """Get all doctors"""
    result = get_client().execute_query("SELECT * FROM doctors")
    
    if result['success']:
        return jsonify({
            'success': True,
            'doctors': result['data'].get('rows', []),
            'count': result['data'].get('row_count', 0)
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@doctors_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get a specific doctor by ID"""
    sql = f"SELECT * FROM doctors WHERE id = {doctor_id}"
    result = get_client().execute_query(sql)
    
    if result['success']:
        rows = result['data'].get('rows', [])
        if rows:
            return jsonify({
                'success': True,
                'doctor': rows[0]
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Doctor not found'
            }), 404
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@doctors_bp.route('/doctors', methods=['POST'])
def create_doctor():
    """Create a new doctor"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({
            'success': False,
            'error': 'Name is required'
        }), 400
    
    sql = f"INSERT INTO doctors (id, name, specialization) VALUES ({data['id']}, '{data['name']}', '{data.get('specialization', '')}')"
    
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Doctor created successfully',
            'doctor': data
        }), 201
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@doctors_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Update a doctor"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({
            'success': False,
            'error': 'Name is required'
        }), 400
    
    # Update name
    sql_name = f"UPDATE doctors SET name = '{data['name']}' WHERE id = {doctor_id}"
    result = get_client().execute_query(sql_name)
    
    if not result['success']:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500
    
    # Update specialization if provided
    if 'specialization' in data:
        sql_spec = f"UPDATE doctors SET specialization = '{data.get('specialization', '')}' WHERE id = {doctor_id}"
        result = get_client().execute_query(sql_spec)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
    
    return jsonify({
        'success': True,
        'message': 'Doctor updated successfully'
    }), 200
    
@doctors_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Delete a doctor"""
    sql = f"DELETE FROM doctors WHERE id = {doctor_id}"
    
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Doctor deleted successfully'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500