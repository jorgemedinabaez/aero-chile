import datetime
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Travel, Plane, Passenger, Profile, Contact
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
  
    # def __init__(self, *args, **kwargs):
    #     super(RegisterForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['placeholder'] = 'Nombre'
    #     self.fields['email'].widget.attrs['placeholder'] = 'Email'
    #     self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
    #     self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Email',
            'password1': False,
            'password2': False,
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
        label=''
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label=''
        )

class PassRecoverForm(forms.Form):
    email = forms.EmailField(label='Email', max_length= 50)

class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['code', 'origin', 'destination', 'flight_date', 'planes_id']
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'example: ABCD'}),
            'origin': forms.Select(attrs={'placeholder': 'Origen de vuelo'}),
            'destination': forms.Select(attrs={'placeholder': 'Destino de viaje'}),
            'flight_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Fecha de vuelo'}),
            'planes_id': forms.Select(attrs={'placeholder': 'Id avión'}),
        }
        labels = {
            'code': 'Código de vuelo',
            'origin': 'Origen',
            'destination': 'Destino',
            'flight_date': 'Fecha',
            'planes_id': 'Id del avión',
        }

class PlaneForm(forms.ModelForm):
    class Meta:
        model = Plane
        fields = ['model', 'capacity']
        widgets = {
            'model': forms.TextInput(attrs={'placeholder': 'Modelo'}),
            'capacity': forms.TextInput(attrs={'placeholder': 'Capacidad máxima'}),
        }
        labels = {
            'model': 'Modelo',
            'capacity': 'Capacidad máxima',
        }

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'birth', 'rut', 'vaccine', 'travels_id']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre y apellido'}),
            'birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de nacimiento'}),
            'rut': forms.TextInput(attrs={'placeholder': 'ejemplo: 1.234.567-8'}),
            'vaccine': forms.Select(attrs={'placeholder': 'Esquema de vacunación'}),
            'travels_id': forms.Select(attrs={'placeholder': 'Código de vuelo'}),

        }
        labels = {
            'name': False,
            'birth': 'Fecha de nacimiento',
            'rut': 'RUT',
            'vaccine': 'Esquema vacunación',
            'travels_id': 'Código de vuelo',
        }
    
    def clean_birth(self):
        birth_date = self.cleaned_data.get('birth')
        if birth_date and birth_date >= datetime.date.today():
            raise ValidationError('La fecha de nacimiento debe ser una fecha pasada.')
        return birth_date

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Email',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de nacimiento'}),
        }
        labels = {
            'first_name': False,
            'last_name': False,
            'birth': 'Fecha de nacimiento',
        }

    def clean_birth(self):
        birth_date = self.cleaned_data.get('birth')
        if birth_date and birth_date >= datetime.date.today():
            raise ValidationError('La fecha de nacimiento debe ser una fecha pasada.')
        return birth_date
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre y apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Asunto'}),
            'message': forms.Textarea(attrs={'placeholder': 'Mensaje', 'rows': 4}),
        }
        labels = {
            'name': False,
            'email': False,
            'subject': False,
            'message': False,
        }

