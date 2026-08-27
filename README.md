# Mechanic Shop API

A RESTful API built with Flask for managing customers, mechanics, service tickets, and inventory for a mechanic shop.

## Key Features

* Customer management
* Mechanic management
* Service ticket creation and tracking
* Assign and remove mechanics from service tickets
* Inventory management
* API documentation with Swagger
* Automated testing
* Postman collection for endpoint testing

## Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* Marshmallow
* MySQL
* PostgreSQL
* Swagger
* Unittest
* Gunicorn
* GitHub Actions

## API Documentation

Swagger documentation is available while the application is running at:

```text
http://127.0.0.1:5000/api/docs
```

## Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
flask --app flask_app run
```

The API will run at:

```text
http://127.0.0.1:5000
```

## Testing

Run the automated tests with:

```bash
python3 -m unittest discover tests
```

A Postman collection is also included for manual API testing.

## What I Learned

This project helped me strengthen my experience with REST API development, database integration, Flask application structure, API documentation, automated testing, and deployment preparation.

## Author

Created by Kimberly Gadeberg.
