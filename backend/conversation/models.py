from django.db import models
from authentication.models import Family

class Post(models.Model):
    family_id = models.ForeignKey(Family, related_name="post", on_delete=models.CASCADE, db_column="family_id")
    content = models.TextField(null=True)
    create_date = models.TimeField(auto_now_add=True)
    update_date = models.TimeField(auto_now=True)
    keyword = models.CharField(max_length=16, blank=True)
    emotion = models.IntegerField(null=True)

    class Meta:
        verbose_name = "posts"
        verbose_name_plural = "post"
        ordering = ("id",)

    def __str__(self):
        return self.keyword