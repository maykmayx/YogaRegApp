from django.contrib import admin
from . import models
from django.contrib.admin import DateFieldListFilter

# Register your models here.

admin.site.register(models.Person)


class RegistrationInline(admin.TabularInline):
    model = models.Registration

class WaitingInline(admin.TabularInline):
    model = models.Waiting

@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [RegistrationInline, WaitingInline]
    exclude = ['code']

