# Vendor Management System with Performance Metrics

This project implements a Vendor Management System (VMS) using Django and Django REST Framework. It facilitates vendor profile management, purchase order tracking, and vendor performance metric calculations.

## Features

### Vendor Profile Management
- Create, retrieve, update, and delete vendor profiles.
- API endpoints for managing vendor information.

### Purchase Order Tracking
- Track purchase orders with details such as PO number, order date, delivery date, etc.
- API endpoints for managing purchase orders.

### Vendor Performance Evaluation
- Calculate performance metrics: on-time delivery rate, quality rating average, average response time, and fulfillment rate.
- API endpoint to retrieve a vendor's performance metrics.

## Setup Instructions

1. **Clone Repository:**
    ```bash
    git https://github.com/LostParadise07/Vendor_Management
    cd Vendor_Management
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

3. **Run Migrations:**
    ```bash
    python manage.py makemigrations
    ```  ```

4. **Run Migrations:**
    ```bash
    python manage.py migrate
    ```


5. **Start Development Server:**
    ```bash
    python manage.py runserver
    ```


