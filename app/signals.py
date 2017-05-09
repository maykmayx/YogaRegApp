from django.db.models import signals
from django.dispatch import dispatcher

def update_count(sender, instance, signal, *args, **kwargs):
  """
  Runs through all the lessons and updates their num enrolled field
  """

  try:
      instance.lesson.update_num_enrolled()
  except:
      print("error: can't update lesson num_enrolled")
