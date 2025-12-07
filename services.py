"""Business logic services"""

from typing import Dict
from constants import TDS_RATES, Country


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

