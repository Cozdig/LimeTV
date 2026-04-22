from django.db import models

# Create your models here.
class Channel(models.Model):
    channel_name = models.CharField(max_length=100, verbose_name="название канала")

class Program(models.Model):
    channel_name = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="programs", verbose_name="название канала")
    date = models.DateField(verbose_name="дата")
    program_id = models.IntegerField(verbose_name="id программы")
    duration = models.IntegerField(verbose_name="длительность")
    title = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(null=True, verbose_name="описание")
    age_rating = models.IntegerField(verbose_name="возрастной рейтинг")
    sub_title = models.CharField(max_length=200, null=True, verbose_name="серия, название серии")
    category = models.TextField(verbose_name="категории")
    start_time = models.DateTimeField(verbose_name="время начала")
    priority = models.FloatField(default=0.0, verbose_name="приоритет программы")
    premier = models.BooleanField(null=True, verbose_name="премьера")