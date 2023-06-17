# eCommerce Project

**This eCommerce project is designed to provide an online shopping experience for customers. It includes various features such as product listing, cart management, user authentication, and order processing.**

## Features

- User registration and authentication
- Product listing and details
- Shopping cart functionality
- Order placement and processing
- User profile management

## Getting Started
**To get a local copy up and running, follow these steps.**
### Prerequisites
- Python 3.x
- Django
- Django Rest Framework (DRF)
- PostgreSQL 

## Installation

 - Clone the repository ```git clone https://github.com/your_username/ecommerce.git``` 
 - Navigate to the project directory: ```cd ecommerce``` 
 - Create and activate a virtual environment (optional, but recommended)```python3 -m venv venv  source venv/bin/activate```
 - Install the project dependencies: ```pip install -r requirements.txt``` 
 - Set up the database: If using PostgreSQL, create a new database and update the database settings in **settings.py**:
 - Apply database migrations :  ```python manage.py migrate``` 
 - Create a superuser for admin access:```python manage.py createsuperuser```
 - Start the development server: ```python manage.py runserver``` 

## Usage
- Access the application by visiting http://localhost:8000 in your web browser.
- Use the provided admin credentials to log in to the admin panel (http://localhost:8000/admin) and manage products, orders, and user accounts.
- Explore the website, add products to the cart, and place orders as a regular user.


## Docker Support

**If you prefer to run the API using Docker, follow these additional steps:**

- Build the Docker image: ```$ docker build -t project-api .```
- Run the Docker container: ```$ $ docker run -p 8000:8000 project-api.```

## Author
 - Youssef Alaa Youssef 

## License
This project is licensed under the MIT License. See the **LICENSE** file for more information.