
from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import ExcelUploadSerializer
from .models import Product
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from django.contrib import messages
import pandas as pd


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return redirect('login-form')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def registration_form(request):
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'password2': request.POST.get('password2')
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login-form')
        return render(request, 'registration_form.html', {'errors': serializer.errors})
    return render(request, 'registration_form.html')


class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                return redirect('products')  # Redirect to the products page
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_form(request):
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                return redirect('products')
            return render(request, 'login_form.html', {'errors': ['Invalid credentials']})
        return render(request, 'login_form.html', {'errors': serializer.errors})
    return render(request, 'login_form.html')


@api_view(['POST'])
def import_products(request):
    serializer = ExcelUploadSerializer(data=request.data)
    if serializer.is_valid():
        excel_file = request.FILES.get('file')
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            for _, row in df.iterrows():
                product_data = {
                    'brand_name': row.get('brand_name'),
                    'product_name': row.get('product_name'),
                    'product_image': row.get('product_image'),
                    'offer_price': row.get('offer_price'),
                    'original_price': row.get('original_price'),
                    'deal_percentage': row.get('deal_percentage'),
                    'sizes': row.get('sizes'),
                    'rating': row.get('rating'),
                    'category': row.get('category'),
                }
                Product.objects.create(**product_data)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def all_products(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products': products})
