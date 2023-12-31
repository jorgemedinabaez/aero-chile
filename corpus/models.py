from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Plane(models.Model):
    id = models.AutoField(primary_key=True)
    # 'model' será el identificador de cada avión ingresado.
    model = models.CharField(max_length=45, unique=True, blank=False, null=False, default= 'A320 Neo - ', verbose_name='Modelo avión')
    # se agrega atributo 'capacity', para agregar la cantidad de pasajeros que pueda transportar el avión. Este campo es necesario en caso de agregar aviones con una capacidad mayor o menor a 'default'.
    capacity = models.IntegerField(default=140, verbose_name='Capacidad avión')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    update = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Avión'
        verbose_name_plural = 'Aviones'
        ordering = ['-created']
   
    def __str__(self):
        return self.model
    
STATE_CHOICES =[('Agendado','Agendado'),('Completado','Completado')] 

CITY_CHOICES =[
    ('Santiago','Santiago - Chile'),
    ('Lima','Lima - Perú'),
    ('Buenos Aires','Buenos Aires - Argentina'),
    ('La Paz','La Paz - Bolivia'),
    ('Quito','Quito - Ecuador'),
]

class Travel(models.Model):
    id = models.AutoField(primary_key=True)
    # 'code' es el código que posee el viaje.
    code = models.CharField(max_length=45, unique=True, blank= False, verbose_name='Código de vuelo')
    # la ciudad de origen y la de destino no deben ser las mismas.
    origin = models.CharField(max_length=45, choices=CITY_CHOICES, default='Seleccione origen', blank=False, verbose_name='Origen de vuelo')
    destination = models.CharField(max_length=45, choices=CITY_CHOICES, default='Seleccione destino', blank=False, verbose_name='Destino de viaje')
    flight_date = models.DateTimeField(blank=False, null=False, verbose_name='Fecha de vuelo')
    # 'current_city' trabajará con los atributos 'origin' y 'destination' para llenar su campo, sumado al atributo 'state', que se encargará de decirnos si corresponde uno u otro atributo, dependiendo del estado ('completado' [destination] o 'agendado' [origin]).
    current_city = models.CharField(max_length=45, verbose_name='Ciudad actual')
    state = models.CharField(max_length=45, choices=STATE_CHOICES, default='Agendado')
    planes_id = models.ForeignKey(Plane, on_delete=models.CASCADE, verbose_name='Id avión')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    update = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Vuelo'
        verbose_name_plural = 'Vuelos'
        ordering = ['-created']
   
    def __str__(self):
        return self.code

# al seleccionar la categoría 'Otra', falta generar un cuadro que permita que el operario escriba la vacuna inoculada.  
VACCINE_CHOICES = [
    ('Sinovac','Sinovac'),
    ('Pfizer','Pfizer'),
    ('Cancino','Cancino'),
    ('Astrazéneca','Astrazéneca'),
    ('Otra','Otra'),
]

class Passenger(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=False, null=False, verbose_name='Nombre pasajero')
    rut = models.CharField(max_length=45, blank=False, null=False, verbose_name='RUT')
    vaccine = models.CharField(max_length=45, choices=VACCINE_CHOICES, blank=False, null=False, verbose_name='Esquema vacunación')
    birth = models.DateField(null=False, blank=False, verbose_name='Fecha de nacimiento')
    travels_id = models.ForeignKey(Travel, on_delete=models.CASCADE, verbose_name='Id vuelo')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    update = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Pasajero'
        verbose_name_plural = 'Pasajeros'
        ordering = ['-created']
   
    def __str__(self):
        return self.name

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45, blank=False, null=False, verbose_name='Nombres')
    last_name = models.CharField(max_length=45, blank=False, null=False, verbose_name='Apellidos')
    birth = models.DateField(null=True, blank=False, verbose_name='Fecha de nacimiento')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    update = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['-created']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def formatted_birth(self):
        if self.birth:
            return self.birth.strftime('%Y-%m-%d')
        return None

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=False, null=False, verbose_name='Nombre y apellido')
    email = models.EmailField(blank=False, null=False, verbose_name='Email')
    subject = models.CharField(max_length=45, blank=False, null=False, verbose_name='Asunto')
    message = models.TextField(blank=False, null=False, verbose_name='Mensaje')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    update = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['-created']
    
    def __str__(self):
        return self.name