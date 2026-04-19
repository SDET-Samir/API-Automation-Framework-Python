from flask import Flask, jsonify, request

app = Flask(__name__)

# --- مسیر GET و POST (روی یک آدرس مشترک) ---


@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'GET':
        # پاسخ برای تست get_student_success
        return jsonify({
            "student_details": {"name": "samir jan", "major": "qa"}
        }), 200

    if request.method == 'POST':
        # منطق برای تست post_student_invalid_name
        received_data = request.get_json()
        name = received_data.get("name", "")
        if len(name) < 3:
            return jsonify({"error": "Invalid name. Must be at least 3 chars."}), 400
        return jsonify({"message": "Student added successfully"}), 201

# --- مسیر DELETE (با پارامتر نام در آدرس) ---


@app.route('/api/students/<string:name>', methods=['DELETE'])
def delete_student(name):
    return jsonify({
        "status": "success",
        "message": f"Student with name '{name}' has been deleted",
        "deleted_name": name
    }), 200


if __name__ == '__main__':
    app.run(port=5000)
