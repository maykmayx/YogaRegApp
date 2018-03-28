import datetime
from django.db.models import F
from django.shortcuts import render, redirect
from . import models

CUR_WEEK_START = 0


# TODO maybe minimize dis
def index(request):
    weeks = get_weeks()
    cur_week = weeks[0]
    next_week = weeks[1]
    pesach = "09/04 - 15/04"
    return render(request, 'index.html', {
        'cur_week':
            {
                'dates': cur_week,
                'url_rpr': get_url_rpr(cur_week).strip('(').strip("\'")
            },
        'next_week':
            {
                'dates': next_week,
                'url_rpr': get_url_rpr(next_week)
            },
        'pesach_week': {  # TODO GET RID OF THS
            'dates': pesach,
            'url_rpr': get_url_rpr(pesach)
        }
    })


# assumption: received in format 'dd/mm - dd/mm'
def get_url_rpr(week):
    return str(week).replace(' ', '')


# 
def get_weeks():
    now = datetime.datetime.now()
    cur_day_code = (int(now.strftime('%u')) % 7) + 1
    if cur_day_code > 5:
        buffer = 8 - cur_day_code  # if friday add 2, if saturday add 1
        cur_week_start = now + datetime.timedelta(days=buffer)
    else:
        cur_week_start = now - datetime.timedelta(days=cur_day_code - 1)
    cur_week_end = cur_week_start + datetime.timedelta(days=6)
    next_week_start = cur_week_end + datetime.timedelta(days=1)
    next_week_end = next_week_start + datetime.timedelta(days=6)
    cur_week = cur_week_start.strftime('%d/%m') + ' - ' + cur_week_end.strftime('%d/%m')
    next_week = next_week_start.strftime('%d/%m') + ' - ' + next_week_end.strftime('%d/%m')
    return cur_week, next_week


def is_week_empty():

    return True

def week(request, week_date):
    year = year = datetime.date.today().year
    dates = week_date.split('-')[0].split('/')
    start = datetime.date(year, int(dates[1]), int(dates[0]))
    lessons_sunday = models.Lesson.objects.filter(day=start)
    lessons_monday = models.Lesson.objects.filter(day=start + datetime.timedelta(days=1))
    lessons_tuesday = models.Lesson.objects.filter(day=start + datetime.timedelta(days=2))
    lessons_wednesday = models.Lesson.objects.filter(day=start + datetime.timedelta(days=3))
    lessons_thursday = models.Lesson.objects.filter(day=start + datetime.timedelta(days=4))
    lessons_friday = models.Lesson.objects.filter(day=start + datetime.timedelta(days=5))
    lessons_saturday = models.Lesson.objects.filter(day=start + datetime.timedelta(days=6))
    empty_week = (not lessons_sunday.exists() and not lessons_monday.exists() and not lessons_tuesday.exists() and not lessons_wednesday.exists() and not lessons_thursday.exists() and not lessons_friday.exists() and not lessons_saturday.exists())
    return render(request, 'week.html', {
        'lessons_sunday': lessons_sunday,
        'lessons_monday': lessons_monday,
        'lessons_tuesday': lessons_tuesday,
        'lessons_wednesday': lessons_wednesday,
        'lessons_thursday': lessons_thursday,
        'lessons_friday': lessons_friday,
        'lessons_saturday': lessons_saturday,
        'cur_week': week_date,
        'empty_week': empty_week
    })


def register(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    lesson_pk = request.POST['choose-class']
    lesson = models.Lesson.objects.get(pk=lesson_pk)
    person, created = models.Person.objects.get_or_create(name=name, email=email, phone=phone)
    # check for room in class
    if lesson.num_enrolled >= lesson.max_participants:
        waiting = models.Waiting(person=person, lesson=lesson)
        waiting.save()
        # lesson.waitings.add(waiting)
        result = 'waiting.html'
    else:
        registration = models.Registration(person=person, lesson=lesson)
        registration.save()
        lesson.update_num_enrolled()
        # lesson.num_enrolled += 1
        # lesson.enrolled.add(registration)
        result = 'enrolled.html'


    lesson.save()
    lesson_rpr = lesson.__unicode__().split('@')
    return render(request, result, {
        'lesson_date': lesson_rpr[0],
        'lesson_time': lesson_rpr[1]
    })


def create_lessons(request):
    return render(request, 'createlessons.html')


# TODO check for doubles
# create new instances of the regularly scheduled lessons in a given week
# request returns the date for sunday in the target week
def submit_lessons(request):
    input_date = request.POST['date']
    date_object = datetime.datetime.strptime(input_date, '%Y-%m-%d')
    lessons = models.Lesson.objects.filter(regular=True)
    for lesson in lessons:
        day_code = lesson.day.strftime('%u')
        delta = (int(day_code) % 7) + 1
        day = date_object + datetime.timedelta(days=(delta - 1))
        time = lesson.time
        max_participants = lesson.max_participants
        new_lesson, created = models.Lesson.objects.get_or_create(day=day, time=time, max_participants=max_participants)
        new_lesson.save()

        for reg in models.Registration.objects.filter(lesson__pk=lesson.pk):
            new_reg = models.Registration.objects.create(lesson=new_lesson, person=reg.person)
            new_reg.save()
        # new_lesson = models.Lesson(day=day, time=time, max_participants=max_participants, num_enrolled=0, regular=False)
        new_lesson.save()

    return render(request, 'yay.html')


