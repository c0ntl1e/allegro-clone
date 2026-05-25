from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from accounts.views import (
    get_company_data,
    register_company,
    dashboard,
    employees,
    add_employee,
)

from orders.views import (
    create_order,
    company_orders,
    order_detail,
)

from products.views import (
    product_list,
    product_detail,
    add_product,
    my_products,
    edit_product,
    delete_product,
)

urlpatterns = [
    # Главная страница сайта → каталог товаров
    path('', product_list, name='home'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Регистрация и панель пользователя
    path('register/', register_company, name='register_company'),
    path('dashboard/', dashboard, name='dashboard'),

    # Авторизация
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    # Выход из аккаунта
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/login/'
        ),
        name='logout'
    ),

    # Товары
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('my-products/', my_products, name='my_products'),
    path('products/<int:pk>/edit/', edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', delete_product, name='delete_product'),

    # Сотрудники компании
    path('employees/', employees, name='employees'),
    path('employees/add/', add_employee, name='add_employee'),

    # Заказы компании
    path('company-orders/', company_orders, name='company_orders'),
    path('company-orders/<int:pk>/', order_detail, name='order_detail'),

    # Создание заказа
    path('orders/create/', create_order, name='create_order'),

    # Корзина
    path('cart/', include('cart.urls')),
    
    path(
    'api/company-data/',
    get_company_data,
    name='company_data'
),
]

# Обслуживание media-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )