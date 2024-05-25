# Ecart

Ecart is a simple e-commerce application built using Django, HTML, CSS, and Bootstrap. This project provides a foundational platform for an online store, where customer can buy electronic items.

## Features

- User authentication and registration(with account activation link)
- Product listing and detail pages
- Shopping cart functionality
- Order processing with payment gateway.
- User can make a review for product after buying the product.
- Responsive design using Bootstrap

## Technologies Used

- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Django
- **Database**: SQLite (default Django configuration)

## Installation

### Prerequisites

- Python (3.8)
- Django (3.1)

### Steps

1. **Clone the repository**
   ```bash
   git clone git@github.com:pintodas16/E-Cart.git
   cd E-Cart
   ```
2. **Create and activate a virtual environment**

   ```
   python -m venv env
   source venv/bin/activate  # On Windows use `env\Scripts\activate`

   ```

3. **Install the required packages**

   ```
   pip install -r requirements.txt


   ```

4. **Run database migrations**

   ```
   python manage.py migrate
   ```

5. **Create a superuser (for accessing the admin panel)**

   ```
   python manage.py createsuperuser
   ```

6. **Start the development server**

   ```
   python manage.py runserver
   ```

## Usage

### Admin Panel

Access the admin panel at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) using the superuser credentials created earlier. Here, you can manage products, orders, and users.

### Adding Products

1. Log in to the admin panel.
2. Navigate to the "Products" section.
3. Add new products with details such as name, description, price, and image.

### Shopping Cart and Checkout

- Users can browse products, add them to the cart, and proceed to checkout.
- Users must be logged to be able place order.

## Contact

- For any inquiries or issues, please contact [pintodas.lu@gmail.com].
