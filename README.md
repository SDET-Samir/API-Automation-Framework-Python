# API Automation Testing Framework
A professional automated testing suite for Student Management Systems.

## Tech Stack
- **Language:** Python
- **Library:** Requests (API interaction)
- **Framework:** Pytest (Test management)
- **Reporting:** Pytest-HTML (Visual reports)

## Scenarios Covered
1. **End-to-End Lifecycle:** Creating a student via POST and verifying data integrity via GET.
2. **Security/Negative Testing:** Validating server response (400 Bad Request) against invalid data.

## How to Generate Reports
Run the following command:
`pytest --html=report.html`
