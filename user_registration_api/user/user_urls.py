from django.urls import path,include
from . import views
# User API Routes

urlpatterns = [
    path('register/', views.register_user, name="register_user" ),
    path('login/', views.login, name="login" ),
    path('logout/', views.logout, name="logout" ),
    path('<str:email>/', views.user_details, name="user_details"),
    path('confirm/<str:emailid>/', views.verify_user, name="user_details"),
    path('reset/', views.reset_password,name='reset_password')
]