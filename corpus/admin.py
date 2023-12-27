from django.contrib import admin
from .models import Plane, Travel, Passenger

# Register your models here.

admin.site.register(Plane)
admin.site.register(Travel)
admin.site.register(Passenger)
