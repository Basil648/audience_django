import django_filters
from django import forms
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    # Category Filter (Dropdown)
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label="All Categories",
        method="filter_by_category",  # Explicit method added
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # "Brand" Filter (Dropdown using Product Names)
    brand = django_filters.ChoiceFilter(
        field_name='name',  # This should be changed if you have a brand field
        choices=[],  # Dynamically populated
        method='filter_by_brand',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Price Range Filter (Using Min & Max Inputs)
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Price'})
    )
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'})
    )

    # Ratings Filter (List)
    rating = django_filters.ChoiceFilter(
        field_name='rating',
        choices=[
            (5, "5 stars"),
            (4, "4 stars and above"),
            (3, "3 stars and above"),
            (2, "2 stars and above"),
            (1, "1 star and above")
        ],
        method="filter_by_rating",
        widget=forms.RadioSelect
    )

    def filter_by_category(self, queryset, name, value):
        """Filter products by category"""
        if value:
            return queryset.filter(category=value)
        return queryset

    def filter_by_brand(self, queryset, name, value):
        """Filter products by brand (if applicable)"""
        return queryset.filter(name=value) if value else queryset

    def filter_by_rating(self, queryset, name, value):
        """Filter products with a minimum rating"""
        return queryset.filter(rating__gte=value)

    def __init__(self, *args, **kwargs):
        """Dynamically populate the brand choices with unique product names"""
        super().__init__(*args, **kwargs)
        unique_brands = Product.objects.values_list('name', flat=True).distinct()
        self.filters['brand'].field.choices = [(brand, brand) for brand in unique_brands]

    class Meta:
        model = Product
        fields = ['category', 'brand', 'min_price', 'max_price', 'rating']
