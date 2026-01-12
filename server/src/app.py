from flask import Flask, jsonify
from flask_cors import CORS

# Import blueprints
from .routes.health import health_bp
from .routes.patients import patients_bp
from .routes.doctors import doctors_bp
from .routes.appointments import appointments_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(patients_bp, url_prefix='/api')
    app.register_blueprint(doctors_bp, url_prefix='/api')
    app.register_blueprint(appointments_bp, url_prefix='/api')
    
    # Root route
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Pesapal RDBMS API is running!',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'tables': '/api/tables',
                'patients': '/api/patients',
                'doctors': '/api/doctors',
                'appointments': '/api/appointments'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')