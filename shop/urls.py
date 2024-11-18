from django.urls import path
from .views import product_detail_view, category_view, cart_view, add_to_cart_view, remove_from_cart, product_search_view, checkout_view, order_confirmation_view, order_history_view

urlpatterns = [
    path('product/<int:id>/', product_detail_view, name='product'),
    path('category/<int:id>/', category_view, name='category'),
    path('cart/', cart_view, name='cart'),
    path('addcart/<int:id>/', add_to_cart_view, name='addtocart' ),
    path('remove/<int:id>/', remove_from_cart, name='remove'),
    path('product/search/', product_search_view, name='productsearch'),
    path('checkout/', checkout_view, name='checkout'),
    path('orderconfirm/', order_confirmation_view, name='confirm'),
    path('orderhistory/', order_history_view, name='orders'),
]