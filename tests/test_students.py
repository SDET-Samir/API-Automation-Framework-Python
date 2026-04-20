import pytest
import requests

# این یک ابزار جادویی در پایتست است


@pytest.fixture
def base_url():
    return "http://localhost:5000/api/students"


def test_get_student_success(base_url):  # آدرس را از فیکسچر می‌گیرد
    response = requests.get(base_url, timeout=5)
    assert response.status_code == 200
    assert response.json()['student_details']['name'] == "samir jan"


def test_post_student_invalid_name(base_url):
    payload = {"name": "ab"}
    response = requests.post(base_url, json=payload, timeout=5)
    assert response.status_code == 400
