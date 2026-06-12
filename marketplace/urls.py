from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include

from accounts.views import (
    get_company_data,
    register_company,
    dashboard,
    employees,
    add_employee,
)

from accounts.admin_views import (
    admin_panel,
    users_list,
    change_user_role,
    delete_user,
    admin_products,
    admin_delete_product,
    admin_orders,
    admin_change_order_status,
)

from orders.views import (
    create_order,
    company_orders,
    order_detail,
)

from products.views import (
    homepage,
    product_list,
    product_detail,
    add_product,
    my_products,
    edit_product,
    delete_product,
)

urlpatterns = [

    # Homepage
    path('', homepage, name='homepage'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Register
    path(
        'register/',
        register_company,
        name='register_company'
    ),

    # Dashboard
    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/login/'
        ),
        name='logout'
    ),

    # Products
    path(
        'products/',
        product_list,
        name='product_list'
    ),

    path(
        'products/add/',
        add_product,
        name='add_product'
    ),

    path(
        'products/<int:pk>/',
        product_detail,
        name='product_detail'
    ),

    path(
        'products/<int:pk>/edit/',
        edit_product,
        name='edit_product'
    ),

    path(
        'products/<int:pk>/delete/',
        delete_product,
        name='delete_product'
    ),

    path(
        'my-products/',
        my_products,
        name='my_products'
    ),

    # Employees
    path(
        'employees/',
        employees,
        name='employees'
    ),

    path(
        'employees/add/',
        add_employee,
        name='add_employee'
    ),

    # Orders
    path(
        'orders/create/',
        create_order,
        name='create_order'
    ),

    path(
        'company-orders/',
        company_orders,
        name='company_orders'
    ),

    path(
        'company-orders/<int:pk>/',
        order_detail,
        name='order_detail'
    ),

    # Admin Panel
    path(
        'admin-panel/',
        admin_panel,
        name='admin_panel'
    ),

    path(
        'admin-users/',
        users_list,
        name='users_list'
    ),

    path(
        'admin-users/<int:user_id>/role/',
        change_user_role,
        name='change_user_role'
    ),

    path(
        'admin-users/<int:user_id>/delete/',
        delete_user,
        name='delete_user'
    ),

    path(
        'admin-products/',
        admin_products,
        name='admin_products'
    ),

    path(
        'admin-products/<int:product_id>/delete/',
        admin_delete_product,
        name='admin_delete_product'
    ),
    
        path(
        'admin-orders/',
        admin_orders,
        name='admin_orders'
    ),

    path(
        'admin-orders/<int:order_id>/status/',
        admin_change_order_status,
        name='admin_change_order_status'
    ),
    
    path(
    'messages/',
    include('messages_app.urls')
    ),

    # Cart
    path(
        'cart/',
        include('cart.urls')
    ),

    # API Company Data
    path(   
        'api/company-data/',
        get_company_data,
        name='company_data'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )