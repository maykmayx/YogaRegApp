from django.contrib import admin
from . import models
from django.contrib.admin import DateFieldListFilter

# Register your models here.

admin.site.register(models.Person)


class RegistrationInline(admin.TabularInline):
    model = models.Registration
    list_display = 'name'

    def name(self):
        return self.person.name


class WaitingInline(admin.TabularInline):
    model = models.Waiting

@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [RegistrationInline, WaitingInline]
    exclude = ['code']
    list_display = ['day','time','num_enrolled','regular']

#  ⁠⁠⁠class InqAdmin(admin.ModelAdmin):
# list_display = ('name','company', 'email', 'subject','date')
#
# class JobAdmin(admin.ModelAdmin):
# list_display = ('headline','date_added', 'active')
#
# class NewsAdmin(admin.ModelAdmin):
# list_display = ('headline','date_added', 'active')
#
#
# admin.site.register(OnePager)
# admin.site.register(Platform)
# admin.site.register(Solution)
# admin.site.register(Solutions)
# admin.site.register(TeamMember)
# admin.site.register(About)
# admin.site.register(News,NewsAdmin)
# admin.site.register(JobPosition, JobAdmin)
# admin.site.register(Inquiry, InqAdmin)