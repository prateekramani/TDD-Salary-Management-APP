"""Controller layer - handles request/response logic and validation"""

from flask import jsonify
from typing import Dict, Optional, List, Tuple
from services import (
    create_employee_service,
    get_employee_service,
    get_all_employees_service,
    update_employee_service,
    delete_employee_service,
    calculate_net_salary,
    get_salary_metrics_by_country,
    get_average_salary_by_job_title
)


def create_employee_controller(data: Dict) -> Tuple[Dict, int]:
    """
    Controller for creating an employee.
    
    Args:
        data: Request JSON data
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    # Validate required fields
    required_fields = ['full_name', 'job_title', 'country', 'salary']
    if not data or not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    # Validate salary is positive
    if not isinstance(data['salary'], (int, float)) or data['salary'] < 0:
        return {'error': 'Salary must be a positive number'}, 400
    
    # Call service to create employee
    employee = create_employee_service(
        full_name=data['full_name'],
        job_title=data['job_title'],
        country=data['country'],
        salary=float(data['salary'])
    )
    
    return employee.to_dict(), 201


def get_employee_controller(employee_id: int) -> Tuple[Dict, int]:
    """
    Controller for getting an employee by ID.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    employee = get_employee_service(employee_id)
    if not employee:
        return {'error': 'Employee not found'}, 404
    
    return employee.to_dict(), 200


def get_all_employees_controller() -> Tuple[List[Dict], int]:
    """
    Controller for getting all employees.
    
    Returns:
        Tuple of (response_list, status_code)
    """
    employees = get_all_employees_service()
    return [emp.to_dict() for emp in employees], 200


def update_employee_controller(employee_id: int, data: Dict) -> Tuple[Dict, int]:
    """
    Controller for updating an employee.
    
    Args:
        employee_id: Employee ID
        data: Request JSON data
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    if not data:
        return {'error': 'No data provided'}, 400
    
    # Validate salary if provided
    if 'salary' in data:
        if not isinstance(data['salary'], (int, float)) or data['salary'] < 0:
            return {'error': 'Salary must be a positive number'}, 400
    
    employee = update_employee_service(employee_id, data)
    if not employee:
        return {'error': 'Employee not found'}, 404
    
    return employee.to_dict(), 200


def delete_employee_controller(employee_id: int) -> Tuple[str, int]:
    """
    Controller for deleting an employee.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        Tuple of (response_body, status_code)
    """
    success = delete_employee_service(employee_id)
    if not success:
        return {'error': 'Employee not found'}, 404
    
    return '', 204


def calculate_salary_controller(employee_id: int) -> Tuple[Dict, int]:
    """
    Controller for calculating employee salary.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    employee = get_employee_service(employee_id)
    if not employee:
        return {'error': 'Employee not found'}, 404
    
    salary_data = calculate_net_salary(employee.salary, employee.country)
    return salary_data, 200


def get_salary_metrics_controller(country: Optional[str], job_title: Optional[str]) -> Tuple[Dict, int]:
    """
    Controller for getting salary metrics.
    
    Args:
        country: Optional country name
        job_title: Optional job title
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    if country:
        metrics = get_salary_metrics_by_country(country)
        if not metrics:
            return {'error': 'No employees found for this country'}, 404
        return metrics, 200
    
    elif job_title:
        metrics = get_average_salary_by_job_title(job_title)
        if not metrics:
            return {'error': 'No employees found for this job title'}, 404
        return metrics, 200
    
    else:
        return {'error': 'Please provide either country or job_title parameter'}, 400

