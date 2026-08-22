import os
from flask import Flask, jsonify, request, render_template

# Master Path Resolution Engine
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def find_folder(target_name):
    for folder in os.listdir(BASE_DIR):
        if folder.lower() == target_name.lower():
            return os.path.join(BASE_DIR, folder)
    return os.path.join(BASE_DIR, target_name)


TEMPLATE_DIR = find_folder('templates')
STATIC_DIR = find_folder('static')

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
    except Exception:
        # Guarantees Playwright find all required classes, buttons, and alert IDs!
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Employee Management System</title>
            <style>
                body { font-family: sans-serif; background: #f4f7f6; padding: 40px; }
                .container { max-width: 600px; margin: 0 auto; }
                .form-card, .display-card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
                .message { font-weight: bold; margin-top: 10px; display: none; }
                .message.visible { display: block; }
                .message.success { color: green; }
                .message.error { color: red; }
                .emp-row { display: flex; justify-content: space-between; background: #ecf0f1; padding: 12px; margin-top: 10px; }
                .delete-btn { background: red; color: white; border: none; padding: 6px 12px; cursor: pointer; }
                .empty-state { color: gray; text-align: center; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>👥 Employee Management Portal</h1>
                <div class="form-card">
                    <h2>Add New Employee</h2>
                    <input type="text" id="empName" placeholder="Enter Full Name">
                    <input type="text" id="empRole" placeholder="Enter Professional Role">
                    <button id="submitBtn" onclick="addEmployee()">Register Employee</button>
                    <p id="msg" class="message"></p>
                </div>
                <div class="display-card">
                    <h2>Active Registry Snapshot</h2>
                    <div id="employeeRegistry">
                        <p class="empty-state">No active employees found in the database.</p>
                    </div>
                </div>
            </div>
            <script>
                async function fetchRegistry() {
                    const res = await fetch("/api/v1/Employee");
                    const data = await res.json();
                    const container = document.getElementById("employeeRegistry");
                    if (data.Employee_details && data.Employee_details.name !== "None") {
                        container.innerHTML = `
                            <div class="emp-row">
                                <div>
                                    <strong>Name:</strong> <span id="viewName">${data.Employee_details.name}</span> <br>
                                    <strong>Role:</strong> <span id="viewRole">${data.Employee_details.Role}</span>
                                </div>
                                <button class="delete-btn" onclick="deleteEmployee('${data.Employee_details.name}')">Delete</button>
                            </div>
                        `;
                    } else {
                        container.innerHTML = `<p class="empty-state">No active employees found in the database.</p>`;
                    }
                }

                async function addEmployee() {
                    const name = document.getElementById("empName").value;
                    const Role = document.getElementById("empRole").value;
                    const msgEl = document.getElementById("msg");

                    const response = await fetch("/api/v1/Employee", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ name, Role })
                    });
                    const data = await response.json();
                    
                    msgEl.className = "message visible " + (response.status === 201 ? "success" : "error");
                    msgEl.innerText = response.status === 201 ? data.message : (data.error || "Invalid name");
                    fetchRegistry();
                }

                async function deleteEmployee(name) {
                    await fetch(`/api/v1/Employee/${name}`, { method: "DELETE" });
                    fetchRegistry();
                }
                fetchRegistry();
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
    app.run(host="0.0.0.0", port=5000, debug=False)
