import os
from flask import Flask, jsonify, request, render_template

# Calculate absolute directory paths to guarantee template delivery inside Linux containers
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Initialize the Flask application instance with explicit folder paths
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Simulated in-memory database storage system
db = {
    "Employee": {"name": "samir jan", "Role": "qa"}
}


@app.route('/')
def UI_Dashboard():
    """
    Serve the frontend web application dashboard portal.
    Implements a case-insensitive template look-up to prevent container path locks.
    """
    if os.path.exists(TEMPLATE_DIR):
        for file_name in os.listdir(TEMPLATE_DIR):
            if file_name.lower() == 'index.html':
                return render_template(file_name)
    return render_template('index.html')


@app.route('/api/v1/Employee', methods=['GET', 'POST'])
def handle_Employee():
    """
    Handle data collection operations for the Employee record registry.
    """
    if request.method == 'GET':
        return jsonify({"Employee_details": db["Employee"]}), 200

    if request.method == 'POST':
        received_data = request.get_json() or {}
        name = received_data.get("name", "")
        role = received_data.get("Role", "General")

        # Clean the input name string by stripping outer whitespace and dots
        clean_name = str(name).strip(" .")

        # Enforce strict character minimum constraints
        if len(clean_name) < 3:
            return jsonify({"error": "Invalid name"}), 400

        # Save the verified clean name and role into the mock data layer
        db["Employee"] = {"name": clean_name, "Role": role}

        return jsonify({
            "message": "Employee added successfully",
            "Employee_details": db["Employee"]
        }), 201


@app.route('/api/v1/Employee/<string:name>', methods=['DELETE'])
def delete_Employee(name):
    """
    Handle deletion operations for individual employee name entries.
    """
    if db["Employee"]["name"] == name:
        db["Employee"] = {"name": "None", "Role": "None"}
        return jsonify({
            "status": "success",
            "message": f"Employee with name '{name}' has been deleted",
            "deleted_name": name
        }), 200
    else:
        return jsonify({"error": "Employee not found"}), 404


if __name__ == '__main__':
    # Force the app to listen to external port traffic bridges inside Docker
    app.run(host="0.0.0.0", port=5000, debug=False)
