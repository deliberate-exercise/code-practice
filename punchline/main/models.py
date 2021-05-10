from django.db import models

# Create your models here.
class Title(models.Model):
    title = models.CharField(max_length=200)
    sub = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Episode(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    seasonNum = models.IntegerField(null=False)
    epiNum = models.IntegerField(null=False)
    epiTitle = models.CharField(max_length=200)
    link = models.CharField(max_length=500)