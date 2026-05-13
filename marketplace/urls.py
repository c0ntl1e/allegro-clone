from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.views import employees, add_employee
from orders.views import create_order, company_orders, order_detail


from accounts.views import register_company, dashboard
from products.views import (
    product_list,
    product_detail,
    add_product,
    my_products,
    edit_product,
    delete_product,
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Rejestracja i panel użytkownika
    path('register/', register_company, name='register_company'),
    path('dashboard/', dashboard, name='dashboard'),

    # Logowanie i wylogowanie
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/login/'
        ),
        name='logout'
    ),

    # Produkty
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('my-products/', my_products, name='my_products'),
    path('products/<int:pk>/edit/', edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', delete_product, name='delete_product'),
    path('employees/', employees, name='employees'),
    path('employees/add/', add_employee, name='add_employee'),
    path('company-orders/', company_orders, name='company_orders'),
    path('company-orders/<int:pk>/', order_detail, name='order_detail'),
    path('orders/create/', create_order, name='create_order'),
    
    # Koszyk
    path('cart/', include('cart.urls')),
]

# Obsługa plików media podczas developmentu
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )