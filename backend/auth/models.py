from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_senior = models.BooleanField(default=False)
    phone_number = models.CharField("핸드폰번호", max_length=20, null=True)
    birth = models.DateField("생년월일", null=True)