# TDD Backend System

A Test-Driven Development based backend system for employee management with salary calculations.

## Features

1. **Employee CRUD Operations** - Create, Read, Update, Delete employees
2. **Salary Calculation** - Calculate deductions and net salary based on country
3. **Salary Metrics** - Get salary statistics by country and job title

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest
```

4. Run the application:
```bash
python app.py
```

## TDD Workflow

Following strict TDD:
1. Write failing test
2. Implement minimal code to pass
3. Refactor

## Project Structure

```
.
├── app.py              # Flask application factory
├── models.py           # Database models
├── routes.py           # API routes
├── tests/              # Test files
│   └── test_employee.py
├── requirements.txt    # Python dependencies
├── pytest.ini         # Pytest configuration
├── .gitignore         # Git ignore file
└── README.md          # This file
```

