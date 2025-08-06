from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product, Category,Wishlist   
from .filters import ProductFilter
from django.db.models import Q
from django.http import JsonResponse
import random
from .models import UsedProduct
from .forms import UsedProductForm
from .models import Product, Review
from .forms import ReviewForm
from django.contrib import messages
from accounts.views import profile_view 


@login_required    
def index(request):
    products = Product.objects.all()[:5]   
    return render(request, 'index.html', {'products': products})
@login_required 
def shop_view(request):
    category_slug = request.GET.get('category', '')
    print(f"Category Slug Received: {category_slug}")  # Debugging line

    products = Product.objects.all()

    # Check if the category exists before filtering
    if category_slug:
        try:
            if category_slug.isdigit():  # If it's an ID
                category = get_object_or_404(Category, id=category_slug)
            else:  # If it's a slug
                category = get_object_or_404(Category, slug=category_slug)

            products = products.filter(category=category)  # Apply filter
        except Exception as e:
            print(f"Category Lookup Error: {e}")  # Debugging output

    # Apply filters
    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs  

    # Pagination
    paginator = Paginator(filtered_products, 9)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, "shop.html", {
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": request.GET.get('category', ''),
        "product_filter": product_filter
    })



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = [img for img in [product.image1, product.image2, product.image3] if img] 

    all_products = list(Product.objects.exclude(id=product.id))  
    related_products = random.sample(all_products, min(len(all_products), 4)) 

    # Fetch real reviews from the database
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    # Fake reviews
    fake_reviews = [
        {"user": "JohnDoe", "rating": 5, "comment": "Amazing product! Highly recommended."},
        {"user": "Alice", "rating": 4, "comment": "Good quality, but shipping was slow."},
        {"user": "Michael", "rating": 5, "comment": "Worth every penny! Great sound."},
    ]

    # Handle review submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Ensure the user is logged in
            review.save()
            return redirect('product_detail', slug=slug)  # Reload page after submission

    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'images': images,
        'related_products': related_products,
        'reviews': reviews,
        'fake_reviews': fake_reviews,
        'form': form
    })



def about(request):
    return render(request, 'about.html')   

def contact(request):
    return render(request, 'contact.html')

 
def search_results(request):
    query = request.GET.get("q", "").strip()

    products = []
    categories = []

    if query:
        # Fetch products where the name contains the query (case-insensitive)
        products = Product.objects.filter(name__icontains=query)

        # Fetch categories where the name matches (for category-based search)
        categories = Category.objects.filter(name__icontains=query)

        # If a category is found, fetch all its products
        if categories.exists():
            for category in categories:
                category_products = category.products.all()
                products = products | category_products  # Combine products from categories

    return render(request, "search.html", {"products": products, "categories": categories})
def search_suggestions(request):
    """Return search suggestions for product names and categories."""
    query = request.GET.get('q', '').strip()
    suggestions = []

    if query:
        product_suggestions = Product.objects.filter(name__icontains=query).values_list('name', flat=True)[:5]
        category_suggestions = Category.objects.filter(name__icontains=query).values_list('name', flat=True)[:5]
        suggestions = list(product_suggestions) + list(category_suggestions)

    return JsonResponse({'suggestions': suggestions})



def  checkout(request):
    return render(request, 'checkout.html')




@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, "Added to Wishlist!")
    else:
        messages.info(request, "Already in Wishlist!")

    return redirect('wishlist_view')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, "Removed from Wishlist!")
    return redirect('wishlist_view')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def submit_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product = Product.objects.get(id=data['product_id'])
        review = Review.objects.create(
            product=product,
            user=request.user,
            text=data['text']
        )
        return JsonResponse({'success': True, 'review': {'username': request.user.username, 'text': review.text}})
    return JsonResponse({'success': False})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UsedProduct
from .forms import UsedProductForm

# Show all used products
def used_products_list(request):
    used_products = UsedProduct.objects.all().order_by('-created_at')
    return render(request, 'used_products_list.html', {'used_products': used_products})

# Add a used product
@login_required
def add_used_product(request):
    if request.method == "POST":
        form = UsedProductForm(request.POST, request.FILES)
        if form.is_valid():
            used_product = form.save(commit=False)
            used_product.seller = request.user
            used_product.save()
            return redirect('used_products_list')
    else:
        form = UsedProductForm()
    return render(request, 'add_used_product.html', {'form': form})

# Show logged-in user’s used products in profile
@login_required
def user_products(request):
    used_products = UsedProduct.objects.filter(seller=request.user)
    return render(request, 'user_added.html', {'used_products': used_products})


@login_required
def delete_used_product(request, product_id):
    product = get_object_or_404(UsedProduct, id=product_id, seller=request.user)
    product.delete()
    return redirect('accounts:profile')

from django.shortcuts import render, get_object_or_404
from .models import UsedProduct

 