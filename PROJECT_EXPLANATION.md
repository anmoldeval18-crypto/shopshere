# ShopSphere Viva Explanation

## One-Line Introduction

ShopSphere is a full-stack e-commerce website built using Django, PostgreSQL, Bootstrap 5, and the Django ORM for managing online shopping workflows such as product browsing, cart, checkout, order tracking, and reviews.

## Project Objective

The goal of this project is to create a practical e-commerce application that demonstrates important full-stack concepts:

- user authentication
- relational database design
- CRUD operations
- reusable templates
- form validation
- session and user-based workflows
- admin inventory management

## Why This Architecture Was Chosen

- Django is suitable because it provides ORM, authentication, admin panel, and form handling in one framework.
- PostgreSQL is used as the main SQL database because it is reliable and widely used in production.
- Bootstrap 5 helps create a responsive interface quickly while keeping the code understandable.
- Function-based views were chosen for easy explanation during viva.

## Main Modules

- `accounts`: handles register, login, profile, and saved addresses
- `products`: manages categories, product data, search, sorting, and product details
- `cart`: stores selected products before checkout
- `wishlist`: stores products users want to buy later
- `orders`: handles checkout, shipping details, payment option, and order history
- `reviews`: lets customers submit one review per purchased product
- `core`: contains home page, dashboard, and shared utilities

## Important Database Relationships

- One user has one profile
- One user can have many addresses
- One category can have many products
- One product can have many images and reviews
- One user has one cart and one wishlist
- One cart can have many cart items
- One order can have many order items
- One order has one payment record

## Order Placement Logic

1. User adds products to cart.
2. At checkout, the user selects a saved address or enters a new one.
3. The system calculates subtotal, shipping, and total amount.
4. An order is created inside a transaction.
5. Cart items are copied into order items.
6. Product stock is reduced.
7. A dummy payment record is created.
8. Cart is cleared and order confirmation is shown.

## Review Logic

- Only logged-in users can submit reviews.
- A user can review a product only once.
- Review submission is allowed only after the product has been purchased.

## Admin Features

- Product and category management
- Stock/inventory visibility
- Order and payment tracking
- User profile and address overview
- Review moderation support

## Possible Future Improvements

- coupon system
- online payment gateway integration
- product image gallery uploads
- pagination and advanced analytics
- email notifications
