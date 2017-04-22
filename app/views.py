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
            }
    })


# assumption: received in format 'dd/mm - dd/mm'
def get_url_rpr(week):
    return str(week).replace(' ', '')


def get_weeks():
    now = datetime.datetime.now()
    cur_day_code = (int(now.strftime('%u')) % 7) + 1
    cur_week_start = now - datetime.timedelta(days=cur_day_code - 1)
    cur_week_end = cur_week_start + datetime.timedelta(days=6)
    next_week_start = cur_week_end + datetime.timedelta(days=1)
    next_week_end = next_week_start + datetime.timedelta(days=6)
    cur_week = cur_week_start.strftime('%d/%m') + ' - ' + cur_week_end.strftime('%d/%m')
    next_week = next_week_start.strftime('%d/%m') + ' - ' + next_week_end.strftime('%d/%m')
    return cur_week, next_week


def week(request, week_date):
    dates = week_date.split('-')[0].split('/')
    start = datetime.date(2017, int(dates[1]), int(dates[0]))
    return render(request, 'week.html', {
        'lessons_sunday': models.Lesson.objects.filter(day=start),
        'lessons_monday': models.Lesson.objects.filter(day=start + datetime.timedelta(days=1)),
        'lessons_tuesday': models.Lesson.objects.filter(day=start + datetime.timedelta(days=2)),
        'lessons_wednesday': models.Lesson.objects.filter(day=start + datetime.timedelta(days=3)),
        'lessons_thursday': models.Lesson.objects.filter(day=start + datetime.timedelta(days=4)),
        'lessons_friday': models.Lesson.objects.filter(day=start + datetime.timedelta(days=5)),
        'lessons_saturday': models.Lesson.objects.filter(day=start + datetime.timedelta(days=2)),

        # 'b lessons': models.Lesson.objects.all().filter(),
        # 'cur_lessons': models.Lesson.object.filter(lesson__date__gt=CUR_WEEK_START)
    })
# Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline='Hello')
# select-class-sunday:anone
# select-class-monday:anone
# select-class-tuesday:10
# select-class-thursday:anone

# TODO handle multiple lessons
def register(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    lesson_pk = request.POST['choose-class']
    lesson = models.Lesson.objects.get(pk=lesson_pk)
    person, created = models.Person.objects.get_or_create(name=name, email=email, phone=phone)
    # check for room in class
    if lesson.num_enrolled > lesson.max_participants:
        waiting = models.Waiting(person=person, lesson=lesson)
        result = 'waiting.html'
        waiting.save()
    else:
        registration = models.Registration(person=person, lesson=lesson)
        result = 'enrolled.html'
        lesson.num_enrolled += 1
        registration.save()
    lesson.save()
    return render(request, result)


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
        day = date_object + datetime.timedelta(days=int(lesson.day.strftime('%u')))
        time = lesson.time
        max_participants = lesson.max_participants
        # new_lesson, created = models.Person.objects.get_or_create(day=day, time=time, max_participants=max_participants, num_enrolled=0, regular=False)
        new_lesson = models.Lesson(day=day, time=time, max_participants=max_participants, num_enrolled=0, regular=False)
        new_lesson.save()
    return render(request, 'yay.html')


