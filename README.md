# Household Services

**Household Services** is a web application designed to connect customers with professionals who offer household services such as AC repairs, cleaning, salon services, and electrical work. The platform allows users to view available service packages, book appointments, and track service history. 

---

## Features

- **User Dashboard**: Separate dashboards for customers and professionals with tailored functionalities.
- **Service Categories**: Browse and explore various service categories such as AC Repair, Salon, Cleaning, Electrician, etc.
- **Service Packages**: View detailed service packages with ratings, prices, and descriptions.
- **Service History**: Customers can view and manage their service history, including ongoing and completed services.
- **Login & Registration**: Separate authentication for customers and professionals with secure login and registration forms.
- **Admin Panel**: Admins can manage users, services, and the platform as a whole.

---

## Technologies Used

- **Flask**: A micro web framework for building web applications in Python.
- **SQLite**: Lightweight relational database used for storing user and service data.
- **SQLAlchemy**: Object-Relational Mapper (ORM) for interacting with the database.
- **Flask-Migrate**: Extension to handle database migrations.
- **Bootstrap 5**: Frontend framework for responsive, mobile-first design.
- **JavaScript**: For dynamic interactions, such as displaying service packages.

---

## Requirements

To run this project, you'll need the following:

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Jinja2
- Gunicorn (for production deployment) (to be decided soon)

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/Household_Services.git
    cd Household_Services
    ```

2. **Create and activate a virtual environment**:
    - **macOS/Linux**:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - **Windows**:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **Run the development server**:
    ```bash
    flask run
    ```

    The app will be available at `http://127.0.0.1:7000`.

---

## Usage

### For Customers:
- **Sign Up / Log In**: Register and log in to access the customer dashboard.
- **Browse Services**: View different service categories (AC Repair, Salon, Cleaning, etc.) and explore service packages.
- **Book Appointments**: Select a package and book an appointment with a professional.
- **Service History**: Keep track of your service history, including active and completed bookings.

### For Professionals:
- **Sign Up / Log In**: Register as a professional and log in to access the professional dashboard.
- **Manage Requests**: View and accept service requests from customers.
- **Service History**: Manage and track the services you have completed.

### For Admins:
- **Admin Dashboard**: Manage the platform by viewing and editing user data, service categories, and service packages.

---

## Project Structure


### Detailed Breakdown:

- **`HOUSEHOLD_SERVICES/`**: Contains the core functionality of the app, including routes, models, templates, and static files.
  - **`__init__.py`**: Initializes the Flask app and its extensions like SQLAlchemy, Migrate, etc.
  - **`models.py`**: Contains the ORM models for users, services, and other entities.
  - **`app.py`**: Defines the URL routes for customer, professional, and admin views, as well as other necessary views.
  - **`templates/`**: Stores HTML templates for rendering pages.
  - **`static/`**: Contains static files like CSS, JavaScript, and images, organized in respective subdirectories.

  - **`migrations/`**: Contains the migration files for database schema changes.
  - **`versions/`**: Folder where Alembic migration scripts are stored. This is automatically created when running `flask db migrate`.

  - **`requirements.txt`**: Lists the Python dependencies required for the project (e.g., Flask, SQLAlchemy, etc.).
  
  - **`run.py`**: The entry point to run the Flask app. It imports the app from `app/__init__.py` and runs it.
  
  - **`README.md`**: The project documentation, which provides an overview of the app, installation instructions, usage, and contribution guidelines.


---

### Why this Structure is Improved:
1. **Separation of Concerns**: The structure organizes code based on responsibilities. The `app` directory holds the core app logic, templates, and static files, while the `migrations` directory handles database migrations. This makes it easier to maintain and scale.
2. **Modularity**: The related code is grouped together, allowing for easier navigation and extensibility.
3. **Scalability**: The structure is designed to easily scale with additional features, like adding new routes, forms, and utility functions.
4. **Maintainability**: With clear separations between models, views, templates, and static files, this structure is more maintainable as your app grows.

---

## Database Setup

- **SQLite**: The app uses SQLite for simplicity and lightweight operation. 
- To switch to a different database (e.g., PostgreSQL), modify the `SQLALCHEMY_DATABASE_URI` in `app.py`.

---

## Contributing

We welcome contributions to improve this project. Here's how you can contribute:

1. **Fork the repository** to your GitHub account.
2. **Create a new branch** for your feature (`git checkout -b feature-branch`).
3. **Make your changes** and test them.
4. **Commit your changes** (`git commit -am 'Add feature'`).
5. **Push to your branch** (`git push origin feature-branch`).
6. **Create a Pull Request** with a description of your changes.

Please ensure your code follows the project's coding standards and includes tests for new functionality.

---

