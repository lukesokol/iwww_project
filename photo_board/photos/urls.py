from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='board'),
    path('add/', views.add_photo, name='add_photo'),
    path('photo/<str:pk>/', views.view_photo, name='photo'),
    path('like_photo/', views.like_photo, name='like_photo'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
]