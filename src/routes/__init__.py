"""Routes package - registers all blueprints"""

from flask import Flask
from .employee_routes import employee_bp
from .salary_routes import salary_bp


def register_routes(app: Flask):
    """
    Register all route blueprints with the Flask application.
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(employee_bp, url_prefix='/api')
    app.register_blueprint(salary_bp, url_prefix='/api')

