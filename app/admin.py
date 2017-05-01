from django.contrib import admin
from . import models
from django.contrib.admin import DateFieldListFilter

# Register your models here.

admin.site.register(models.Person)


def deleteReg():
    return


class RegistrationInline(admin.TabularInline):
    model = models.Registration
    fields = ('person',)
    actions = [deleteReg]


class WaitingInline(admin.TabularInline):
    model = models.Waiting


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [RegistrationInline, WaitingInline]
    exclude = ('code','num_enrolled')
    list_display = ('day', 'time', 'num_enrolled', 'regular')
    date_hierarchy = 'day'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            if formset.deleted_objects:
                instance.num_enrolled -= 1
        # for obj in formset.deleted_objects:



#
# class Model2Inline(admin.TabularInline):
#     model = Model2
#
# class Model1Admin(admin.ModelAdmin):
#     inlines = [Model2Inline]
#     def save_formset(self, request, form, formset, change):
#         super(Model1Admin, self).save_formset(self, request, form, formset, change)
#         if formset.model == Model2:
#             obj = formset.instance
#             if obj.reformat:
#                 obj.model2.all().delete()
#                 # creating new objects
#
#             obj.save()