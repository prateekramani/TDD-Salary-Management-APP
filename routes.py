from flask import Blueprint, request, jsonify
from app import db
from models import Employee

employee_bp = Blueprint('employees', __name__)


@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.get_json()
    employee = Employee(
        full_name=data['full_name'],
        job_title=data['job_title'],
        country=data['country'],
        salary=data['salary']
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201


@employee_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get an employee by ID"""
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(employee.to_dict()), 200


@employee_bp.route('/employees', methods=['GET'])
def get_all_employees():
    """Get all employees"""
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees]), 200


@employee_bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update an employee"""
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()
    employee.full_name = data['full_name']
    employee.job_title = data['job_title']
    employee.country = data['country']
    employee.salary = data['salary']
    db.session.commit()
    return jsonify(employee.to_dict()), 200


@employee_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee"""
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204

