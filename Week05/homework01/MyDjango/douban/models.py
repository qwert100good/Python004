from django.db import models

# Create your models here.
class Comments(models.Model):
    movie_name = models.CharField(max_length=20)
    shorts = models.CharField(max_length=400)
    stars = models.IntegerField()
    votes = models.IntegerField()
    sentiments = models.DecimalField(max_digits=8, decimal_places=6)
    comment_time = models.DateField()

    class Meta:
        managed = True
        db_table = 'comments'
