from django.contrib import admin

# Register your models here.
from .models import Lead, Comment, LeadFile
admin.site.register(Lead)
admin.site.register(Comment)
admin.site.register(LeadFile)