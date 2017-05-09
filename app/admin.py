from django.contrib import admin
from . import models
from django.contrib.admin import DateFieldListFilter

# Register your models here.

admin.site.register(models.Person)

#
# def deleteReg():
#     return


class RegistrationInline(admin.TabularInline):
    model = models.Registration
    list_display = ('person',)


class WaitingInline(admin.TabularInline):
    model = models.Waiting


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [RegistrationInline, WaitingInline]
    exclude = ('code',)
    list_display = ('day', 'time', 'num_enrolled', 'regular', 'full')
    date_hierarchy = 'day'
    list_filter = (('day',DateFieldListFilter),)




