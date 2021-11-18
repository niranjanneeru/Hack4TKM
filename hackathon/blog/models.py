from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"


class Blog(models.Model):
    author = models.CharField(max_length=50)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    rating = models.PositiveSmallIntegerField(default=0)
    platform = models.CharField(max_length=10, default="medium")
    image_link = models.URLField(max_length=500)
    tags = models.ManyToManyField(Tags)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title
