from django.db import models


class Blog(models.Model):
    author = models.CharField(max_length=50)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    rating = models.PositiveSmallIntegerField()
    platform = models.CharField(max_length=10)

    def __str__(self):
        return self.title
