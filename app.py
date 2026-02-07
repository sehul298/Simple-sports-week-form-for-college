from flask import Flask, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)

SPORTS = [
    "Football",
    "Cricket",
    "Chess",
    "Kabaddi",
    "Volleyball",
    "Badminton"
]

DEPARTMENTS = [
    "Information Technology (IT)",
    "Computer Engineering (CE)",
    "Biomedical Engineering (BM)",
    "Electrical Engineering (ECE)",
    "Civil Engineering (CVE)",
    "Electronics & Communication (EC)",
    "Instrumentation & Control Engineering (IC)"
]

# JSON file path
REGISTRATIONS_FILE = "registrations.json"

def load_registrations():
    """Load all registrations from JSON file"""
    if os.path.exists(REGISTRATIONS_FILE):
        with open(REGISTRATIONS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_registrations(registrations):
    """Save all registrations to JSON file"""
    with open(REGISTRATIONS_FILE, 'w') as file:
        json.dump(registrations, file, indent=4)

def check_enrollment_exists(enrollment_no):
    """Check if enrollment number already exists"""
    registrations = load_registrations()
    for reg in registrations:
        if reg['enrollment_number'] == enrollment_no:
            return True
    return False

def add_registration(first_name, last_name, sport, department, enrollment_no):
    """Add a new registration"""
    # Check if enrollment number already exists
    if check_enrollment_exists(enrollment_no):
        return False
    
    # Load existing registrations
    registrations = load_registrations()
    
    # Create new registration
    new_registration = {
        "id": len(registrations) + 1,
        "first_name": first_name,
        "last_name": last_name,
        "sport": sport,
        "department": department,
        "enrollment_number": enrollment_no,
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add to list and save
    registrations.append(new_registration)
    save_registrations(registrations)
    return True

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS, departments=DEPARTMENTS)

@app.route("/register", methods=["POST"])
def register():
    # Get form data
    first_name = request.form.get("First Name", "").strip()
    last_name = request.form.get("Last Name", "").strip()
    sport = request.form.get("Sport", "").strip()
    department = request.form.get("Department", "").strip()
    enrollment_no = request.form.get("Enrollment Number", "").strip()
    
    # Validation
    if not first_name or not last_name:
        return render_template("error.html", message="Please enter both first and last name")
    
    if not sport or sport not in SPORTS:
        return render_template("error.html", message="Please select a valid sport")
    
    if not department or department not in DEPARTMENTS:
        return render_template("error.html", message="Please select a valid department")
    
    if not enrollment_no or len(enrollment_no) != 12 or not enrollment_no.isdigit():
        return render_template("error.html", message="Enrollment number must be exactly 10 digits")
    
    # Save the registration
    success = add_registration(first_name, last_name, sport, department, enrollment_no)
    
    if not success:
        return render_template("error.html", message="This enrollment number is already registered")
    
    return render_template("success.html", 
                         first_name=first_name, 
                         last_name=last_name,
                         sport=sport,
                         department=department,
                         enrollment_no=enrollment_no)

@app.route("/registrations")
def view_registrations():
    registrations = load_registrations()
    return render_template("registrations.html", registrations=registrations)

if __name__ == "__main__":

    app.run()
