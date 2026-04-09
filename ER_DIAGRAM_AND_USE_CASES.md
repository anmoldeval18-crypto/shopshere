# ER Diagram Entities and Use Cases

## Suggested ER Diagram Entities

- User
- Profile
- Address
- Category
- Product
- ProductImage
- Cart
- CartItem
- Wishlist
- WishlistItem
- Order
- OrderItem
- Payment
- Review

## Relationship Summary

- User 1:1 Profile
- User 1:M Address
- Category 1:M Product
- Product 1:M ProductImage
- User 1:1 Cart
- Cart 1:M CartItem
- User 1:1 Wishlist
- Wishlist 1:M WishlistItem
- User 1:M Order
- Order 1:M OrderItem
- Order 1:1 Payment
- User 1:M Review
- Product 1:M Review

## Main Use Cases

### Customer

- register account
- login/logout
- browse categories
- search and filter products
- view product details
- add products to cart
- update or remove cart items
- add products to wishlist
- move wishlist items to cart
- save addresses
- place order using cash on delivery or dummy online payment
- view previous orders
- submit review for purchased product

### Admin

- login to admin panel
- manage categories
- manage products and stock
- manage users and profiles
- manage orders and payment records
- monitor low-stock items
- moderate reviews if needed
