# Transport Management System

## Overview

This is a Django-based Transport Management System designed to manage user registration, authentication, and transport schedules for an educational institution. The system features:

- User registration with role-based access (students, staff, faculty)
- Automatic generation of user cards with QR codes
- Transport schedule management
- Admin views for user management

## Features

### User Management
- Registration with email, ID number, and role-specific fields
- Login/logout functionality
- Profile viewing with generated QR code
- Role-based access control

### Card System
- Automatic card generation upon registration
- QR code generation containing user ID
- Card viewing interface

### Transport Management
- Schedule viewing interface
- Schedule updates tracking

### Admin Features
- View all registered users
- Staff/faculty information listing

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (recommended) or SQLite
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shaikat020/CTMS.git
   cd transport-management-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the project root
   - Include necessary settings like database credentials, secret key, etc.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

### User Registration
1. Navigate to `/register`
2. Fill in the registration form with all required details
3. Upon successful registration, a card with QR code will be automatically generated

### User Login
1. Navigate to `/login`
2. Enter your email and password
3. Upon successful login, you'll be redirected to your profile

### Profile and Card
- View your profile at `/profile`
- Access your generated card at `/generate-card`

### Transport Schedule
- View the latest schedule at `/schedule`

### Admin Features
- Access the admin panel at `/admin/`
- View all registered users at `/admin/users`

## Dependencies

The system relies on the following key packages:

- Django (5.1.5)
- Pillow (for image processing)
- qrcode (for QR code generation)
- psycopg2 (for PostgreSQL connection)
- python-dotenv (for environment variables)

## Configuration

Ensure the following settings are properly configured in your Django settings:

- Database connection (PostgreSQL recommended)
- Static files configuration
- Email settings (if using email features)
- Authentication backends

## Troubleshooting

If you encounter issues:

1. Check that all dependencies are installed correctly
2. Verify database connection settings
3. Ensure migrations have been run
4. Check the Django server logs for error messages

## Contributing

**Md Tahsin Azad Shaikat**

CSE Undergraduate | Backend Developer | Robotics & IoT Enthusiast

🔗 [LinkedIn](https://www.linkedin.com/in/mdtahsinazad020/)

🐙 [GitHub](https://github.com/shaikat020)

**Dipa Barua**

CSE Undergraduate | Frontend Developer | UI/UX Designer

🔗 [LinkedIn](https://www.linkedin.com/in/dipa-barua-387071303/)

🐙 [GitHub](https://github.com/dipabarua22)

**Md Rakibul Hassan**

CSE Undergraduate | Backend Developer | Robotics & IoT Enthusiast

🔗 [LinkedIn](https://www.linkedin.com/in/md-rakibul-hassan-507b00308)

🐙 [GitHub](https://github.com/RR0327)

**Md Ifthakhar Alam Shams**

CSE Undergraduate | Database Developer | Prompt Engineering

🔗 [LinkedIn](https://www.linkedin.com/in/md-ifthakhar-alam-shams-85080a29a/)

🐙 [GitHub](https://github.com/suns11)

**SAIMA SHARMIN**

CSE Undergraduate | UI/UX Designer | Manual Testing

🔗 [LinkedIn](https://www.linkedin.com/in/saima-sharmin-865148325/)

🐙 [GitHub](https://github.com/SaimaShama)

## License

This project is open source and available under the MIT License.
