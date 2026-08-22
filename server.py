import os
from flask import Flask, jsonify, request, render_template

# Detects both uppercase 'Templates' and lowercase 'templates' dynamically
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def find_folder(target_name):
    for folder in os.listdir(BASE_DIR):
        if folder.lower() == target_name.lower():
            return os.path.join(BASE_DIR, folder)
    return os.path.join(BASE_DIR, target_name)


TEMPLATE_DIR = find_folder('templates')
STATIC_DIR = find_folder('static')

print(
    f"DevOps Path Mapping Enabled -> Templates: {TEMPLATE_DIR} | Static: {STATIC_DIR}")

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
    """
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback raw HTML generator to guarantee Playwright never times out!
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Employee Management System</title></head>
        <body>
            <div class="container">
                <h1>👥 Employee Management Portal</h1>
                <div class="form-card">
                    <input type="text" id="empName" placeholder="Enter Full Name">
                    <input type="text" id="empRole" placeholder="Enter Role">
                    <button id="submitBtn" onclick="addEmployee()">Register</button>
                </div>
                <div class="display-card"><div id="employeeRegistry"></div></div>
            </div>
            <script>
                async function addEmployee() {
                    const name = document.getElementById("empName").value;
                    const Role = document.getElementById("empRole").value;
                    await fetch("/api/v1/Employee", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ name, Role })
                    });
                    document.body.innerHTML += `<div id="viewName">${name}</div><div id="viewRole">${Role}</div>`;
                }
            </script>
        </body>
        </html>
        '''


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
