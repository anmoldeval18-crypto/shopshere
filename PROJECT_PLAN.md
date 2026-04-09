# ShopSphere Project Plan

## Final Folder Structure

```text
ShopSphere/
├── accounts/
├── cart/
├── core/
│   └── management/commands/seed_data.py
├── orders/
├── products/
├── reviews/
├── shopsphere/
├── static/
│   ├── css/style.css
│   └── js/main.js
├── templates/
│   ├── accounts/
│   ├── cart/
│   ├── core/
│   ├── includes/
│   ├── orders/
│   ├── products/
│   └── wishlist/
├── wishlist/
├── .env.example
├── manage.py
├── PROJECT_EXPLANATION.md
├── ER_DIAGRAM_AND_USE_CASES.md
├── README.md
├── requirements.txt
└── SCREENSHOT_CHECKLIST.md
```

## App Responsibilities

- `core`: shared home page, admin dashboard, global context processor, seed command
- `accounts`: registration, login, password reset, profile management, address book
- `products`: categories, products, product images, catalog browsing, search, filters
- `cart`: shopping cart and cart item management
- `wishlist`: wishlist creation, save for later, move to cart
- `orders`: checkout, order placement, payment record, order history
- `reviews`: customer ratings and reviews

## Database Schema Summary

- `User`: Django built-in authentication user
- `Profile`: extra user details such as phone number, bio, and profile image
- `Address`: saved user shipping addresses
- `Category`: product grouping with slug and description
- `Product`: main product information, price, discount, stock, flags
- `ProductImage`: product gallery images
- `Cart`: one active cart per user
- `CartItem`: selected products and quantities
- `Wishlist`: one wishlist per user
- `WishlistItem`: saved products
- `Order`: shipping details, totals, order status, payment method
- `OrderItem`: product snapshot inside each order
- `Payment`: dummy payment tracking for placed orders
- `Review`: one review per user per purchased product

## Architecture Overview

- Presentation layer uses Django templates with Bootstrap 5 and reusable includes
- Business logic is kept in readable function-based views
- Data access uses Django ORM relationships and model helper properties
- Authentication relies on Django's built-in auth system
- Inventory reduces at order placement time inside a database transaction
- Admin operations use both Django admin and a simple staff dashboard page

## Step-by-Step Build Plan

1. Configure Django project settings, static files, media files, environment variables, and shared URLs.
2. Create modular apps for authentication, products, cart, wishlist, orders, and reviews.
3. Define models with clear relationships and admin registrations.
4. Build forms for registration, profile, address, checkout, and reviews.
5. Implement views and URL routing for catalog browsing and purchase flow.
6. Design responsive templates using Bootstrap 5 and shared components.
7. Seed sample categories and products for demo and testing.
8. Run migrations, create a superuser, test user flow, and document the project.
