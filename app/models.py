from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship 
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    DOB: Mapped[date]
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    loans: Mapped[List['Loan']] = db.relationship(back_populates='customer') 
    orders: Mapped[List["Order"]] = db.relationship(back_populates="customer")
    #relationship attribute
    
class Loan(db.Model):
    __tablename__ = 'loans'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(db.Date)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    
    customer: Mapped['Customer'] = db.relationship(back_populates='loans') #relationship attribute
    
class Repair(db.Model):
    __tablename__ = 'repairs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    mechanic_id: Mapped[int] = mapped_column()
    repair_date: Mapped[date] = mapped_column(db.Date)
    description: Mapped[str] = mapped_column(db.String(500), nullable=False)
    fee: Mapped[float] = mapped_column(db.Float)
    
    parts = relationship('Part', secondary = 'repair_parts', back_populates = 'repairs')
    
class Part(db.Model):
    __tablename__ = 'parts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    repairs = relationship('Repair', secondary = 'repair_parts', back_populates = 'parts')
    
class RepairPart(db.Model): #Many-to-Many relationship table between Repair and Part
    __tablename__ = 'repair_parts'
    
    repair_id: Mapped[int] = mapped_column(db.ForeignKey('repairs.id'), primary_key=True)
    part_id: Mapped[int] = mapped_column(db.ForeignKey('parts.id'), primary_key=True)  
    
class Mechanic(db.Model):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_tickets: Mapped[List['ServiceTicket']] = relationship(secondary='service_ticket_mechanics', back_populates='mechanics')
    
class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(500), nullable=False)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    
    mechanics: Mapped[List['Mechanic']] = relationship(secondary='service_ticket_mechanics', back_populates='service_tickets')
    
class ServiceTicketMechanic(db.Model):
    __tablename__ = 'service_ticket_mechanics'
    
    service_ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'), primary_key=True)
    
class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
class Item(db.Model):
    __tablename__ = "items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float(), nullable=False)
    
    order_items: Mapped[List["OrderItem"]] = db.relationship(back_populates = "item")
    
class Order(db.Model):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[date] = mapped_column(nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"), nullable=False)
    
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")
    order_items: Mapped[List["OrderItem"]] = db.relationship(back_populates="order")
    
class OrderItem(db.Model):
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(db.ForeignKey("orders.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(db.ForeignKey("items.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    
    order: Mapped["Order"] = db.relationship(back_populates="order_items")
    item: Mapped["Item"] = db.relationship(back_populates="order_items")