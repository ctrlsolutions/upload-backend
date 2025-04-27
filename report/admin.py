from django.contrib import admin
from .models import Form, Field, Response, ResponseDocument, Report, College, Department

# Register your models here.

admin.site.register(Form)
admin.site.register(Field)
admin.site.register(Response)
admin.site.register(ResponseDocument)
admin.site.register(Report)

admin.site.register(College)
admin.site.register(Department)