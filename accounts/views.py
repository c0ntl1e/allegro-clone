from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CompanyRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm
from .models import User

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
            employee.set_password(form.cleaned_data['password1'])
            employee.save()

            return redirect('/employees/')
    else:
        form = EmployeeForm()

    return render(request, 'accounts/add_employee.html', {
        'form': form
    })