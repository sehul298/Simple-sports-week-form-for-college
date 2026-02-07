"""
Validation helpers for registration data
"""
from constants import SPORTS, DEPARTMENTS, ENROLLMENT_NUMBER_LENGTH


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class RegistrationValidator:
    """Validates registration form data"""
    
    @staticmethod
    def validate_name(first_name, last_name):
        """Validate first and last names"""
        if not first_name or not first_name.strip():
            raise ValidationError("First name is required")
        
        if not last_name or not last_name.strip():
            raise ValidationError("Last name is required")
        
        if len(first_name.strip()) < 2:
            raise ValidationError("First name must be at least 2 characters")
        
        if len(last_name.strip()) < 2:
            raise ValidationError("Last name must be at least 2 characters")
        
        return True
    
    @staticmethod
    def validate_sport(sport):
        """Validate sport selection"""
        if not sport or sport.strip() not in SPORTS:
            raise ValidationError("Please select a valid sport")
        return True
    
    @staticmethod
    def validate_department(department):
        """Validate department selection"""
        if not department or department.strip() not in DEPARTMENTS:
            raise ValidationError("Please select a valid department")
        return True
    
    @staticmethod
    def validate_enrollment_number(enrollment_no):
        """Validate enrollment number"""
        if not enrollment_no or not enrollment_no.strip():
            raise ValidationError("Enrollment number is required")
        
        enrollment_no = enrollment_no.strip()
        
        if len(enrollment_no) != ENROLLMENT_NUMBER_LENGTH:
            raise ValidationError(f"Enrollment number must be exactly {ENROLLMENT_NUMBER_LENGTH} digits")
        
        if not enrollment_no.isdigit():
            raise ValidationError("Enrollment number must contain only digits")
        
        return True
    
    @classmethod
    def validate_all(cls, first_name, last_name, sport, department, enrollment_no):
        """Validate all fields at once"""
        cls.validate_name(first_name, last_name)
        cls.validate_sport(sport)
        cls.validate_department(department)
        cls.validate_enrollment_number(enrollment_no)
        return True
