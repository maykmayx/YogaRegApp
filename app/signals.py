from django.db.models import signals
from django.dispatch import dispatcher


def update_count(sender, instance, signal, *args, **kwargs):
  """
  Runs through all the lessons and updates their num enrolled field
  """
  from app.models import Lesson
  for lesson in Lesson.objects.all():
    lesson.update_num_enrolled()

