from django.urls import path
from django.shortcuts import redirect
from .views import *  
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    path('', login_required(index), name='index'),
    path('products/', login_required(shop_view), name='shop_view'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),  # Product detail page
    path('about/', about, name='about'),
    path('contact/',contact, name='contact'),
    path('search/', search_results, name='search_results'),
    path('search_suggestions/', search_suggestions, name='search_suggestions'),  # Add this
    path('checkout/', checkout, name='checkout'),
    path('wishlist/', wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('submit-review/', submit_review, name='submit_review'),
    path('used-products/', used_products_list, name='used_products_list'),
    path('used-products/add/', add_used_product, name='add_used_product'),
    path('used-products/my/', user_products, name='user_products'),
    path('delete-used-product/<int:product_id>/', delete_used_product, name='delete_used_product'),
 
]
 
