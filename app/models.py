from datetime import date, datetime

from django.db import models
from django.db.models import signals
from app.signals import update_count

class Person(models.Model):
    name = models.CharField(max_length=1024)
    email = models.EmailField()
    phone = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'%s' % (self.name)

class Registration(models.Model):
    person = models.ForeignKey(Person)
    lesson = models.ForeignKey('Lesson')

    def __unicode__(self):
        return self.person.name


class Waiting(models.Model):
    person = models.ForeignKey(Person)
    lesson = models.ForeignKey('Lesson')

    def __unicode__(self):
        return self.person.name



class Lesson(models.Model):
    day = models.DateField(null=True)
    time = models.CharField(max_length=1024)
    max_participants = models.IntegerField(default=10)
    regular = models.BooleanField(default=True)
    num_enrolled = models.IntegerField(default=0, editable=False)

    # make num_enrolled update with number of registrations
    def update_num_enrolled(self):
        count = self.registration_set.count()
        self.num_enrolled = count
        self.save()


    # enrolled = models.ManyToManyField(Registration, related_name='enrolls')
    # waitings = models.ManyToManyField(Waiting, related_name='waits')

    # @property
    # def waiting_list(self):
    #     return list(self.waitings.all())
    #
    # @property
    # def enrolled_list(self):
    #     return list(self.enrolled.all())

    def decrease_num(self):
        self.num_enrolled -= 1



    # (mod 7) + 1 to permute to hebrew schedule
    def get_day_num(self):
        temp = self.day.strftime('%u')
        return int((temp % 7) + 1)

    def __unicode__(self):
        date_formatted = self.day.strftime('%d') + '/' + self.day.strftime('%m')
        return date_formatted + ' @%s' % self.time


# Rerun the totals for each ChangeType whenever a Change is saved or deleted.
signals.post_save.connect(update_count, sender=Registration)
signals.post_delete.connect(update_count, sender=Registration)