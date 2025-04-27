from django.contrib import admin
from .models import Form, Field, Response, ResponseDocument

# Register your models here.

admin.site.register(Form)
admin.site.register(Field)
admin.site.register(Response)
admin.site.register(ResponseDocument)