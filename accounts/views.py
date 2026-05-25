from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from bs4 import BeautifulSoup

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

    # очистка NIP
    nip = nip.replace('-', '').replace(' ', '')

    url = (
        "https://aplikacja.ceidg.gov.pl/"
        "CEIDG/CEIDG.Public.UI/Search.aspx"
    )

    params = {
        'nip': nip
    }

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        html = response.text

        print(html)

        # если фирма не найдена
        if "Brak wpisów spełniających podane kryteria" in html:

            return JsonResponse({
                'error': 'Firma nie istnieje'
            }, status=404)

        soup = BeautifulSoup(
            html,
            'html.parser'
        )

        company_name = ''
        regon = ''

        # поиск названия фирмы
        links = soup.find_all('a')

        for link in links:

            text = link.get_text(strip=True)

            if text and len(text) > 5:

                company_name = text
                break

        # поиск REGON
        body_text = soup.get_text()

        if 'REGON' in body_text:

            lines = body_text.splitlines()

            for i, line in enumerate(lines):

                if 'REGON' in line and i + 1 < len(lines):

                    regon = lines[i + 1].strip()
                    break

        return JsonResponse({
            'name': company_name,
            'regon': regon,
            'address': '',
        })

    except Exception as e:

        print(e)

        return JsonResponse({
            'error': str(e)
        }, status=500)