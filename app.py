from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    """Employee model"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Convert employee to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'job_title': self.job_title,
            'country': self.country,
            'salary': self.salary
        }


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    @app.route('/api/employees', methods=['POST'])
    def create_employee():
        """Create a new employee"""
        pass
    
    @app.route('/api/employees/<int:employee_id>', methods=['GET'])
    def get_employee(employee_id):
        """Get an employee by ID"""
        pass
    
    @app.route('/api/employees', methods=['GET'])
    def get_all_employees():
        """Get all employees"""
        pass
    
    @app.route('/api/employees/<int:employee_id>', methods=['PUT'])
    def update_employee(employee_id):
        """Update an employee"""
        pass
    
    @app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        """Delete an employee"""
        pass
    
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
