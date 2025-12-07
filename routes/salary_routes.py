"""Salary routes - handles salary calculation and metrics"""

from flask import Blueprint, request, jsonify
from controllers import (
    calculate_salary_controller,
    get_salary_metrics_controller
)

salary_bp = Blueprint('salary', __name__)


@salary_bp.route('/employees/<int:employee_id>/calculate-salary', methods=['GET'])
def calculate_salary(employee_id):
    """Calculate deductions and net salary for an employee"""
    response, status_code = calculate_salary_controller(employee_id)
    return jsonify(response), status_code


@salary_bp.route('/salary-metrics', methods=['GET'])
def get_salary_metrics():
    """
    Get salary metrics by country or job title.
    
    Query parameters:
    - country: Get min, max, and average salary for a country
    - job_title: Get average salary for a job title
    """
    country = request.args.get('country')
    job_title = request.args.get('job_title')
    response, status_code = get_salary_metrics_controller(country, job_title)
    return jsonify(response), status_code

