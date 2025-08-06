from django import forms
from .models import Review
from .models import UsedProduct

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


from django import forms
from .models import UsedProduct

class UsedProductForm(forms.ModelForm):
    class Meta:
        model = UsedProduct
        fields = ['title', 'description', 'price', 'phone_number', 'condition', 'image1', 'image2', 'image3']
