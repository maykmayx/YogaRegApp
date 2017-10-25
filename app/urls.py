from django.conf.urls import url
from . import views
app_name = 'app'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<week_date>\d+/\d+-\d+/\d+)', views.week, name='week'),
    url(r'^register$', views.register, name='register'),
    url(r'^create_lessons$', views.create_lessons, name='create_lessons'),
    url(r'^create$', views.submit_lessons, name='create')
]

#url pattern for dates: dd/mm-dd/mm   \d+/\d+-\d+/\d+
[]

