# Mechanic Shop API

This project is a Flask API for a small mechanic shop. It uses the Application Factory Pattern, Flask-SQLAlchemy, Marshmallow schemas, and MySQL.

## Features

- Customer CRUD routes
- Mechanic CRUD routes
- Service ticket create and list routes
- Assign a mechanic to a service ticket
- Remove a mechanic from a service ticket

## Project Structure

```text
mechanic_shop_app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── mechanics/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   └── service_tickets/
│       ├── __init__.py
│       ├── routes.py
│       └── schemas.py
├── app.py
├── extensions.py
├── models.py
├── schemas.py
└── Mechanic Shop API.postman_collection.json
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install flask flask-sqlalchemy mysql-connector-python marshmallow
```

3. Create a MySQL database named `mechanic_shop_db`.
4. Update the database connection string in `app/__init__.py` with your MySQL credentials.
5. Run the app:

```bash
python3 app.py
```

The app runs at `http://127.0.0.1:5000`.

## Main Endpoints

### Customers

- `GET /customers`
- `POST /customers`
- `PUT /customers/<customer_id>`
- `DELETE /customers/<customer_id>`

### Mechanics

- `GET /mechanics/`
- `POST /mechanics/`
- `PUT /mechanics/<mechanic_id>`
- `DELETE /mechanics/<mechanic_id>`

### Service Tickets

- `GET /service-tickets/`
- `POST /service-tickets/`
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>`
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>`

## Testing

Postman requests for the API are included in:

`Mechanic Shop API.postman_collection.json`

Import that collection into Postman to test the routes.
