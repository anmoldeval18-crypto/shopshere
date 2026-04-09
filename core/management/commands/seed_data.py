from decimal import Decimal

from django.core.management.base import BaseCommand

from products.models import Category, Product


class Command(BaseCommand):
    help = "Seeds the database with sample categories and products for ShopSphere."

    def handle(self, *args, **options):
        categories = [
            {
                "name": "Electronics",
                "description": "Smart devices and accessories for everyday use.",
            },
            {
                "name": "Fashion",
                "description": "Trendy and comfortable products for daily wear.",
            },
            {
                "name": "Home & Living",
                "description": "Useful products that improve home comfort and style.",
            },
            {
                "name": "Books",
                "description": "Academic and leisure books for every learner.",
            },
        ]

        category_objects = {}
        for category_data in categories:
            category, _ = Category.objects.get_or_create(
                name=category_data["name"],
                defaults={"description": category_data["description"]},
            )
            category_objects[category.name] = category

        products = [
            {
                "category": "Electronics",
                "name": "Wireless Bluetooth Headphones",
                "sku": "ELEC-001",
                "short_description": "Over-ear headphones with deep bass and long battery life.",
                "description": "Comfortable Bluetooth headphones suitable for online classes, entertainment, and gaming. Includes noise isolation ear cups and up to 20 hours of battery backup.",
                "specifications": "Bluetooth 5.2\n20-hour battery life\nBuilt-in microphone\nType-C charging",
                "price": Decimal("2999.00"),
                "discount_price": Decimal("2499.00"),
                "stock": 18,
                "is_featured": True,
                "is_trending": True,
            },
            {
                "category": "Electronics",
                "name": "Portable Power Bank 20000mAh",
                "sku": "ELEC-002",
                "short_description": "Fast charging power bank for phones and small gadgets.",
                "description": "A reliable power bank with dual USB output ports and LED battery indicator for travel and daily use.",
                "specifications": "20000mAh capacity\n18W fast charging\nDual USB output\nLED battery status",
                "price": Decimal("1899.00"),
                "discount_price": Decimal("1599.00"),
                "stock": 24,
                "is_featured": True,
                "is_trending": False,
            },
            {
                "category": "Fashion",
                "name": "Classic Denim Jacket",
                "sku": "FASH-001",
                "short_description": "Smart casual denim jacket with a timeless fit.",
                "description": "A stylish denim jacket designed for casual outings and college wear. Easy to pair with shirts and T-shirts.",
                "specifications": "Cotton blend\nRegular fit\nButton closure\nTwo side pockets",
                "price": Decimal("2499.00"),
                "discount_price": Decimal("2199.00"),
                "stock": 12,
                "is_featured": False,
                "is_trending": True,
            },
            {
                "category": "Fashion",
                "name": "Sports Running Shoes",
                "sku": "FASH-002",
                "short_description": "Lightweight running shoes for active daily use.",
                "description": "Breathable sports shoes made for college, jogging, and comfortable walking throughout the day.",
                "specifications": "Mesh upper\nFoam sole\nLace-up closure\nShock absorption",
                "price": Decimal("3499.00"),
                "discount_price": Decimal("2999.00"),
                "stock": 15,
                "is_featured": True,
                "is_trending": True,
            },
            {
                "category": "Home & Living",
                "name": "Minimal Desk Lamp",
                "sku": "HOME-001",
                "short_description": "Modern study lamp with adjustable brightness.",
                "description": "A compact desk lamp ideal for study tables and workspaces. It includes multiple brightness levels for focused work.",
                "specifications": "LED lighting\nTouch controls\n3 brightness modes\nUSB powered",
                "price": Decimal("1299.00"),
                "discount_price": Decimal("999.00"),
                "stock": 20,
                "is_featured": False,
                "is_trending": False,
            },
            {
                "category": "Home & Living",
                "name": "Insulated Water Bottle",
                "sku": "HOME-002",
                "short_description": "Stainless steel bottle that keeps drinks hot or cold.",
                "description": "A sleek insulated bottle for daily college and office use, designed to maintain beverage temperature for long hours.",
                "specifications": "750ml capacity\nStainless steel body\nLeak-proof lid\nEasy carry design",
                "price": Decimal("899.00"),
                "discount_price": Decimal("749.00"),
                "stock": 30,
                "is_featured": False,
                "is_trending": True,
            },
            {
                "category": "Books",
                "name": "Python for Beginners Handbook",
                "sku": "BOOK-001",
                "short_description": "A beginner-friendly guide to Python programming.",
                "description": "An easy-to-understand programming handbook covering Python fundamentals, control structures, functions, and mini exercises.",
                "specifications": "Paperback\n320 pages\nBeginner friendly\nPractice examples",
                "price": Decimal("699.00"),
                "discount_price": Decimal("549.00"),
                "stock": 40,
                "is_featured": True,
                "is_trending": False,
            },
            {
                "category": "Books",
                "name": "Digital Marketing Basics",
                "sku": "BOOK-002",
                "short_description": "Foundational concepts of online marketing and branding.",
                "description": "A practical introductory book for students who want to understand social media marketing, SEO, ads, and online customer engagement.",
                "specifications": "Paperback\n250 pages\nBusiness basics\nCase studies included",
                "price": Decimal("799.00"),
                "discount_price": Decimal("649.00"),
                "stock": 26,
                "is_featured": False,
                "is_trending": True,
            },
        ]

        created_count = 0
        for item in products:
            _, created = Product.objects.get_or_create(
                sku=item["sku"],
                defaults={
                    "category": category_objects[item["category"]],
                    "name": item["name"],
                    "short_description": item["short_description"],
                    "description": item["description"],
                    "specifications": item["specifications"],
                    "price": item["price"],
                    "discount_price": item["discount_price"],
                    "stock": item["stock"],
                    "is_featured": item["is_featured"],
                    "is_trending": item["is_trending"],
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Added {created_count} products."))
