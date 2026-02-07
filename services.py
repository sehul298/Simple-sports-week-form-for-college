"""
Service layer for registration business logic
"""
from datetime import datetime
from repository import RegistrationRepository
from validators import RegistrationValidator, ValidationError


class RegistrationService:
    """Handles business logic for registrations"""
    
    def __init__(self):
        self.repository = RegistrationRepository()
        self.validator = RegistrationValidator()
    
    def register_student(self, first_name, last_name, sport, department, enrollment_no):
        """
        Register a new student
        
        Returns:
            tuple: (success: bool, message: str, data: dict or None)
        """
        try:
            # Validate all inputs
            self.validator.validate_all(first_name, last_name, sport, department, enrollment_no)
            
            # Clean the data
            first_name = first_name.strip()
            last_name = last_name.strip()
            sport = sport.strip()
            department = department.strip()
            enrollment_no = enrollment_no.strip()
            
            # Check if enrollment number already exists
            if self.repository.exists_by_enrollment(enrollment_no):
                return False, "This enrollment number is already registered", None
            
            # Create registration data
            registration_data = {
                "id": self.repository.count() + 1,
                "first_name": first_name,
                "last_name": last_name,
                "sport": sport,
                "department": department,
                "enrollment_number": enrollment_no,
                "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save to repository
            if self.repository.add(registration_data):
                return True, "Registration successful", registration_data
            else:
                return False, "Failed to save registration", None
                
        except ValidationError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}", None
    
    def get_all_registrations(self):
        """Get all registrations"""
        return self.repository.load_all()
    
    def get_registration_by_enrollment(self, enrollment_no):
        """Get a specific registration by enrollment number"""
        return self.repository.find_by_enrollment(enrollment_no)
    
    def get_registrations_by_sport(self, sport):
        """Get all registrations for a specific sport"""
        return self.repository.get_by_sport(sport)
    
    def get_registrations_by_department(self, department):
        """Get all registrations for a specific department"""
        return self.repository.get_by_department(department)