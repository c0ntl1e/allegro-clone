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

    # Очистка NIP
    nip = nip.replace('-', '').replace(' ', '')

    url = (
        "https://dane.biznes.gov.pl/api/ceidg/v2/"
        f"firma?nip={nip}"
    )

    try:

        response = requests.get(
            url,
            headers={
                'Accept': 'application/json'
            },
            timeout=10
        )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            return JsonResponse({
                'error': 'Firma nie istnieje'
            }, status=404)

        data = response.json()

        firma = data.get('firma')

        if not firma:
            return JsonResponse({
                'error': 'Nie znaleziono firmy'
            }, status=404)

        address = ''

        adres = firma.get('adresDzialalnosci', {})

        if adres:

            parts = [
                adres.get('ulica', ''),
                adres.get('nrNieruchomosci', ''),
                adres.get('kodPocztowy', ''),
                adres.get('miejscowosc', ''),
            ]

            address = ' '.join(
                [p for p in parts if p]
            )

        return JsonResponse({
            'name': firma.get('nazwa', ''),
            'regon': firma.get('regon', ''),
            'address': address,
        })

    except Exception as e:

        print(e)

        return JsonResponse({
            'error': 'Błąd CEIDG API'
        }, status=500)