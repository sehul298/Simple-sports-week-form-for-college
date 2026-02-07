"""
Data access layer for registration storage
"""
import json
import os
from constants import REGISTRATIONS_FILE


class RegistrationRepository:
    """Handles all data storage and retrieval operations"""
    
    def __init__(self, file_path=REGISTRATIONS_FILE):
        self.file_path = file_path
    
    def load_all(self):
        """Load all registrations from JSON file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading registrations: {e}")
                return []
        return []
    
    def save_all(self, registrations):
        """Save all registrations to JSON file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(registrations, file, indent=4)
            return True
        except IOError as e:
            print(f"Error saving registrations: {e}")
            return False
    
    def find_by_enrollment(self, enrollment_no):
        """Find a registration by enrollment number"""
        registrations = self.load_all()
        for reg in registrations:
            if reg.get('enrollment_number') == enrollment_no:
                return reg
        return None
    
    def exists_by_enrollment(self, enrollment_no):
        """Check if enrollment number already exists"""
        return self.find_by_enrollment(enrollment_no) is not None
    
    def add(self, registration_data):
        """Add a new registration"""
        registrations = self.load_all()
        registrations.append(registration_data)
        return self.save_all(registrations)
    
    def count(self):
        """Get total count of registrations"""
        return len(self.load_all())
    
    def get_by_sport(self, sport):
        """Get all registrations for a specific sport"""
        registrations = self.load_all()
        return [reg for reg in registrations if reg.get('sport') == sport]
    
    def get_by_department(self, department):
        """Get all registrations for a specific department"""
        registrations = self.load_all()
        return [reg for reg in registrations if reg.get('department') == department]
