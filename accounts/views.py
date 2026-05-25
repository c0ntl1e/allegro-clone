from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import CompanyRegistrationForm, EmployeeForm
from .models import User

import requests


def register_company(request):

    if request.method == 'POST':

        form = CompanyRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('/dashboard/')

    else:

        form = CompanyRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


@login_required
def dashboard(request):

    return render(request, 'accounts/dashboard.html')


@login_required
def employees(request):

    if request.user.role != 'company':
        return redirect('/dashboard/')

    employees = User.objects.filter(
        role='sales',
        company=request.user.owned_company
    )

    return render(request, 'accounts/employees.html', {
        'employees': employees
    })


@login_required
def add_employee(request):

    if request.user.role != 'company':
        return redirect('/dashboard/')

    if request.method == 'POST':

        form = EmployeeForm(request.POST)

        if form.is_valid():

            employee = form.save(commit=False)

            employee.role = 'sales'
            employee.company = request.user.owned_company

            employee.set_password(
                form.cleaned_data['password1']
            )

            employee.save()

            return redirect('/employees/')

    else:

        form = EmployeeForm()

    return render(request, 'accounts/add_employee.html', {
        'form': form
    })


def get_company_data(request):

    nip = request.GET.get('nip')

    if not nip:
        return JsonResponse({
            'error': 'Brak NIP'
        }, status=400)

    nip = nip.replace('-', '').replace(' ', '')

    url = (
        "https://nowe-firmy-ceidg-api.p.rapidapi.com/api/v1/future-companies"
    )

    headers = {
        "x-rapidapi-key": "fad7f1785cmsh4a819a5441c132bp15a35djsn9b96c5c809bb",
        "x-rapidapi-host": "nowe-firmy-ceidg-api.p.rapidapi.com"
    }

    params = {
        "page": 1,
        "limit": 20
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        print(response.status_code)
        print(response.text)

        data = response.json()

        companies = data.get('data', [])

        found_company = None

        for company in companies:

            company_nip = str(
                company.get('nip', '')
            ).replace('-', '').replace(' ', '')

            if company_nip == nip:

                found_company = company
                break

        if not found_company:

            return JsonResponse({
                'error': 'Firma nie istnieje'
            }, status=404)

        return JsonResponse({
            'name': found_company.get('companyName', ''),
            'regon': found_company.get('regon', ''),
            'address': found_company.get('address', ''),
        })

    except Exception as e:

        print(e)

        return JsonResponse({
            'error': 'Błąd RapidAPI'
        }, status=500)