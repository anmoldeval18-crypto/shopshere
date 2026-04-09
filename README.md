# ShopSphere

ShopSphere is a full-stack e-commerce website built as a college major project using Django, PostgreSQL, Bootstrap 5, JavaScript, and the Django ORM. It demonstrates the complete shopping workflow from user registration to order placement, while keeping the code clean, modular, and easy to explain in viva.

## Features

- User registration, login, logout, profile page, and password reset flow
- Home page with hero section, featured products, categories, and new arrivals
- Product catalog with category browsing, search, price filters, and sorting
- Cart management with quantity update and subtotal calculation
- Wishlist with move-to-cart support
- Checkout with saved address or new shipping form
- Dummy payment flow and cash on delivery support
- Order confirmation, order history, and order detail pages
- Ratings and reviews for purchased products
- Staff dashboard and Django admin management for products, categories, stock, orders, payments, and users
- Sample seed data command for quick demonstration
- Automated Django tests for core pages and shopping flow

## Tech Stack

- Backend: Python Django
- Database: PostgreSQL via environment variables
- Frontend: HTML, CSS, Bootstrap 5, JavaScript
- ORM: Django ORM
- Media Handling: Django `ImageField`

## Project Structure

- `accounts` for authentication, profiles, and addresses
- `products` for categories, products, images, browsing, and search
- `cart` for shopping cart logic
- `wishlist` for saved products
- `orders` for checkout, payments, and order history
- `reviews` for user ratings and reviews
- `core` for home page, staff dashboard, and sample seed data

## Important Design Decisions

- The project uses Django's built-in `User` model and a separate `Profile` model. This is easier to explain in viva than a custom user model.
- Checkout supports both a saved address and a one-time shipping address.
- New checkout addresses are saved to the profile only when the user explicitly selects the save option.
- The payment flow is intentionally dummy-based to keep the project safe, local, and submission-friendly.

## Installation Steps

1. Clone or download the project.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Copy `.env.example` to `.env` and update the PostgreSQL values:

```bash
cp .env.example .env
```

6. Choose one database option:

- For PostgreSQL:
  Create a PostgreSQL database such as `shopsphere_db`, then fill the `POSTGRES_*` values in `.env`.
- For a quick local demo:
  Leave `POSTGRES_DB` blank in `.env` and the project will use SQLite automatically.

7. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

8. Create a superuser:

```bash
python manage.py createsuperuser
```

9. Seed sample data:

```bash
python manage.py seed_data
```

10. Start the development server:

```bash
python manage.py runserver
```

11. Run the automated tests:

```bash
python manage.py test
```

12. Open the project in your browser:

- Home page: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## Quick Local Run Notes

- If PostgreSQL variables are not provided, the project falls back to SQLite for quick demo usage.
- Password reset emails are printed in the terminal because the project uses Django's console email backend in development.
- Product images are stored using media files. Add uploaded images through the admin panel.
- Bootstrap 5 and Google Fonts are loaded from CDNs, so internet access gives the best visual result during demo.

## Default Admin Creation

Use the following command to create an admin account:

```bash
python manage.py createsuperuser
```

After logging in to `/admin/`, you can add categories, products, images, and manage orders.

## Demo User Flow to Test

1. Register a new user account
2. Login
3. Browse the product catalog
4. Add items to wishlist and cart
5. Go to checkout and place an order
6. Open My Orders and view the order
7. Return to the purchased product and submit a review

## Manual Testing Checklist

1. Open the home page and verify featured and trending sections load.
2. Register a new account and log in.
3. Open the profile page and save one address.
4. Browse the product catalog and test search, category filter, and sorting.
5. Open a product detail page and add the product to the wishlist.
6. Move the wishlist item to the cart.
7. Update cart quantity and remove one cart item.
8. Add a product again and proceed to checkout.
9. Test both payment methods: `Cash on Delivery` and `Online Payment (Dummy)`.
10. Confirm the order appears in `My Orders`.
11. Open the product again and submit one review.
12. Log in to `/admin/` and verify product, order, payment, review, and address management.

## Final Run Commands

```bash
cd /Users/rahulmalhotra/Documents/Anmol
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py test
python manage.py runserver
```

## Missing Files or Setup Notes

- Create `.env` from `.env.example` before running the server.
- Add product images from the admin panel if you want a more visual demo.
- If you want PostgreSQL instead of SQLite fallback, make sure the database server is running before `migrate`.

## Report and Viva Support

- [Project Plan](PROJECT_PLAN.md)
- [Project Explanation](PROJECT_EXPLANATION.md)
- [Screenshot Checklist](SCREENSHOT_CHECKLIST.md)
- [ER Diagram and Use Cases](ER_DIAGRAM_AND_USE_CASES.md)
