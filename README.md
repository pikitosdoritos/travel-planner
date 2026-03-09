# Travel Planner API

This project is a small backend application for managing travel projects and places to visit.
It was built as a test task using **FastAPI** and **SQLite**.

The idea is simple: a user can create a travel project and add places they want to visit.
Places are fetched and validated using the **Art Institute of Chicago API**.

The system allows users to add notes, mark places as visited, and automatically complete the project when all places are visited.

---

# Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* HTTPX
* Swagger (FastAPI auto documentation)

---

# Project Structure

```
travel-planner
│
├── app
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   │
│   ├── routers
│   │   ├── projects.py
│   │   └── project_places.py
│   │
│   └── services
│       └── artic_api.py
│
├── requirements.txt
└── README.md
```

---

# How to Run the Project

### 1. Clone the repository

```
git clone <repository_link>
cd travel-planner
```

### 2. Create virtual environment

```
python -m venv venv
```

Activate it:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the server

```
uvicorn app.main:app --reload
```

---

# API Documentation

After running the server, open:

```
http://127.0.0.1:8000/docs
```

FastAPI automatically generates Swagger documentation where all endpoints can be tested.

---

# Main Features

### Travel Projects

* Create travel project
* Update project information
* Delete project
* List all projects
* Get a single project

Project fields:

* name
* description
* start_date

---

### Project Places

* Add place to project
* Get all places in a project
* Get single place
* Update notes
* Mark place as visited

Each place stores:

* external_id
* title
* api_link
* notes
* visited status

---

# Business Rules

The system enforces several rules:

* A project can contain **maximum 10 places**
* The same place cannot be added twice to the same project
* A project **cannot be deleted if any place is already visited**
* When **all places are visited**, the project is automatically marked as completed

---

# External API

Places are validated using the **Art Institute of Chicago API**.

Example endpoint used:

```
https://api.artic.edu/api/v1/artworks/{id}
```

The API is used to verify that a place exists and to retrieve its basic information.

---

# Example Workflow

1. Create a travel project
2. Add places from the Art Institute API
3. Add notes to places
4. Mark places as visited
5. When all places are visited → the project becomes completed

---

# Notes

This project focuses mainly on backend logic, API design, and database interaction.

The frontend is not included because the API can be fully tested using Swagger UI or Postman.
