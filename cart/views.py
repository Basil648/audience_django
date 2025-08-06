from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse
from django.db.models import Sum, F
from decimal import Decimal  # Import Decimal



def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")  # Ensure user is logged in before adding to cart

    # Ensure the user has a cart, create one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)

    # Increase quantity if item already exists
    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_view")


def decrease_cart_quantity(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")  

    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item if quantity reaches 0

    return redirect("cart_view")


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_price": total_price
    }

    return render(request, "cart.html", context)



def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")  

    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    
    return redirect("cart_view")


     
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Corrected total calculation
    total_price = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or Decimal(0)

    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect("login")  

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Debug information
    print(f"User: {request.user.username}")
    print(f"Cart ID: {cart.id}")
    print(f"Cart items count: {cart_items.count()}")
    
    # Calculate total price only if there are items
    if cart_items.exists():
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        print(f"Total price: {total_price}")
    else:
        total_price = 0
        print("No items in cart")

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    
    # Print the final context
    print(f"Context: {context}")
    
    return render(request, "checkout.html", context)







 
from .models import BillingDetails

from django.contrib.auth.decorators import login_required
from .models import BillingDetails, Cart, CartItem

@login_required
def process_payment(request):
    if request.method == 'POST':
        user = request.user

        # Get billing info from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        state_country = request.POST.get('state_country')
        postal_zip = request.POST.get('postal_zip')
        email_address = request.POST.get('email_address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        # Get user's cart and items
        cart = Cart.objects.get(user=user)
        cart_items = cart.cart_items.all()

        # Prepare cart items in JSON-serializable format
        cart_items_data = [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "price": float(item.product.discounted_price),
                "total_price": float(item.total_price),
            }
            for item in cart_items
        ]

        # Save billing with cart items
        billing = BillingDetails.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            state_country=state_country,
            postal_zip=postal_zip,
            email_address=email_address,
            phone=phone,
            payment_method=payment_method,
            cart_items=cart_items_data  # 👈 make sure this is a JSONField
        )

        # ✅ Clear the cart after order is placed
        cart_items.delete()

        # Redirect based on payment method
        if payment_method == 'card':
            return redirect('card_payment')
        elif payment_method == 'cod':
            return redirect('cod_view')

    return redirect('checkout')
 

def card_payment(request):
    return render(request, 'payments/card.html')

 

from django.contrib.auth.decorators import login_required
from cart.models import BillingDetails

@login_required
def cod_view(request):
    try:
        billing_details = BillingDetails.objects.filter(email_address=request.user.email).latest('created_at')

    except BillingDetails.DoesNotExist:
        billing_details = None  # Handle case where no billing details exist

    context = {'billing_details': billing_details}
    return render(request, 'payments/cod.html', context)



def thank_you(request):
    return render(request, 'payments/thank_you.html')

def thanku_card(request):
    return render(request, 'payments/thanku_card.html')