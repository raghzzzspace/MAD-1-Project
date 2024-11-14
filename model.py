from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum


# Initializing the database
db = SQLAlchemy()

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    role = db.Column(Enum('customer', name='role'), default='customer')

class Professional(db.Model):
    professional_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    service_name = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    document = db.Column(db.LargeBinary)  # To store PDF as binary data
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    role = db.Column(Enum('professional', name='role'), default='professional')
    status = db.Column(db.String(10), nullable=True)  # Status of the professional

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Services(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    service_name=db.Column(db.String(256),nullable=False)
    base_price=db.Column(db.Integer,nullable=False)

class Service_Req(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    service_name=db.Column(db.String(256),nullable=False)
    assign_prof=db.Column(db.Integer)
    req_date=db.Column(db.Date,nullable=False)

class Service_History(db.Model):
    id=db.Column(db.Integer)
    service_id=db.Column(db.Integer, primary_key=True)
    service_name=db.Column(db.String(256),nullable=False)
    professional_name=db.Column(db.String(256),nullable=False)
    email = db.Column(db.String(255), nullable=False)
    status=db.Column(db.String(16),nullable=False)    

class Today_Services(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    customer_name=db.Column(db.String(256),nullable=False)
    email = db.Column(db.String(255), nullable=False)
    location=db.Column(db.Integer,nullable=True)
    professional_id=db.Column(db.Integer,nullable=False)
    customer_id=db.Column(db.Integer,nullable=False)

class Closed_Services(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    customer_name=db.Column(db.String(256),nullable=False)
    email = db.Column(db.String(255), nullable=False)
    location=db.Column(db.Integer,nullable=False)
    date=db.Column(db.Date,nullable=False)
    rating=db.Column(db.Integer)
    pid=db.Column(db.Integer,nullable=False)
    cid=db.Column(db.Integer,nullable=False)

class Services_status(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    customer_name=db.Column(db.String(256),nullable=False)
    email = db.Column(db.String(255), nullable=False)
    location=db.Column(db.String,nullable=True)
    status=db.Column(db.String(16),nullable=False)
