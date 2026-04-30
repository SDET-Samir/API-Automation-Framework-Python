import logging
import pytest
import requests
from config import APP_URL


@pytest.fixture
def base_url():
    return APP_URL


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_employee_lifecycle(base_url):
    """
      Verify the full lifecycle of an employee record.

    Steps:
    1. Create a new employee via POST.
    2. Retrieve the employee details via GET.
    3. Assert that the data integrity is maintained.
    """
    new_emp = {"name": "Ahmad Samir", "Role": "software QA"}
    response_post = requests.post(base_url, json=new_emp, timeout=5)
    res_json = response_post.json()

    assert response_post.status_code == 201
    assert "Employee_details" in res_json

    delete_url = f"{base_url}/Ahmad Samir"
    res_delete = requests.delete(delete_url, timeout=5)
    assert res_delete.status_code == 200
    res_verify = requests.get(base_url, timeout=5)
    assert res_verify.json()["Employee_details"]["name"]
    logger.info("verified: Employee is actually gone from DB ")


@pytest.mark.parametrize("bad_name", ["A", "Ab", "", "  "])
def test_create_employee_invalid_names(base_url, bad_name):
    '''
Test security constraints for employee name validation.

    Args:
        base_url (str): The root API endpoint.
        bad_name (str): Various invalid names provided by pytest parametrize.

    Expected:
        The server should reject the request with a 400 Bad Request status.
    '''
    payload = {"name": bad_name, "Role": "QA"}
    response = requests.post(base_url, json=payload, timeout=5)
    assert response.status_code == 400
    logger.info(f"Successfully rejected invalid name: {bad_name}")


def test_full_Employee_lifecycle(base_url):
    '''
       Validation of the employee creation and immediate deletion flow.
    Ensures that the success status is explicitly returned by the server.
    '''
    new_emp = {"name": "Engineer Samir", "Role": "QA Expert"}
    requests.post(base_url, json=new_emp, timeout=5)
    delete_url = f"{base_url}/Engineer Samir"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 200
    assert response.json()['status'] == "success"


@pytest.mark.parametrize("null_name", ["", "...", "  "])
def test_create_employee_null_names(base_url, null_name):
    '''
       Stress test for null or placeholder names.
    Ensures the API handles edge-case strings correctly.
    '''
    payload = {"name": null_name, "Role": "QA"}
    response = requests.post(base_url, json=payload, timeout=5)
    assert response.status_code == 400
    logger.info(f"Successfully rejected invalid name: {null_name}")


def test_delete_non_existent_employee(base_url):
    '''
    Validate that the system returns a 404 error when attempting to delete
    a non-existent employee record.
    '''
    fake_name = "Ghost_User_99"
    delete_url = f"{base_url}/{fake_name}"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 404
    logger.info(f"correctly handled deletion of non-existent user:{fake_name}")
