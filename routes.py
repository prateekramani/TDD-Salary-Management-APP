from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app import db
from models import Employee
from services import calculate_net_salary

employee_bp = Blueprint('employees', __name__)


@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['full_name', 'job_title', 'country', 'salary']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate salary is positive
    if not isinstance(data['salary'], (int, float)) or data['salary'] < 0:
        return jsonify({'error': 'Salary must be a positive number'}), 400
    
    employee = Employee(
        full_name=data['full_name'],
        job_title=data['job_title'],
        country=data['country'],
        salary=float(data['salary'])
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
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate salary if provided
    if 'salary' in data:
        if not isinstance(data['salary'], (int, float)) or data['salary'] < 0:
            return jsonify({'error': 'Salary must be a positive number'}), 400
        employee.salary = float(data['salary'])
    
    if 'full_name' in data:
        employee.full_name = data['full_name']
    if 'job_title' in data:
        employee.job_title = data['job_title']
    if 'country' in data:
        employee.country = data['country']
    
    db.session.commit()
    return jsonify(employee.to_dict()), 200


@employee_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee"""
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204


@employee_bp.route('/employees/<int:employee_id>/calculate-salary', methods=['GET'])
def calculate_salary(employee_id):
    """
    Calculate deductions and net salary for an employee.
    
    Returns 404 if employee doesn't exist (handled by get_or_404).
    """
    employee = Employee.query.get_or_404(employee_id)
    
    salary_data = calculate_net_salary(employee.salary, employee.country)
    
    return jsonify(salary_data), 200


@employee_bp.route('/salary-metrics', methods=['GET'])
def get_salary_metrics():
    """
    Get salary metrics by country or job title.
    
    Query parameters:
    - country: Get min, max, and average salary for a country
    - job_title: Get average salary for a job title
    
    Returns 404 if no employees found.
    """
    country = request.args.get('country')
    job_title = request.args.get('job_title')
    
    if country:
        # Get salary metrics by country
        result = db.session.query(
            func.min(Employee.salary).label('min_salary'),
            func.max(Employee.salary).label('max_salary'),
            func.avg(Employee.salary).label('avg_salary')
        ).filter(Employee.country == country).first()
        
        if not result or result.min_salary is None:
            return jsonify({'error': 'No employees found for this country'}), 404
        
        return jsonify({
            'country': country,
            'minimum_salary': float(result.min_salary),
            'maximum_salary': float(result.max_salary),
            'average_salary': round(float(result.avg_salary), 2)
        }), 200
    
    elif job_title:
        # Get average salary by job title
        result = db.session.query(
            func.avg(Employee.salary).label('avg_salary')
        ).filter(Employee.job_title == job_title).first()
        
        if not result or result.avg_salary is None:
            return jsonify({'error': 'No employees found for this job title'}), 404
        
        return jsonify({
            'job_title': job_title,
            'average_salary': round(float(result.avg_salary), 2)
        }), 200
    
    else:
        return jsonify({'error': 'Please provide either country or job_title parameter'}), 400

