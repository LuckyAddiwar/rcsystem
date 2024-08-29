from turtle import home
from django.urls import path
from .views import RegisterUserView, import_products, registration_form, LoginUserView, login_form, all_products

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register-form/', registration_form, name='registration-form'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('login-form/', login_form, name='login-form'),
    path('import-products/', import_products, name='import-products'),
    path('products/', all_products, name='products'),
]
