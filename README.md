# Healthcare Management System API

A RESTful backend application built with Django REST Framework and PostgreSQL to manage patient records, doctor information, user authentication, and patient-doctor assignments.

The application uses JSON Web Token (JWT) authentication to secure API endpoints and provides a homepage for navigating the available API resources.

**Author:** Harshita Yadav

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Sample API Requests](#sample-api-requests)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

---

## Project Overview

The Healthcare Management System API provides a backend for managing healthcare-related information through RESTful endpoints.

Users can register and log in, manage their patient records, maintain doctor information, and associate doctors with patients. Authentication and permission checks help ensure that protected resources are accessed only by authorized users.

The project also includes a homepage that provides an overview of the application and links to its main API sections.

## Features

- User registration and login.
- JWT-based authentication using access and refresh tokens.
- Patient record management with CRUD operations.
- Doctor record management with CRUD operations.
- Patient-doctor assignment and mapping management.
- Ownership-based access control for patient records.
- Validation for patient age and doctor email addresses.
- Prevention of duplicate patient-doctor assignments.
- PostgreSQL database integration.
- Django Admin interface for application administration.
- Homepage for navigating available API resources.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django REST Framework | REST API development |
| PostgreSQL | Relational database |
| Simple JWT | Token-based authentication |
| django-environ | Environment variable management |
| Psycopg | PostgreSQL database adapter |
| Postman | API testing |
| Git | Version control |

## Project Structure

```text
Whatbytes-main/
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── patients/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
└── mappings/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── tests.py
```

*Note: This structure describes the main application files. Additional files and migrations may be present in the actual project.*

## Prerequisites

Before running the project, ensure that the following software is installed:

- Python 3.10 or later.
- PostgreSQL.
- Git, if cloning the repository.
- Postman for API testing.
- Visual Studio Code or another code editor.

## Installation and Setup

### 1. Clone or extract the project

If using Git:

```bash
git clone <repository-url>
cd Whatbytes-main
```

Alternatively, extract the project ZIP and open the `Whatbytes-main` folder in your terminal.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is unavailable, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If dependency installation fails, check the Python version and the error reported by pip before changing package versions.

## Environment Configuration

Create a `.env` file in the project root, alongside `manage.py`.

Add the following configuration:

```env
SECRET_KEY=replace-with-a-generated-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5555
```

Replace the example secret key and database password with your own values.

The database port above is `5555`, matching the local PostgreSQL server configuration used during development. If your server uses a different port, enter the actual port.

### Generating a Django secret key

Run the following command in your terminal:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the generated value into `SECRET_KEY` in your `.env` file.

Do not commit `.env` to version control or share your actual credentials.

## Database Configuration

### 1. Create the database

Open pgAdmin, connect to your PostgreSQL server, and create a database named:

```text
healthcare_db
```

You can also create it using SQL:

```sql
CREATE DATABASE healthcare_db;
```

Run this command only if the database does not already exist.

### 2. Verify the connection settings

Ensure that the following values in `.env` match your PostgreSQL installation:

- Database name
- Database username
- Database password
- Host
- Port

### 3. Apply migrations

Run:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

The migration commands create or update the database schema required by the application. Review any generated migrations before applying them, particularly if the database already contains important data.

### 4. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the Django Admin account.

## Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

The application will normally be available at:

- **Homepage:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/
- **Authentication API:** http://127.0.0.1:8000/api/auth/
- **Patient API:** http://127.0.0.1:8000/api/patients/
- **Doctor API:** http://127.0.0.1:8000/api/doctors/
- **Patient-doctor mappings:** http://127.0.0.1:8000/api/mappings/

The homepage provides navigation to the application's main resources. Individual endpoints may require authentication or specific HTTP methods.

## API Documentation

The API accepts and returns JSON for its data operations.

Use Postman to test requests. For protected endpoints, include a valid JWT access token in the request headers.

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/auth/register/` | Register a user | Not required |
| POST | `/api/auth/login/` | Log in and obtain JWT tokens | Not required |

### Patient Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/patients/` | List the authenticated user's patients |
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/<id>/` | Retrieve a patient |
| PUT | `/api/patients/<id>/` | Update a patient |
| PATCH | `/api/patients/<id>/` | Partially update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |

Patient records are associated with the authenticated user. The API restricts patient access based on ownership.

### Doctor Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/doctors/` | List doctors |
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor |
| PATCH | `/api/doctors/<id>/` | Partially update a doctor |
| DELETE | `/api/doctors/<id>/` | Delete a doctor |

Doctor management endpoints require authentication. Review the configured permissions before exposing doctor records in a production environment.

### Patient-Doctor Mapping

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/mappings/` | List mappings for the authenticated user's patients |
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/<patient_id>/` | Retrieve mappings for a patient |
| DELETE | `/api/mappings/<mapping_id>/` | Remove a patient-doctor assignment |

The mapping detail route currently uses the same integer URL pattern for patient-specific retrieval and mapping deletion. Check the view implementation when choosing the identifier: GET interprets it as a patient ID, whereas DELETE interprets it as a mapping ID.

## Authentication

The application uses JSON Web Tokens (JWT) to protect API endpoints.

### Step 1: Register a user

Send a `POST` request to:

```text
http://127.0.0.1:8000/api/auth/register/
```

Example JSON body:

```json
{
  "name": "Harshita Yadav",
  "email": "harshita@example.com",
  "password": "ChooseAStrongPassword123!"
}
```

Use your own email and a strong password when testing.

### Step 2: Log in

Send a `POST` request to:

```text
http://127.0.0.1:8000/api/auth/login/
```

Example JSON body:

```json
{
  "email": "harshita@example.com",
  "password": "ChooseAStrongPassword123!"
}
```

A successful login returns a response containing an access token and a refresh token.

### Step 3: Access protected endpoints

In Postman, open the Authorization tab and select **Bearer Token**.

Paste the access token returned by the login endpoint.

Alternatively, add this HTTP header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Use the access token for authenticated API requests. Obtain a new access token when the current one expires.

## Sample API Requests

### Create a patient

**Method:** POST

**URL:**

```text
http://127.0.0.1:8000/api/patients/
```

**Headers:**

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**JSON body:**

```json
{
  "name": "Aarav Sharma",
  "age": 35,
  "gender": "Male",
  "phone": "9876543210",
  "address": "New Delhi, India"
}
```

The API associates the patient with the authenticated user.

### Create a doctor

**Method:** POST

**URL:**

```text
http://127.0.0.1:8000/api/doctors/
```

**JSON body:**

```json
{
  "name": "Dr. Priya Sharma",
  "specialization": "Cardiology",
  "phone": "9876543211",
  "email": "priya.sharma@example.com"
}
```

Include the Bearer token and JSON content type in the request headers.

### Assign a doctor to a patient

**Method:** POST

**URL:**

```text
http://127.0.0.1:8000/api/mappings/
```

**JSON body:**

```json
{
  "patient": 1,
  "doctor": 1
}
```

Replace `1` with the actual patient and doctor IDs returned by your API.

The patient must belong to the authenticated user, and the same doctor cannot be assigned to the same patient more than once.

### List patients

**Method:** GET

```text
http://127.0.0.1:8000/api/patients/
```

Include the Bearer token in the request headers.

### List doctors

**Method:** GET

```text
http://127.0.0.1:8000/api/doctors/
```

Include the Bearer token in the request headers.

## Error Handling

The API uses standard HTTP status codes to indicate the result of a request.

| Status code | Meaning |
|---|---|
| 200 OK | Request completed successfully |
| 201 Created | Resource created successfully |
| 204 No Content | Request succeeded without a response body |
| 400 Bad Request | Invalid input or validation failure |
| 401 Unauthorized | Missing or invalid authentication credentials |
| 403 Forbidden | Access denied |
| 404 Not Found | Resource or URL not found |
| 405 Method Not Allowed | HTTP method is not supported by the endpoint |
| 500 Internal Server Error | Unexpected server-side error |

The exact status code depends on the endpoint and the outcome of the request.

## Testing

Run the project's automated tests:

```bash
python manage.py test
```

Check Django configuration:

```bash
python manage.py check
```

Check whether model changes require new migrations:

```bash
python manage.py makemigrations --check --dry-run
```

Use Postman to test registration, login, patient CRUD operations, doctor CRUD operations, mapping creation, and permission restrictions.

Record test results only after the relevant tests have been executed successfully.

## Security Considerations

- Keep `SECRET_KEY` and database credentials in environment variables.
- Never commit `.env` to version control.
- Use `DEBUG=False` in production.
- Configure `ALLOWED_HOSTS` for the deployment environment.
- Use HTTPS in production.
- Protect patient information with appropriate authorization and access controls.
- Do not expose access tokens or passwords in logs.
- Apply migrations carefully and maintain regular database backups.
- Review Django and dependency security updates before deployment.

The built-in Django development server is intended for local development and testing, not production hosting.

## Troubleshooting

### Homepage returns 404

Verify that `config/urls.py` contains a root route:

```python
path('', home, name='home')
```

Ensure the `home` view is imported correctly and restart the server if necessary.

### PostgreSQL connection fails

Check that PostgreSQL is running and the database exists. Confirm that the host, port, username, password, and database name in `.env` match your local PostgreSQL installation.

### API returns 401 Unauthorized

Log in again and provide the access token in the `Authorization` header using the Bearer scheme.

### API returns 403 Forbidden

Verify that the authenticated user has permission to access the requested resource.

### API returns 404 Not Found

Check the URL path in `config/urls.py` and the relevant app's `urls.py`. Confirm that the requested resource exists and that you are using the correct identifier.

### Dependencies fail to install

Activate the project's virtual environment and install the packages listed in `requirements.txt`. Review the full installation error before changing package versions.

## Author

**Harshita Yadav**
