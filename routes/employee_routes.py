"""Employee routes - handles employee CRUD operations"""

from flask import Blueprint, request, jsonify
from controllers import (
    create_employee_controller,
    get_employee_controller,
    get_all_employees_controller,
    update_employee_controller,
    delete_employee_controller
)

employee_bp = Blueprint('employees', __name__)


@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.get_json()
    response, status_code = create_employee_controller(data)
    return jsonify(response), status_code


@employee_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get an employee by ID"""
    response, status_code = get_employee_controller(employee_id)
    return jsonify(response), status_code


@employee_bp.route('/employees', methods=['GET'])
def get_all_employees():
    """Get all employees"""
    response, status_code = get_all_employees_controller()
    return jsonify(response), status_code


@employee_bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update an employee"""
    data = request.get_json()
    response, status_code = update_employee_controller(employee_id, data)
    return jsonify(response), status_code


@employee_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee"""
    response, status_code = delete_employee_controller(employee_id)
    if status_code == 204:
        return '', status_code
    return jsonify(response), status_code

