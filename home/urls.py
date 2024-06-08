from django.contrib import admin
from django.urls import path 
from home import views

urlpatterns = [
    path('homepage',views.studenthome,name="defaulthome"),
    path('home',views.formSubmission,name="home"),
    path('',views.loginUser,name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('login',views.loginUser,name="login"),
    path('adminpage',views.admin_dashboard,name="admin"),
    path('register',views.registerUser,name="register"),
    path('admin_register',views.registerAdmin,name="admin_register"),
    path('activate/<uidb64>/<token>',views.activate,name="activate")
]