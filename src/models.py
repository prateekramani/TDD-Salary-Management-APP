from app import db


class Employee(db.Model):
    """Employee model"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Convert employee to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'job_title': self.job_title,
            'country': self.country,
            'salary': self.salary
        }

