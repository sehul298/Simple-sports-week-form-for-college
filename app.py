"""
Refactored Flask application for Sports Registration System
"""
from flask import Flask, render_template, request
from constants import SPORTS, DEPARTMENTS
from services import RegistrationService

app = Flask(__name__)

# Initialize service
registration_service = RegistrationService()


@app.route("/")
def index():
    """Render the registration form"""
    return render_template("index.html", sports=SPORTS, departments=DEPARTMENTS)


@app.route("/register", methods=["POST"])
def register():
    """Handle registration form submission"""
    # Get form data
    first_name = request.form.get("First Name", "")
    last_name = request.form.get("Last Name", "")
    sport = request.form.get("Sport", "")
    department = request.form.get("Department", "")
    enrollment_no = request.form.get("Enrollment Number", "")
    
    # Process registration through service layer
    success, message, data = registration_service.register_student(
        first_name, last_name, sport, department, enrollment_no
    )
    
    if not success:
        return render_template("error.html", message=message)
    
    return render_template("success.html", 
                         first_name=data['first_name'], 
                         last_name=data['last_name'],
                         sport=data['sport'],
                         department=data['department'],
                         enrollment_no=data['enrollment_number'])


@app.route("/registrations")
def view_registrations():
    """View all registrations"""
    registrations = registration_service.get_all_registrations()
    return render_template("registrations.html", registrations=registrations)

@app.route("/search")
def search():
    """Search registrations"""
    sport = request.args.get("sport")
    department = request.args.get("department")
    
    if sport:
        registrations = registration_service.get_registrations_by_sport(sport)
        filter_type = f"Sport: {sport}"
    elif department:
        registrations = registration_service.get_registrations_by_department(department)
        filter_type = f"Department: {department}"
    else:
        registrations = registration_service.get_all_registrations()
        filter_type = "All Registrations"
    
    return render_template("registrations.html", 
                         registrations=registrations,
                         filter_type=filter_type)


if __name__ == "__main__":
    app.run(debug=True)
