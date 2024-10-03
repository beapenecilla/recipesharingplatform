# forms.py
from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'steps', 'image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 4}),
            'steps': forms.Textarea(attrs={'rows': 6}),
        }
