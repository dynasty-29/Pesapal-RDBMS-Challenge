from flask import Blueprint, jsonify, request
from ..services.rdbms_client import RDBMSClient

appointments_bp = Blueprint('appointments', __name__)

def get_client():
    """Get or create RDBMS client"""
    if not hasattr(get_client, 'client'):
        get_client.client = RDBMSClient()
    return get_client.client

@appointments_bp.route('/appointments', methods=['GET'])
def get_all_appointments():
    """Get all appointments"""
    sql = "SELECT * FROM appointments"
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'appointments': result['data'].get('rows', []),
            'count': result['data'].get('row_count', 0)
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get a specific appointment by ID"""
    sql = f"SELECT * FROM appointments WHERE id = {appointment_id}"
    result = get_client().execute_query(sql)
    
    if result['success']:
        rows = result['data'].get('rows', [])
        if rows:
            return jsonify({
                'success': True,
                'appointment': rows[0]
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Appointment not found'
            }), 404
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@appointments_bp.route('/appointments', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    data = request.get_json()
    
    required_fields = ['id', 'patient_id', 'doctor_id', 'appointment_date', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'{field} is required'
            }), 400
    
    sql = f"INSERT INTO appointments (id, patient_id, doctor_id, appointment_date, status) VALUES ({data['id']}, {data['patient_id']}, {data['doctor_id']}, '{data['appointment_date']}', '{data['status']}')"
    
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Appointment created successfully',
            'appointment': data
        }), 201
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Update an appointment status"""
    data = request.get_json()
    
    if not data.get('status'):
        return jsonify({
            'success': False,
            'error': 'Status is required'
        }), 400
    
    sql = f"UPDATE appointments SET status = '{data['status']}' WHERE id = {appointment_id}"
    
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Appointment updated successfully'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Delete an appointment"""
    sql = f"DELETE FROM appointments WHERE id = {appointment_id}"
    
    result = get_client().execute_query(sql)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Appointment deleted successfully'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500