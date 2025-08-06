from django.db import models
from django.contrib.auth.models import User
from store.models import Product  # Importing Product from the store app


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")  # Added related_name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")  # Added related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):  # ✅ Changed method to property
        return self.product.discounted_price * self.quantity  

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class BillingDetails(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('cod', 'Cash on Delivery'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    state_country = models.CharField(max_length=100)
    postal_zip = models.CharField(max_length=20)
    email_address = models.EmailField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    
    # Store cart items with product name, quantity, and price information
    cart_items = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.payment_method}"

    def get_cart_items(self):
        # Returns a readable representation of cart items
        return self.cart_items

 