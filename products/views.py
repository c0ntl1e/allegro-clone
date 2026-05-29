from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm
from django.core.paginator import Paginator

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

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if query:
        products = products.filter(
            name__icontains=query
        )

    if category and category != 'None':
        products = products.filter(
            category_id=category
        )

    if company and company != 'None':
        products = products.filter(
            company_id=company
        )

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    if sort == 'price_asc':

        products = products.order_by('price')

    elif sort == 'price_desc':

        products = products.order_by('-price')

    elif sort == 'oldest':

        products = products.order_by('id')

    else:

        products = products.order_by('-id')

    category_counts = {}

    for cat in categories:

        category_counts[cat.id] = Product.objects.filter(
            category=cat
        ).count()

    paginator = Paginator(products, 8)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'products/homepage.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'companies': companies,
        'category_counts': category_counts,
        'query': query,
        'selected_category': category,
        'selected_company': company,
        'selected_sort': sort,
        'min_price': min_price,
        'max_price': max_price,
    })


from django.core.paginator import Paginator

def product_list(request):

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

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if query:
        products = products.filter(
            name__icontains=query
        )

    if category and category != 'None':
        products = products.filter(
            category_id=category
        )

    if company and company != 'None':
        products = products.filter(
            company_id=company
        )

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    if sort == 'price_asc':
        products = products.order_by('price')

    elif sort == 'price_desc':
        products = products.order_by('-price')

    elif sort == 'oldest':
        products = products.order_by('id')

    else:
        products = products.order_by('-id')

    category_counts = {}

    for cat in categories:
        category_counts[cat.id] = Product.objects.filter(
            category=cat
        ).count()

    paginator = Paginator(products, 8)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'products/product_list.html',
        {
            'products': page_obj,
            'page_obj': page_obj,
            'categories': categories,
            'companies': companies,
            'category_counts': category_counts,
            'query': query,
            'selected_category': category,
            'selected_company': company,
            'selected_sort': sort,
            'min_price': min_price,
            'max_price': max_price,
        }
    )


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