from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    real_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=[("F", "여자"), ("M", "남자")])
    cold_sensitivity = models.CharField(
        max_length=10, choices=[("민감", "민감"), ("보통", "보통"), ("둔감", "둔감")]
    )
    heat_sensitivity = models.CharField(
        max_length=10, choices=[("민감", "민감"), ("보통", "보통"), ("둔감", "둔감")]
    )

    def __str__(self):
        return f"{self.user.username}님의 프로필"
