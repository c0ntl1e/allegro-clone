from django import forms
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()


class CompanyRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    company_name = forms.CharField(max_length=255)
    nip = forms.CharField(max_length=20)
    regon = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea)

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
    
    from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


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
            raise forms.ValidationError('Hasła muszą być identyczne.')

        return cleaned_data