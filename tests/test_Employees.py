import logging
import pytest
import requests
from config import APP_URL

# Configure your logging output
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@pytest.fixture
def api_url():
    # Append the canonical endpoint path directly to the base url string
    # This automatically guarantees that all test requests hit the correct endpoint route!
    return f"{APP_URL.rstrip('/')}/api/v1/Employee"


def test_employee_lifecycle(api_url):
    """
    Verify the full lifecycle of an employee record.
    """
    new_emp = {"name": "Ahmad Samir", "Role": "software QA"}
    response_post = requests.post(api_url, json=new_emp, timeout=5)
    res_json = response_post.json()

    assert response_post.status_code == 201
    assert "Employee_details" in res_json

    delete_url = f"{api_url}/Ahmad Samir"
    res_delete = requests.delete(delete_url, timeout=5)
    assert res_delete.status_code == 200

    res_verify = requests.get(api_url, timeout=5)
    # Check if the list or dictionary returns empty/clean
    assert "Ahmad Samir" not in res_verify.text
    logger.info("verified: Employee is actually gone from DB ")


@pytest.mark.parametrize("bad_name", ["A", "Ab", "", "  "])
def test_create_employee_invalid_names(api_url, bad_name):
    """
    Test security constraints for employee name validation.
    """
    payload = {"name": bad_name, "Role": "QA"}
    response = requests.post(api_url, json=payload, timeout=5)
    assert response.status_code == 400
    logger.info(f"Successfully rejected invalid name: {bad_name}")


def test_full_Employee_lifecycle(api_url):
    """
    Validation of the employee creation and immediate deletion flow.
    """
    new_emp = {"name": "Engineer Samir", "Role": "QA Expert"}
    requests.post(api_url, json=new_emp, timeout=5)
    delete_url = f"{api_url}/Engineer Samir"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 200
    assert response.json()['status'] == "success"


@pytest.mark.parametrize("null_name", ["", "...", "  "])
# FIXED: Parameter updated to match fixture
def test_create_employee_null_names(api_url, null_name):
    """
    Stress test for null or placeholder names.
    """
    payload = {"name": null_name, "Role": "QA"}
    response = requests.post(api_url, json=payload, timeout=5)
    assert response.status_code == 400
    logger.info(f"Successfully rejected invalid name: {null_name}")


def test_delete_non_existent_employee(api_url):
    """
    Validate that the system returns a 404 error when attempting to delete
    a non-existent employee record.
    """
    fake_name = "Ghost_User_99"
    delete_url = f"{api_url}/{fake_name}"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 404
    logger.info(f"correctly handled deletion of non-existent user:{fake_name}")
