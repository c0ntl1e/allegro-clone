from django import forms
from django.contrib.auth import get_user_model
from companies.models import Company
import requests

User = get_user_model()


class CompanyRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    company_name = forms.CharField(
        max_length=255,
        required=False
    )

    nip = forms.CharField(max_length=20)

    regon = forms.CharField(
        max_length=20,
        required=False
    )

    address = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    def clean_nip(self):
        nip = self.cleaned_data['nip']

        # Удаляем пробелы и тире
        nip = nip.replace('-', '').replace(' ', '')

        # Проверка длины
        if len(nip) != 10:
            raise forms.ValidationError(
                'NIP musi mieć 10 cyfr.'
            )

        # Проверка существует ли фирма
        url = f"https://dane.biznes.gov.pl/api/ceidg/v3/firma?nip={nip}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise forms.ValidationError(
                    'Nie znaleziono firmy o podanym NIP.'
                )

            data = response.json()

            if not data:
                raise forms.ValidationError(
                    'Firma nie istnieje.'
                )

        except requests.RequestException:
            raise forms.ValidationError(
                'Błąd połączenia z bazą CEIDG.'
            )

        return nip

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role='company'
        )

        company = Company.objects.create(
            name=self.cleaned_data['company_name'],
            nip=self.cleaned_data['nip'],
            regon=self.cleaned_data['regon'],
            address=self.cleaned_data['address'],
            owner=user
        )

        return user


class EmployeeForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Powtórz hasło',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email']

        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'Adres e-mail',
        }

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError(
                'Hasła muszą być identyczne.'
            )

        return cleaned_data