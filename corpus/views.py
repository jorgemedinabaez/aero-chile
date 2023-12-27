from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, PassRecoverForm, TravelForm, PlaneForm, PassengerForm, ProfileForm, CustomUserCreationForm, ContactForm
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Travel, Passenger, Profile
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator


# Create your views here.

# @login_required
def home(request):
    travels = Travel.objects.all()
    login = LoginForm()

    data = {
        'travels': travels,
        'login': login,
    }
    return render(request, 'corpus/home.html', data)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'corpus/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
                
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Credenciales inválidas. Inténtelo nuevamente"
                return render(request, 'corpus/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'corpus/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def recover_pass_view(request):
    if request.method == 'POST':
        form = PassRecoverForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                # Generar token para restablecer la contraseña
                token = default_token_generator.make_token(user)

                # Construir el enlace para restablecer la contraseña
                uid = force_str(urlsafe_base64_encode(force_bytes(user.pk)))
                reset_link = request.build_absolute_uri('/recover_confirm/{}/{}'.format(uid, token))

                # Enviar correo electrónico con el enlace para restablecer la contraseña
                email_subject = 'Solicitud de restablecimiento de contraseña'
                email_body = render_to_string('corpus/recover_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                send_mail(email_subject, email_body, 'operaciones@aerochile.com', [email])

                messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña.')
                return redirect('login')
            else:
                messages.error(request, 'No se encontró ninguna cuenta asociada a este correo electrónico.')
    else:
        form = PassRecoverForm()


    return render(request, 'corpus/recover_pass.html', {'form': form})

def recover_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Si el usuario y el token son válidos, permitir el cambio de contraseña
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
            # Procesar el cambio de contraseña
            # Aquí debes agregar el código para cambiar la contraseña del usuario
            # Ejemplo: user.set_password(nueva_contraseña)        
                messages.success(request, 'Contraseña restablecida con éxito.')
                return redirect('login')
        else:
            # return render(request, 'corpus/recover_confirm.html', {'uidb64': uidb64, 'token': token})
            form = SetPasswordForm(user)
        return render(request, 'corpus/recover_confirm.html', {'form': form})
    else:
        messages.error(request, 'El enlace para restablecer la contraseña es inválido o ha expirado.')
        return redirect('recover_pass')

def recover_email_view(request):
    return render(request, 'corpus/recover_email.html')

def add_travel_view(request):
    if request.method == 'POST':
        form = TravelForm(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            # Redirigir a una página de éxito o realizar alguna acción adicional
            return redirect('home')
    else:
        form = TravelForm()

    return render(request, 'corpus/add_travel.html', {'form': form})

# def travel_state_view(request):
#     if request.method == 'POST':
#         travel_id = request.POST.get('travel_id')
#         new_state = request.POST.get('new_state')

#         # Obtener el objeto Travel basado en travel_id
#         travel = Travel.objects.get(pk=travel_id)
#         travel.state = new_state
#         travel.save()

#         # Redirigir a la misma página (home.html) después de procesar la selección
#         return redirect('home')

#     # Si la solicitud no es POST, renderizar la plantilla inicial (template.html)
#     travels = Travel.objects.all()
#     return render(request, 'corpus/home.html', {'travels': travels})

def travel_state_view(request):
    if request.method == 'POST':
        travel_id = request.POST.get('travel_id')
        new_state = request.POST.get('new_state')

        # Obtener el objeto Travel basado en travel_id
        travel = get_object_or_404(Travel, pk=travel_id)

        if new_state == 'Completado':
            # Actualizar el campo 'origen' con la información de 'destino'
            travel.origin = travel.destination

            # Establecer 'destino' con el valor por defecto ('Seleccione destino')
            travel.destination = 'Nuevo destino'

        travel.state = new_state
        travel.save()

        # Redirigir a la misma página (home.html) después de procesar la selección
        return redirect('home')

    # Si la solicitud no es POST, renderizar la plantilla inicial (template.html)
    travels = Travel.objects.all()
    return render(request, 'corpus/home.html', {'travels': travels})

def add_plane_view(request):
    if request.method == 'POST':
        form = PlaneForm(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            messages.success(request, '¡Registro exitosamente realizado!')

            # Redirigir a una página de éxito o realizar alguna acción adicional
            return redirect('home')
    else:
        form = PlaneForm()

    return render(request, 'corpus/add_plane.html', {'form': form})

def add_passenger_view(request):
    if request.method == 'POST':

        try:
            # Obtener el ID del vuelo desde el formulario
            travel_id = request.POST.get('travels_id')
            # Obtener la instancia del vuelo correspondiente al ID
            travel_instance = Travel.objects.get(pk=travel_id)
        except Travel.DoesNotExist:
            messages.error(request, 'El vuelo seleccionado no existe')
            return redirect('add_passenger')
        
        # Asociar el ID del vuelo al crear una instancia del formulario de pasajeros
        passenger_form = PassengerForm(request.POST)
        if passenger_form.is_valid():
            # Guardar el formulario si es válido
            passenger = passenger_form.save(commit=False)
            passenger.travels_id = travel_instance  # Asociar el vuelo al pasajero
            passenger.save()

            messages.success(request, 'Pasajero agregado correctamente')
            return redirect('home')
        
        else:
            messages.error(request, 'Error al agregar el pasajero')
    else:
        passenger_form = PassengerForm()

    return render(request, 'corpus/add_passenger.html', {'passenger_form': passenger_form})

def travel_detail_view(request, travel_id):
    travel = get_object_or_404(Travel, pk=travel_id)
    passengers = Passenger.objects.filter(travels_id=travel)

    if request.method == 'POST':
        # Si se envía el formulario con datos actualizados
        form = TravelForm(request.POST, instance=travel)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cambios realizados exitosamente!')
            return redirect('home')
    else:
        travel.flight_date = travel.flight_date.strftime('%Y-%m-%dT%H:%M') if travel.flight_date else None
        # Si es una solicitud GET, se muestra el formulario con los datos existentes
        form = TravelForm(instance=travel)
        
    context = {
        'travel': travel,
        'form': form,
        'passengers': passengers,
    }

    return render(request, 'corpus/travel_detail.html', context)

def modify_passenger_view(request, passenger_id):
    passenger = get_object_or_404(Passenger, pk=passenger_id)

    if request.method == 'POST':
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cambios realizados exitosamente!')
            return redirect('travel_detail', travel_id=passenger.travels_id.id)
    else:
        form = PassengerForm(instance=passenger)
        # Modificar el valor del campo de fecha de nacimiento si existe
        if passenger.birth:
            form.initial['birth'] = passenger.birth.strftime('%Y-%m-%d')

    context = {
        'form': form,
        'passenger': passenger,
    }

    return render(request, 'corpus/modify_passenger.html', context)

def eliminate_passenger_view(request, passenger_id):
    passenger = get_object_or_404(Passenger, pk=passenger_id)

    if request.method == 'POST':
        # Elimina al pasajero
        passenger.delete()

        # Redirige a la página de detalles del viaje
        return redirect('travel_detail', travel_id=passenger.travels_id.id)
    
    return redirect('travel_detail', travel_id=passenger.travels_id)

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        register_form = CustomUserCreationForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if register_form.is_valid() and profile_form.is_valid():
            register_form.save()
            profile_form.save()
            messages.success(request, '¡Cambios realizados exitosamente!')
            return redirect('home')
    else:
        # Obtener los datos del formulario de registro
        register_form = CustomUserCreationForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

        # Verificar si hay una fecha de nacimiento almacenada en el perfil del usuario
        if profile.birth:
            # profile_form.fields['birth'].initial = profile.birth
            # profile_form.initial['birth'] = profile_form.birth.strftime('%Y-%m-%d')
             profile_form.initial['birth'] = profile.formatted_birth

    return render(
        request,
        'corpus/profile.html',
        {
            'register_form': register_form,
            'profile_form': profile_form,
            'profile': profile,
        }
    )

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            messages.success(request, '¡Mensaje enviado correctamente!')
            # Redirigir a una página de éxito o realizar alguna acción adicional
            return redirect('home')
    else:
        form = ContactForm()
    
    data = {
        'form':form,
    }

    return render(request, 'corpus/contact.html', data)

def support_view(request):

    return render(request, 'corpus/support.html')

def aeronova_view(request):

    return render(request, 'corpus/aeronova.html')
