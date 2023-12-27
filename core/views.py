from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Travel, Passenger, Plane


# Create your views here.


def home(request):
    travels = Travel.objects.all()
    context = {
        'travels':travels
    }
    return render(request,'core/home.html', context)

def register(request):
    if request.method == 'GET':
        return render(request,'core/register.html', {
        'form':UserCreationForm
    })
        # print('Enviando formulario')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
            # Formulario de registro
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                # return HttpResponse('Usuario creado satisfactoriamente')
                return redirect('task')
            except IntegrityError:
                # return HttpResponse('El usuario ya existe')
                return render(request,'core/register.html', {
                    'form':UserCreationForm,
                    'error':'El usuario ya existe'
                })
        # print(request.POST)
        # print('Obteniendo datos')
        # return HttpResponse('Las contraseñas no coinciden')
        return render(request,'core/register.html', {
            'form':UserCreationForm,
            'error':'Las contraseñas no coinciden'
        }) 
   
def task(request):
    return render(request, 'core/task.html')

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'core/login.html', {
            'form':AuthenticationForm,
        })
    else:
        # Con el 'print' nos aseguramos de que el query aparezca en la consola:
        # print(request.POST)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'core/login.html', {
                'form':AuthenticationForm,
                'error': 'Nombre de usuario y/o contraseña incorrectos'
            })
        else:
            login(request, user)
        # En el siguiente 'redirect', podría retornar el usuario al 'home' con las opciones extra que aparecen cuando un usuario se encuentra autenticado.
            return redirect('home')

        # return render(request, 'core/login.html', {
        #     'form':AuthenticationForm,
        # })

def sign_out(request):
    logout(request)
    return redirect('login')

def add_travel(request):
    return render(request,'core/add_travel.html')

def add_travel_register(request):
    codigo = request.POST['code']
    origen = request.POST['origin']
    destino = request.POST['destination']
    fecha_vuelo = request.POST['flight_date']
    avion = request.POST['planes_id']
    plane = Plane.objects.get(model=avion)
    flight = Travel(code=codigo, origin=origen, destination=destino, flight_date=fecha_vuelo, planes_id=plane)
    flight.save()
    return render(request, 'core/add_travel_register')

def add_passenger(request):
    return render(request,'core/add_passenger.html')

def add_passenger_register(request):
    nombre = request.POST['name']
    nacimiento = request.POST['birth']
    vacuna = request.POST['vaccine']
    rut = request.POST['rut']
    passenger = Passenger(name=nombre, birth=nacimiento, vaccine=vacuna, rut=rut)
    passenger.save()
    return render(request, 'core/add_passenger_register')