from django.contrib import admin
from . import models
from django.contrib.admin import DateFieldListFilter

# Register your models here.

admin.site.register(models.Person)

#
# def deleteReg(pk):
#     reg = models.Registration.objects.get(pk=pk)
#     reg.delete()
#     return


class RegistrationInline(admin.TabularInline):
    model = models.Registration
    fields = ('person',)
    # actions = [deleteReg]


class WaitingInline(admin.TabularInline):
    model = models.Waiting


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [RegistrationInline, WaitingInline]
    exclude = ('code',)
    list_display = ('day', 'time', 'num_enrolled', 'regular')
    date_hierarchy = 'day'

    def save_formset(self, request, form, formset, change):
        if formset.model == models.Registration:
            formset.instane.delete()


