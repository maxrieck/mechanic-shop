# Mechanic Shop ORM Practice

This project is a practice implementation of a mechanic shop management system using Flask, SQLAlchemy, and Marshmallow. It demonstrates basic CRUD operations for customers, mechanics, and service tickets, with a modular blueprint structure.

## Features
- Customer management (create, read, update, delete)
- Mechanic management (create, read, update, delete)
- Service ticket management (assign/remove mechanics, view tickets)
- RESTful API endpoints
- Data validation with Marshmallow

## Setup
1. Clone the repository or copy the project files.
2. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure your database settings in `config.py`.
5. Run the application:
   ```
   python app.py
   ```

## API Endpoints
- `/customers/` - Manage customers
- `/mechanics/` - Manage mechanics
- `/service_tickets/` - Manage service tickets

## Folder Structure
- `app/` - Main application package
  - `blueprints/` - Contains modular blueprints for each resource
  - `models.py` - SQLAlchemy models
  - `extensions.py` - Flask extensions
- `config.py` - Configuration settings
- `app.py` - Application entry point

## License
This project is for educational purposes.
