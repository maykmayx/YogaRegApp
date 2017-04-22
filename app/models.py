from datetime import date, datetime

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=1024)
    email = models.EmailField()
    phone = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'%s' % (self.name)
    # def __str__(self):
    #     return self.name
    #

class Lesson(models.Model):
    day = models.DateField(null=True)
    time = models.CharField(max_length=1024)
    max_participants = models.IntegerField(default=10)
    num_enrolled = models.IntegerField(default=0, editable=False)
    regular = models.BooleanField(default=True)
    # code = models.CharField(max_length=1024, editable=False)

    # enrolled_list = models.ManyToManyField(Person, related_name='enrolled')
    # waiting_list = models.ManyToManyField(Person, related_name='waits')
    #
    # @property
    # def waiting_list(self):
    #     return list(self.waiting_list.all())
    #
    # @property
    # def enrolled_list(self):
    #     return list(self.enrolled_list.all())

    # (mod 7) + 1 to permute to hebrew schedule
    def get_day_num(self):
        temp = self.day.strftime('%u')
        return (temp % 7) + 1
    #
    # def __unicode__(self):
    #     date_formatted = self.day.strftime('%d') + '/' + self.day.strftime('%m')
    #     return date_formatted + ' @' + str(self.time)
    def __unicode__(self):
        date_formatted = self.day.strftime('%d') + '/' + self.day.strftime('%m')
        return date_formatted + ' @ u%s' % (self.time)

class Registration(models.Model):
    person = models.ForeignKey(Person)
    lesson = models.ForeignKey(Lesson)
    #
    # def __unicode__(self):
    #     return '%s registered for %s' % (self.person, self.lesson)


class Waiting(models.Model):
    person = models.ForeignKey(Person)
    lesson = models.ForeignKey(Lesson)

    # def __unicode__(self):
    #     return '%s waiting for %s' % (self.person, self.lesson)
