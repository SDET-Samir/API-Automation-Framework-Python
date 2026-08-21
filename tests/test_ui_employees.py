import pytest
import requests
from playwright.sync_api import Page, expect
from config import APP_URL

# Standardize our URLs based on your running port 5001 configurations
UI_URL = "http://localhost:5001/"
API_URL = "http://localhost:5001/api/v1/Employee"


def test_full_stack_employee_registration_and_deletion(page: Page):
    """
    ENTEPRISE DUAL-LAYER VALIDATION:
    1. Open the UI Web Portal and enter a new employee.
    2. Click Register and verify the UI updates.
    3. Backdoor API Check: Query the backend directly via requests to ensure data integrity.
    4. Delete the employee via the UI and verify the registry is empty.
    """
    # --- LAYER 1: FRONTEND UI INTERACTION ---
    page.goto(UI_URL)

    # Fill out input fields using robust string selectors
    page.fill("#empName", "Captain Samir")
    page.fill("#empRole", "DevOps SDET Expert")

    # Click the registration submission button
    page.click("#submitBtn")

    # Verify the UI card instantly reflects the new employee state data
    expect(page.locator("#viewName")).to_have_text("Captain Samir")
    expect(page.locator("#viewRole")).to_have_text("DevOps SDET Expert")

    # --- LAYER 2: BACKDOOR CORE API VERIFICATION ---
    # We bypass the browser and check the server memory layer directly!
    api_response = requests.get(API_URL, timeout=5)
    assert api_response.status_code == 200

    db_json = api_response.json()
    assert db_json["Employee_details"]["name"] == "Captain Samir"
    assert db_json["Employee_details"]["Role"] == "DevOps SDET Expert"

    # --- LAYER 3: UI DELETION & REGISTRY RESET ---
    # Click the delete button on the newly created row element
    page.click(".delete-btn")

    # Verify the UI falls back to showing an empty state message panel
    expect(page.locator(".empty-state")).to_be_visible()

    # Final API Backdoor Check to confirm server state is completely cleared
    final_api_response = requests.get(API_URL, timeout=5)
    assert final_api_response.json()["Employee_details"]["name"] == "None"


@pytest.mark.parametrize("invalid_name", ["S", "Sa", "  "])
def test_ui_validation_error_handling(page: Page, invalid_name):
    """
    Verify that security and naming limits on the UI block bad data
    and show correct error messages.
    """
    page.goto(UI_URL)

    # Input invalid credentials that do not match the minimum 3 character rule
    page.fill("#empName", invalid_name)
    page.fill("#empRole", "Automation Runner")
    page.click("#submitBtn")

    # Verify that the browser displays the red error alert block message panel
    error_msg = page.locator("#msg")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_have_class("message error")
    expect(error_msg).to_have_text("Invalid name")
