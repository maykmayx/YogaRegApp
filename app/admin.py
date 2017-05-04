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
    fields = ('person__name', 'person__email', 'person__phone')
    # actions = [deleteReg]
    # list_display = ('person__name',)


class WaitingInline(admin.TabularInline):
    model = models.Waiting


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [RegistrationInline, WaitingInline]
    exclude = ('code',)
    list_display = ('day', 'time', 'num_enrolled', 'regular')
    date_hierarchy = 'day'

    # def save_formset(self, request, form, formset, change):
    #     super(LessonAdmin).save_formset(request, form, formset, change)
    #     if formset.model == models.Registration:
    #         obj = formset.instance
    #         if obj.reformat:
    #             form.instance.num_enrolled -= 1
    #             obj.delete()
    #         obj.save()
    # def save_formset(self, request, form, formset, change):
    #     # super(LessonAdmin, self).save_formset(request, form, formset, change)
    #     instances = formset.save()
    #     for instance in instances:
    #         if instance.model == models.Lesson:
    #             instance.num_enrolled -= 1

    #     # #     obj.save()
    #     # for obj in formset.deleted_objects:
    #     #     obj.my_delete()
    #     #     # obj.save()
    #     # formset.save()
    # #         obj.lesson.num_enrolled -= 1
    # #     obj.save()
    #                     # creating new objects
    #     # instances = formset.save(commit=False)
    #     # for instance in instances:
    #     #     instance.save()
    #     # for obj in formset.deleted_objects:
    #     #     obj.lesson.num_enrolled -= 1
    #     #     obj.delete()



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