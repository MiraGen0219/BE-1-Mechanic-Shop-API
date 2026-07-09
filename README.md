# 🔧 Mechanic Shop API

A modular RESTful backend API for managing customers, mechanics, automotive service tickets, inventory, customer orders, and authentication. This project demonstrates modern Flask architecture using the **Application Factory Pattern**, **Blueprints**, **SQLAlchemy ORM**, **Marshmallow**, **JWT Authentication**, **Rate Limiting**, and **Caching**.

---

# 📌 Project Overview

The Mechanic Shop API provides a complete backend for a fictional automotive repair business.

Features include:

* Customer management
* Mechanic management
* Service ticket management
* Inventory management
* Customer orders
* Item catalog
* Authentication using JWT
* Protected routes
* Pagination
* Search functionality
* Rate limiting
* Response caching

This project was developed to practice scalable Flask application architecture, relational database design, authentication, and RESTful API development.

---

# 🛠️ Technologies Used

* Python 3.14
* Flask
* SQLAlchemy
* Marshmallow
* Flask-Limiter
* Flask-Caching
* python-jose (JWT)
* MySQL
* Postman
* Git
* GitHub

---

# 🏗️ Architecture

This project follows the **Flask Application Factory Pattern** for modular application design.

Features include:

* Application Factory Pattern
* Blueprint Architecture
* SQLAlchemy ORM
* Marshmallow Schemas
* JWT Authentication
* Route Protection
* Rate Limiting
* Response Caching
* RESTful API Design
* Modular Project Structure

---

# 📂 Project Structure

```text
BE-1-SQL/
│
├── app/
│   ├── blueprints/
│   │   ├── customers/
│   │   ├── mechanics/
│   │   ├── service_tickets/
│   │   ├── inventory/
│   │   ├── items/
│   │   ├── orders/
│   │   └── users/
│   │
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
│
├── app.py
├── config.py
├── requirements.txt
├── BE-1.postman_collection_v2.json
└── README.md
```

---

# 📦 Database Models

### Customer

* ID
* Name
* Email
* Date of Birth
* Password

### Mechanic

* ID
* Name
* Email
* Phone
* Salary

### Service Ticket

* ID
* Service Date
* Service Description
* Vehicle VIN

### Inventory

* ID
* Name
* Price

### Item

* ID
* Item Name
* Price

### Order

* ID
* Order Date
* Customer

### Order Item

* Order
* Item
* Quantity

### User

* Username
* Email
* Password

---

# 🔗 Database Relationships

### One-to-Many

* Customer → Loans
* Customer → Orders
* Order → Order Items
* Item → Order Items

### Many-to-Many

* Service Tickets ↔ Mechanics
* Service Tickets ↔ Inventory

This allows multiple mechanics to work on the same repair while multiple inventory items can be associated with each service ticket.

---

# 🚀 API Features

## Customers

* Create customer
* Retrieve customers
* Update customer
* Delete customer
* Customer Login
* Customer Authentication
* Customer Pagination

---

## Mechanics

* CRUD Operations
* Search mechanics by name
* Frequently assigned mechanics
* Ticket assignment

---

## Service Tickets

* CRUD Operations
* Assign mechanics
* Remove mechanics
* Add inventory to tickets
* Customer-specific ticket lookup
* Pagination

---

## Inventory

* Create inventory item
* Retrieve inventory
* Update inventory
* Delete inventory
* Associate inventory with service tickets

---

## Orders

* Create customer orders
* View customer orders
* Order item relationships

---

## Items

* CRUD Operations
* Order integration

---

## Authentication

* JWT Token Generation
* Protected Routes
* Token Validation
* Bearer Token Authorization

---

## Performance

* Flask-Limiter Rate Limiting
* Flask-Caching
* Paginated API Responses

---

# 🧪 API Testing

Every endpoint was tested using **Postman**.

A complete Postman collection is included:

```text
BE-1.postman_collection_v2.json
```

---

# 💡 Concepts Practiced

* Flask Application Factory Pattern
* Blueprints
* SQLAlchemy ORM
* Marshmallow Serialization
* Marshmallow Validation
* JWT Authentication
* Protected Routes
* Rate Limiting
* Response Caching
* Pagination
* Search Endpoints
* CRUD Operations
* One-to-Many Relationships
* Many-to-Many Relationships
* Junction Tables
* REST API Design
* MySQL Database Design
* Postman API Testing
* Git
* GitHub

---

# 📚 Lessons Learned

This project significantly expanded my backend development experience.

Key concepts reinforced included:

* Designing modular Flask applications using the Application Factory Pattern
* Building scalable APIs using Blueprints
* Creating secure authentication with JWT tokens
* Protecting endpoints using decorators
* Implementing rate limiting and response caching
* Designing one-to-many and many-to-many database relationships
* Managing SQLAlchemy relationships using append() and remove()
* Building advanced queries with SQLAlchemy
* Creating reusable Marshmallow schemas
* Debugging Flask routing, imports, authentication, and ORM relationships
* Testing complete REST APIs using Postman
* Managing version control using Git and GitHub

---

# 🔮 Future Improvements

Potential future enhancements include:

* Role-based authorization (Admin / Mechanic / Customer)
* Inventory quantity tracking
* Service status workflow
* Customer vehicle management
* Repair history
* Mechanic scheduling
* Email notifications
* Automated unit testing
* Integration testing
* Docker deployment
* CI/CD Pipeline

---

# 👨‍💻 Author

**Erin**

Animal Science Graduate | Full-Stack Software Engineering Student
