from datetime import date, datetime

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Person(models.Model):
    name = models.CharField(max_length=1024)
    email = models.EmailField()
    phone = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'%s' % (self.name)


class Lesson(models.Model):
    day = models.DateField(null=True)
    time = models.CharField(max_length=1024)
    max_participants = models.IntegerField(default=10)
    num_enrolled = models.IntegerField(default=0, editable=False)
    regular = models.BooleanField(default=True)

    def decrease_num(self):
        self.num_enrolled -=1


    # (mod 7) + 1 to permute to hebrew schedule
    def get_day_num(self):
        temp = self.day.strftime('%u')
        return (temp % 7) + 1

    def __unicode__(self):
        date_formatted = self.day.strftime('%d') + '/' + self.day.strftime('%m')
        return date_formatted + ' @%s' % (self.time)


class Registration(models.Model):
    person = models.ForeignKey(Person)
    lesson = models.ForeignKey(Lesson)
    #
    # def delete(self, **kwargs):
    #     self.lesson.decrease_num()
    #     super().delete()
    #     # self.delete()
    #     return


class Waiting(models.Model):
    person = models.ForeignKey(Person)
    lesson = models.ForeignKey(Lesson)


def remove_reg(sender, instance, **kwargs):
    reg = Registration.objects.get(pk=instance.pk)
    reg.lesson.num_enrolled -= 1

pre_delete.connect(remove_reg, sender=Registration)

