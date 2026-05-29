from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm


def homepage(request):

    products = Product.objects.select_related(
        'company',
        'category'
    ).all()

    categories = Category.objects.all()

    companies = []

    for product in Product.objects.select_related('company'):
        if product.company not in companies:
            companies.append(product.company)

    query = request.GET.get('q', '')

    category = request.GET.get('category')

    company = request.GET.get('company')

    sort = request.GET.get('sort')

    if query:

        products = products.filter(
            name__icontains=query
        )

    if category:

        products = products.filter(
            category_id=category
        )

    if company:

        products = products.filter(
            company_id=company
        )

    if sort == 'price_asc':

        products = products.order_by('price')

    elif sort == 'price_desc':

        products = products.order_by('-price')

    elif sort == 'newest':

        products = products.order_by('-created_at')

    elif sort == 'oldest':

        products = products.order_by('created_at')

    else:

        products = products.order_by('-created_at')

    return render(request, 'products/homepage.html', {
        'products': products,
        'categories': categories,
        'companies': companies,
        'query': query,
        'selected_category': category,
        'selected_company': company,
        'selected_sort': sort,
    })


def product_list(request):

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    products = Product.objects.select_related(
        'company',
        'category'
    ).all()

    # Поиск по названию товара
    if query:

        products = products.filter(
            name__icontains=query
        )

    # Фильтрация по категории
    if category_id:

        products = products.filter(
            category_id=category_id
        )

    # Все категории
    categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
    })


def product_detail(request, pk):

    product = get_object_or_404(
        Product.objects.select_related(
            'company',
            'category'
        ),
        pk=pk
    )

    return render(request, 'products/product_detail.html', {
        'product': product
    })


@login_required
def add_product(request):

    # Только firma / sales
    if request.user.role not in ['company', 'sales']:

        return redirect('/dashboard/')

    # Определяем компанию
    if request.user.role == 'company':

        company = request.user.owned_company

    else:

        company = request.user.company

    # Обработка формы
    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(commit=False)

            product.company = company

            product.save()

            return redirect('/my-products/')

    else:

        form = ProductForm()

    return render(request, 'products/add_product.html', {
        'form': form
    })


@login_required
def my_products(request):

    # Только firma / sales
    if request.user.role not in ['company', 'sales']:

        return redirect('/dashboard/')

    # Компания пользователя
    if request.user.role == 'company':

        company = request.user.owned_company

    else:

        company = request.user.company

    products = Product.objects.filter(
        company=company
    ).select_related('category')

    return render(request, 'products/my_products.html', {
        'products': products
    })


@login_required
def edit_product(request, pk):

    # Только firma / sales
    if request.user.role not in ['company', 'sales']:

        return redirect('/dashboard/')

    # Компания пользователя
    if request.user.role == 'company':

        company = request.user.owned_company

    else:

        company = request.user.company

    product = get_object_or_404(
        Product,
        pk=pk,
        company=company
    )

    # Редактирование
    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect('/my-products/')

    else:

        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product,
    })


@login_required
def delete_product(request, pk):

    # Только firma / sales
    if request.user.role not in ['company', 'sales']:

        return redirect('/dashboard/')

    # Компания пользователя
    if request.user.role == 'company':

        company = request.user.owned_company

    else:

        company = request.user.company

    product = get_object_or_404(
        Product,
        pk=pk,
        company=company
    )

    # Удаление
    if request.method == 'POST':

        product.delete()

        return redirect('/my-products/')

    return render(request, 'products/delete_product.html', {
        'product': product
    })