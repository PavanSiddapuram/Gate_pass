# Gate Pass Management System

The Gate Pass Management System is a web application developed using Django to manage the issuance and approval of gate passes for materials in a university setting. This system supports multi-level approvals, activity tracking, and includes different views for employees, department heads, and security heads.

## Features

- **User Roles**: Supports three roles - Employee, Department Head, and Security Head.
- **Authentication**: Secure login and logout functionality.
- **Dashboard**: Role-based dashboards showing relevant information.
- **Forms**: Separate forms for returnable and non-returnable gate passes.
- **Approval Workflow**: Multi-level approval process involving department heads and security heads.
- **Activity Tracking**: View activity logs and status of gate passes.
- **Forgot Password**: Password recovery functionality.

## Prerequisites

- Python 3.x
- Django 3.x or later
- MySQL or SQLite (default)

## Installation

1. **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd manage_system
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database**:

    Update the `DATABASES` setting in `manage_system/settings.py` to match your database configuration.

5. **Run migrations**:

    ```bash
    python manage.py migrate
    ```

6. **Create initial users**:

    ```bash
    python manage.py create_initial_users
    ```

7. **Collect static files**:

    ```bash
    python manage.py collectstatic
    ```

8. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

## Usage

1. **Access the application**:

    Open your web browser and go to `http://127.0.0.1:8000/`.

2. **Login**:

    Use the predefined usernames and passwords to log in:
    
    - Employee: `employee1` / `employee123`
    - Department Head: `depthead1` / `depthead123`
    - Security Head: `security1` / `security123`

3. **Dashboard**:

    The dashboard will vary based on the user role:
    
    - Employees can view their submitted gate passes.
    - Department Heads can approve/reject gate passes from their department.
    - Security Heads can approve/reject gate passes approved by department heads.

4. **Forms**:

    - Employees can fill out returnable and non-returnable gate pass forms.

5. **Approvals**:

    - Department Heads and Security Heads can approve or reject gate passes from their respective approval views.

6. **Activity Tracking**:

    - Users can view the activity logs and status of gate passes.

## Project Structure

- `manage_system/`: The Django project directory.
- `mypass/`: The application directory containing models, views, forms, and templates.
- `static/`: Directory for static files.
- `templates/`: Directory for HTML templates.

## Adding New Users

To add new users, use the Django admin interface or extend the `create_initial_users` command.

## Customization

To customize the application, you can modify the views, templates, and static files as needed.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any changes or suggestions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or support, please contact the project maintainer at pavansiddapuram9441@gmail.com.
