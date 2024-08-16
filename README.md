This README provides information on how to set up, use, and configure the app. Getting started

Prerequisites Make sure you have the following installed on your system: python

Cloning the project You can clone the project by copying this project link to your local repository. Use: (git clone 'url copied.....') to clone

Installing dependencies Setting Up Python Environment (Backend)

To prepare your development environment for running the Python backend, please follow these steps: --- Open your terminal and ensure you have different terminal windows or tabs available for running both the frontend and backend of your project. --- Set up a Python environment to isolate your project dependencies. You can refer to the official Python documentation at python.org for guidance on creating a virtual environment. --- Activate your Python environment to work within its isolated environment after navigating to backend_only root directory. --- Install all the necessary project dependencies by running the following command:

& pip install -r requirements.txt This command will install all the required Python packages listed in the requirements.txt file. Make sure you have Django installed. If not, you can install it using the Python package manager (pip).

Start the Django development server by running the following command: & python manage.py runserver This will launch the server, and your backend will be up and running.

You can now proceed to apply database migrations. Use the following command to migrate all tables to your database: & python manage.py migrate


The following are the list of the endpoints as regards the assessment question.
1. User Authentication API
http://127.0.0.1:8000/auth/users/  for creating an account
http://127.0.0.1:8000/auth/jwt/create/ for login in

2. Inventory Management API
http://127.0.0.1:8000/store/products/ For geting, updating, posting and deleting product

3. Order Management
http://127.0.0.1:8000/store/carts/  To store products in a cart, you can send a POST request with a cart_id to the endpoint. The server will respond by generating and storing a unique identifier for the cart in the database. This unique identifier is a 36-character UUID (e.g., daab6dee-d4d8-408e-9cfb-314dbe8a152c). Be sure to copy and keep this unique identifier for future reference.

After obtaining the unique identifier (UUID) for your cart, you can add items to it by navigating to http://127.0.0.1:8000/store/carts/{uuid}/items/, replacing {uuid} with the copied unique identifier. This URL allows you to access the items endpoint, where you can include various items through their respective IDs in your cart. When you are done shopping, you can see the list of items by getting your cart again. http://127.0.0.1:8000/store/carts/{uuid}/

- After completing your shopping, navigate to http://127.0.0.1:8000/store/orders/{uuid}/, replacing {uuid} with your unique identifier. This will allow you to retrieve your product order instantly.




http://127.0.0.1:8000/store/lesser-product-report/?quantity_lt=5