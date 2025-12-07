import pytest
from app import create_app, db
from models import Employee


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_create_employee(client):
    """Test creating a new employee"""
    response = client.post('/api/employees', json={
        'full_name': 'John Doe',
        'job_title': 'Software Engineer',
        'country': 'India',
        'salary': 100000
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['full_name'] == 'John Doe'
    assert data['job_title'] == 'Software Engineer'
    assert data['country'] == 'India'
    assert data['salary'] == 100000
    assert 'id' in data


def test_get_employee(client):
    """Test retrieving an employee by ID"""
    # First create an employee
    create_response = client.post('/api/employees', json={
        'full_name': 'Jane Smith',
        'job_title': 'Product Manager',
        'country': 'United States',
        'salary': 120000
    })
    employee_id = create_response.get_json()['id']
    
    # Then retrieve it
    response = client.get(f'/api/employees/{employee_id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['full_name'] == 'Jane Smith'
    assert data['job_title'] == 'Product Manager'
    assert data['country'] == 'United States'
    assert data['salary'] == 120000


def test_get_all_employees(client):
    """Test retrieving all employees"""
    # Create multiple employees
    client.post('/api/employees', json={
        'full_name': 'Alice Johnson',
        'job_title': 'Designer',
        'country': 'Canada',
        'salary': 90000
    })
    client.post('/api/employees', json={
        'full_name': 'Bob Williams',
        'job_title': 'Developer',
        'country': 'India',
        'salary': 80000
    })
    
    response = client.get('/api/employees')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_update_employee(client):
    """Test updating an employee"""
    # Create an employee
    create_response = client.post('/api/employees', json={
        'full_name': 'Charlie Brown',
        'job_title': 'Analyst',
        'country': 'United States',
        'salary': 75000
    })
    employee_id = create_response.get_json()['id']
    
    # Update the employee
    response = client.put(f'/api/employees/{employee_id}', json={
        'full_name': 'Charlie Brown',
        'job_title': 'Senior Analyst',
        'country': 'United States',
        'salary': 85000
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['job_title'] == 'Senior Analyst'
    assert data['salary'] == 85000


def test_delete_employee(client):
    """Test deleting an employee"""
    # Create an employee
    create_response = client.post('/api/employees', json={
        'full_name': 'David Lee',
        'job_title': 'Manager',
        'country': 'India',
        'salary': 110000
    })
    employee_id = create_response.get_json()['id']
    
    # Delete the employee
    response = client.delete(f'/api/employees/{employee_id}')
    
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f'/api/employees/{employee_id}')
    assert get_response.status_code == 404


def test_calculate_salary_india(client):
    """Test salary calculation for India (10% TDS)"""
    # Create an employee in India
    create_response = client.post('/api/employees', json={
        'full_name': 'Raj Kumar',
        'job_title': 'Developer',
        'country': 'India',
        'salary': 100000
    })
    employee_id = create_response.get_json()['id']
    
    # Calculate salary
    response = client.get(f'/api/employees/{employee_id}/calculate-salary')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['gross_salary'] == 100000
    assert data['tds'] == 10000  # 10% of 100000
    assert data['net_salary'] == 90000  # 100000 - 10000


def test_calculate_salary_united_states(client):
    """Test salary calculation for United States (12% TDS)"""
    # Create an employee in United States
    create_response = client.post('/api/employees', json={
        'full_name': 'John Smith',
        'job_title': 'Manager',
        'country': 'United States',
        'salary': 120000
    })
    employee_id = create_response.get_json()['id']
    
    # Calculate salary
    response = client.get(f'/api/employees/{employee_id}/calculate-salary')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['gross_salary'] == 120000
    assert data['tds'] == 14400  # 12% of 120000
    assert data['net_salary'] == 105600  # 120000 - 14400


def test_calculate_salary_other_country(client):
    """Test salary calculation for other countries (no deductions)"""
    # Create an employee in Canada
    create_response = client.post('/api/employees', json={
        'full_name': 'Alice Brown',
        'job_title': 'Designer',
        'country': 'Canada',
        'salary': 90000
    })
    employee_id = create_response.get_json()['id']
    
    # Calculate salary
    response = client.get(f'/api/employees/{employee_id}/calculate-salary')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['gross_salary'] == 90000
    assert data['tds'] == 0  # No deductions
    assert data['net_salary'] == 90000  # Same as gross


def test_calculate_salary_nonexistent_employee(client):
    """Test salary calculation for non-existent employee"""
    response = client.get('/api/employees/999/calculate-salary')
    
    assert response.status_code == 404


def test_salary_metrics_by_country(client):
    """Test salary metrics (min, max, average) for a country"""
    # Create employees in India with different salaries
    client.post('/api/employees', json={
        'full_name': 'Raj Kumar',
        'job_title': 'Developer',
        'country': 'India',
        'salary': 80000
    })
    client.post('/api/employees', json={
        'full_name': 'Priya Sharma',
        'job_title': 'Manager',
        'country': 'India',
        'salary': 120000
    })
    client.post('/api/employees', json={
        'full_name': 'Amit Patel',
        'job_title': 'Designer',
        'country': 'India',
        'salary': 100000
    })
    
    response = client.get('/api/salary-metrics?country=India')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['country'] == 'India'
    assert data['minimum_salary'] == 80000
    assert data['maximum_salary'] == 120000
    assert data['average_salary'] == 100000.0  # (80000 + 120000 + 100000) / 3


def test_salary_metrics_by_country_no_employees(client):
    """Test salary metrics for country with no employees"""
    response = client.get('/api/salary-metrics?country=Germany')
    
    assert response.status_code == 404


def test_average_salary_by_job_title(client):
    """Test average salary for a specific job title"""
    # Create employees with same job title
    client.post('/api/employees', json={
        'full_name': 'John Developer',
        'job_title': 'Software Engineer',
        'country': 'United States',
        'salary': 100000
    })
    client.post('/api/employees', json={
        'full_name': 'Jane Developer',
        'job_title': 'Software Engineer',
        'country': 'India',
        'salary': 80000
    })
    client.post('/api/employees', json={
        'full_name': 'Bob Developer',
        'job_title': 'Software Engineer',
        'country': 'Canada',
        'salary': 90000
    })
    
    response = client.get('/api/salary-metrics?job_title=Software Engineer')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['job_title'] == 'Software Engineer'
    assert data['average_salary'] == 90000.0  # (100000 + 80000 + 90000) / 3


def test_average_salary_by_job_title_no_employees(client):
    """Test average salary for job title with no employees"""
    response = client.get('/api/salary-metrics?job_title=CEO')
    
    assert response.status_code == 404

