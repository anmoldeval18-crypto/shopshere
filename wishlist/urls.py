from django.urls import path

from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.wishlist_detail, name="wishlist_detail"),
    path("toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("remove/<int:item_id>/", views.remove_wishlist_item, name="remove_wishlist_item"),
    path("move-to-cart/<int:item_id>/", views.move_to_cart, name="move_to_cart"),
]
