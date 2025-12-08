"""Service layer - handles business logic and database operations"""

from typing import Dict, Optional, List
from sqlalchemy import func
from app import db
from models import Employee
from constants import TDS_RATES, Country


# Database operations (CRUD)
def create_employee_service(full_name: str, job_title: str, country: str, salary: float) -> Employee:
    """
    Create a new employee in the database.
    
    Args:
        full_name: Employee full name
        job_title: Job title
        country: Country
        salary: Salary amount
        
    Returns:
        Created Employee object
    """
    employee = Employee(
        full_name=full_name,
        job_title=job_title,
        country=country,
        salary=salary
    )
    db.session.add(employee)
    db.session.commit()
    return employee


def get_employee_service(employee_id: int) -> Optional[Employee]:
    """
    Get an employee by ID.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        Employee object or None if not found
    """
    return Employee.query.get(employee_id)


def get_all_employees_service() -> List[Employee]:
    """
    Get all employees.
    
    Returns:
        List of Employee objects
    """
    return Employee.query.all()


def update_employee_service(employee_id: int, data: Dict) -> Optional[Employee]:
    """
    Update an employee.
    
    Args:
        employee_id: Employee ID
        data: Dictionary with fields to update
        
    Returns:
        Updated Employee object or None if not found
    """
    employee = Employee.query.get(employee_id)
    if not employee:
        return None
    
    if 'full_name' in data:
        employee.full_name = data['full_name']
    if 'job_title' in data:
        employee.job_title = data['job_title']
    if 'country' in data:
        employee.country = data['country']
    if 'salary' in data:
        employee.salary = float(data['salary'])
    
    db.session.commit()
    return employee


def delete_employee_service(employee_id: int) -> bool:
    """
    Delete an employee.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        True if deleted, False if not found
    """
    employee = Employee.query.get(employee_id)
    if not employee:
        return False
    
    db.session.delete(employee)
    db.session.commit()
    return True


# Business logic functions
def calculate_tds(gross_salary: float, country: str) -> float:
    """
    Calculate TDS (Tax Deducted at Source) based on country.
    
    Args:
        gross_salary: The gross salary amount
        country: The country name
        
    Returns:
        The TDS amount
    """
    tds_rate = TDS_RATES.get(country, 0.0)
    return gross_salary * tds_rate


def calculate_net_salary(gross_salary: float, country: str) -> Dict[str, float]:
    """
    Calculate net salary with deductions based on country.
    
    Args:
        gross_salary: The gross salary amount
        country: The country name
        
    Returns:
        Dictionary containing gross_salary, tds, and net_salary
    """
    tds = calculate_tds(gross_salary, country)
    net_salary = gross_salary - tds
    
    return {
        'gross_salary': gross_salary,
        'tds': round(tds, 2),
        'net_salary': round(net_salary, 2)
    }


def get_salary_metrics_by_country(country: str) -> Optional[Dict[str, float]]:
    """
    Get salary metrics (min, max, average) for a specific country.
    
    Args:
        country: The country name
        
    Returns:
        Dictionary with country, minimum_salary, maximum_salary, and average_salary
        Returns None if no employees found for the country
    """
    result = db.session.query(
        func.min(Employee.salary).label('min_salary'),
        func.max(Employee.salary).label('max_salary'),
        func.avg(Employee.salary).label('avg_salary')
    ).filter(Employee.country == country).first()
    
    if not result or result.min_salary is None:
        return None
    
    return {
        'country': country,
        'minimum_salary': float(result.min_salary),
        'maximum_salary': float(result.max_salary),
        'average_salary': round(float(result.avg_salary), 2)
    }


def get_average_salary_by_job_title(job_title: str) -> Optional[Dict[str, float]]:
    """
    Get average salary for a specific job title.
    
    Args:
        job_title: The job title
        
    Returns:
        Dictionary with job_title and average_salary
        Returns None if no employees found for the job title
    """
    result = db.session.query(
        func.avg(Employee.salary).label('avg_salary')
    ).filter(Employee.job_title == job_title).first()
    
    if not result or result.avg_salary is None:
        return None
    
    return {
        'job_title': job_title,
        'average_salary': round(float(result.avg_salary), 2)
    }

