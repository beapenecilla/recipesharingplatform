from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe, Comment, Rating, SavedRecipe
from django.db.models import Q
from . import models
from django.db.models import Avg
from django.http import HttpResponseBadRequest



# Homepage View
def homepage(request):
    context = {}
    return render(request, "myApp/homepage.html", context)

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'myApp/register.html', {'form': form})

# Login View
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'myApp/login.html', {'form': form})

# Logout View
def logout(request):
    auth_logout(request)
    return redirect('homepage')

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            return redirect('profile')
    else:
        form = RecipeForm()
    return render(request, 'myApp/create_recipe.html', {'form': form})

def profile_view(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(created_by=request.user)
        saved_recipes = request.user.saved_recipes.all()
    else:
        recipes = []
        saved_recipes = []
    return render(request, 'myApp/profile.html', {'recipes': recipes, 'saved_recipes': saved_recipes})

def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, created_by=request.user)
    recipe.delete()
    return redirect('profile')

# View for all recipes
def all_recipes(request):
    search_query = request.GET.get('search', '')
    recipes = Recipe.objects.all()

    if search_query:
        recipes = recipes.filter(Q(title__icontains=search_query) | Q(created_by__username__icontains=search_query))

    return render(request, 'myApp/all_recipes.html', {'recipes': recipes, 'search_query': search_query})

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'myApp/edit_recipe.html', {'form': form, 'recipe': recipe})

@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        if text:
            comment = Comment(recipe=recipe, user=request.user, text=text)
            comment.save()
        return redirect('recipe_detail', pk=recipe.pk)
    return redirect('recipe_detail', pk=recipe.pk)

@login_required
def add_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.created_by == request.user:
        return redirect('recipe_detail', pk=recipe.pk)

    if request.method == 'POST':
        score = request.POST.get('rating')
        try:
            score = int(score)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid rating value. Please enter a number.")

        if score < 1 or score > 5:
            return HttpResponseBadRequest("Rating must be between 1 and 5.")

        if Rating.objects.filter(recipe=recipe, user=request.user).exists():
            return redirect('recipe_detail', pk=recipe.pk)

        rating = Rating(recipe=recipe, user=request.user, score=score)
        rating.save()

        return redirect('recipe_detail', pk=recipe.pk)

    return redirect('recipe_detail', pk=recipe.pk)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all()
    ratings = recipe.ratings.all()

    # Calculating average rating
    average_rating = ratings.aggregate(Avg('score'))['score__avg'] if ratings.exists() else None
    
    return render(request, 'myApp/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'average_rating': average_rating,
        'ratings': ratings,
    })

@login_required
def save_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    saved_recipe, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    
    # Redirect to the user's profile page after saving the recipe
    return redirect('profile') 

@login_required
def unsave_recipe(request, pk):
    saved_recipe = get_object_or_404(SavedRecipe, pk=pk, user=request.user)
    saved_recipe.delete()
    return redirect('profile')

def about(request):
    return render(request, 'myApp/about_us.html')

def contact(request):
    return render(request, 'myApp/contact.html')