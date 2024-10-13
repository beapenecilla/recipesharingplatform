from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"), 
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'), 
    path('recipe/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('recipe/<int:pk>/rating/', views.add_rating, name='add_rating'),
    path('recipe/<int:pk>/save/', views.save_recipe, name='save_recipe'),  # New URL for saving recipes
    path('profile/', views.profile_view, name='profile'),
    path('recipe/delete/<int:pk>/', views.delete_recipe, name='delete_recipe'),
    path('all_recipes/', views.all_recipes, name='all_recipes'), 
    path('recipe/edit/<int:pk>/', views.edit_recipe, name='edit_recipe'),
    #new for profile pic
     path('profile/update/', views.update_profile, name='update_profile'),
]
