# 🔧 Mechanic Shop API

A RESTful backend API for managing customers, mechanics, and automotive service tickets. This project demonstrates modern Flask application architecture using the **Application Factory Pattern**, **Blueprints**, **SQLAlchemy ORM**, and **Marshmallow** for serialization and validation.

---

## 📌 Project Overview

The Mechanic Shop API allows users to:

- Manage customer records
- Manage mechanic records
- Create and retrieve service tickets
- Assign mechanics to service tickets
- Remove mechanics from service tickets

This project was built to practice scalable Flask architecture, relational database design, and RESTful API development.

---

## 🛠️ Technologies Used

- Python 3.14
- Flask
- SQLAlchemy
- Marshmallow
- MySQL
- Postman
- Git & GitHub

---

## 🏗️ Architecture

This project utilizes the **Flask Application Factory Pattern** to create a modular and scalable application.

Features include:

- Application Factory Pattern
- Blueprint architecture
- Modular route organization
- SQLAlchemy ORM
- Marshmallow schemas
- RESTful API design

---

## 📂 Project Structure

```
BE-1-SQL/
│
├── app/
│   ├── blueprints/
│   │   ├── customers/
│   │   ├── mechanics/
│   │   └── service_tickets/
│   │
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
│
├── app.py
├── config.py
├── requirements.txt
├── BE-1.postman_collection.json
└── README.md
```

---

## 📦 Models

### Customer

- id
- name
- email
- date of birth
- password

### Mechanic

- id
- name
- email
- phone
- salary

### Service Ticket

- id
- service date
- service description
- vehicle VIN

---

## 🔗 Database Relationships

### One-to-Many

- Customer → Loans

### Many-to-Many

- Service Tickets ↔ Mechanics

A mechanic may work on multiple service tickets.

A service ticket may have multiple mechanics assigned.

---

## 🚀 API Endpoints

### Customers

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/customers/` | Create customer |
| GET | `/customers/` | Retrieve all customers |
| GET | `/customers/<id>` | Retrieve customer by ID |
| PUT | `/customers/<id>` | Update customer |
| DELETE | `/customers/<id>` | Delete customer |

---

### Mechanics

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/mechanics/` | Create mechanic |
| GET | `/mechanics/` | Retrieve all mechanics |
| PUT | `/mechanics/<id>` | Update mechanic |
| DELETE | `/mechanics/<id>` | Delete mechanic |

---

### Service Tickets

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/service-tickets/` | Create service ticket |
| GET | `/service-tickets/` | Retrieve all service tickets |
| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign mechanic |
| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove mechanic |

---

## 🧪 API Testing

All endpoints were tested using **Postman**.

A complete Postman collection is included with the repository:

```
BE-1.postman_collection.json
```

---

## 💡 Concepts Practiced

- Flask Application Factory Pattern
- Blueprints
- REST API Design
- SQLAlchemy ORM
- Marshmallow Validation
- Serialization / Deserialization
- One-to-Many Relationships
- Many-to-Many Relationships
- Relationship Tables
- CRUD Operations
- Postman API Testing
- Git Version Control
- GitHub Repository Management

---

## 📚 Lessons Learned

This project provided valuable experience building a modular Flask backend application.

Some of the key lessons included:

- Organizing larger Flask projects using the Application Factory Pattern
- Registering and managing multiple Blueprints
- Designing one-to-many and many-to-many database relationships
- Using SQLAlchemy relationship methods such as `append()` and `remove()`
- Serializing SQLAlchemy models with Marshmallow
- Debugging import paths, blueprint registration, and relationship configuration
- Testing and validating REST endpoints using Postman
- Managing source control with Git and GitHub

Working through debugging and resolving runtime errors significantly strengthened my understanding of Flask application structure and backend development workflows.

---

## 🔮 Future Improvements

Potential future enhancements include:

- Authentication and authorization
- JWT-based login
- Mechanic scheduling
- Customer vehicle records
- Repair history tracking
- Service status updates
- Search and filtering endpoints
- Pagination
- Docker deployment
- Automated unit and integration testing

---

## 👨‍💻 Author

**Erin**

Animal Science Graduate | Full-Stack Software Engineering Student

Interested in:

- Python Development
- SQL Databases
- REST APIs
- React
- Wildlife Conservation Data Systems
- Population Management Software

---
