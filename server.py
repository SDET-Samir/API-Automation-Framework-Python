from flask import Flask, jsonify, request

app = Flask(__name__)

db = {
    "student": {"name": "samir jan", "major": "qa"}
}


@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'GET':
        return jsonify({"student_details": db["student"]}), 200

    if request.method == 'POST':
        received_data = request.get_json()
        name = received_data.get("name", "")
        major = received_data.get("major", "General")
        if len(name) < 3:
            return jsonify({"error": "Invalid name. Must be at least 3 chars."}), 400

        db["student"] = {"name": name, "major": major}

        return jsonify({
            "message": "Student added successfully",
            "student_details": db["student"]
        }), 201


@app.route('/api/students/<string:name>', methods=['DELETE'])
def delete_student(name):
    if db["student"]["name"] == name:
        db["student"] = {"name": "None", "major": "None"}
        return jsonify({
            "status": "success",
            "message": f"Student with name '{name}' has been deleted",
            "deleted_name": name
        }), 200
    else:
        return jsonify({"error": "Student not found"}), 404


if __name__ == '__main__':
    app.run(port=5000)
