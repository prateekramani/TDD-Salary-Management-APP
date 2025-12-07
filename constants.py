"""Constants for the application"""

# Country names
class Country:
    INDIA = 'India'
    UNITED_STATES = 'United States'


# TDS (Tax Deducted at Source) rates by country
TDS_RATES = {
    Country.INDIA: 0.10,  # 10%
    Country.UNITED_STATES: 0.12,  # 12%
    # Other countries have 0% TDS (default)
}

