from flask import Flask, jsonify, request

app = Flask(__name__)

db = {
    "Employee": {"name": "samir jan", "Role": "qa"}
}


@app.route('/api/v1/Employee', methods=['GET', 'POST'])
def handle_Employee():
    if request.method == 'GET':
        return jsonify({"Employee_details": db["Employee"]}), 200

    if request.method == 'POST':
        received_data = request.get_json()
        name = received_data.get("name", "")
        Role = received_data.get("Role", "General")
        if len(name) < 3 or not name.strip(" . "):
            return jsonify({"error": "Invalid name"}), 400

        db["Employee"] = {"name": name, "Role": Role}

        return jsonify({
            "message": "Employee added successfully",
            "Employee_details": db["Employee"]
        }), 201


@app.route('/api/v1/Employee/<string:name>', methods=['DELETE'])
def delete_Employee(name):
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
