from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(ResearchReport)
admin.site.register(PublicationReport)
admin.site.register(PaperPresentationReport)
admin.site.register(PatentReport)
admin.site.register(TrainingReport)
admin.site.register(ExtensionReport)
admin.site.register(PartnershipReport)
admin.site.register(OtherResearchReport)
admin.site.register(OthersReport)
