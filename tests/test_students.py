import requests
url = "http://localhost:5000/api/students"


def test_get_student_success():
    response = requests.get(url, timeout=5)
    data = response.json()
    assert response.status_code == 200, f"expected 200 but got {response.status_code}"
    assert data['student_details']['name'] == "master samir"


def test_post_student_invalid_name():
    payload = {"name": "ab"}
    response = requests.post(url, json=payload, timeout=5)
    assert response.status_code == 400
    assert "error" in response.json()
