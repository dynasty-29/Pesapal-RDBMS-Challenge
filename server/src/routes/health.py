from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Pesapal RDBMS API'
    }), 200

@health_bp.route('/tables', methods=['GET'])
def list_tables():
    """List all tables in the database"""
    from ..services.rdbms_client import RDBMSClient
    
    client = RDBMSClient()
    result = client.get_all_tables()
    
    if result['success']:
        return jsonify({
            'success': True,
            'tables': result['data']
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500