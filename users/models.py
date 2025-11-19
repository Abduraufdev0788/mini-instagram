from django.db import models



class Users(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    image = models.ImageField(upload_to="avatars/", null=True, default="avatars/default.png")

    def __str__(self):
        return f"{self.id}.{self.first_name} - {self.last_name}"
    


class Profile(models.Model):
    JOB_CHOICES = [
        ("developer", "Dasturchi"),
        ("designer", "Dizayner"),
        ("teacher", "O‘qituvchi"),
        ("doctor", "Shifokor"),
        ("engineer", "Muhandis"),
        ("driver", "Haydovchi"),
        ("businessman", "Biznesmen"),
        ("bloger", "Bloger"),
        ("accountant", "Buxgalter"),
        ("student", "Talaba"),
    ]
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    jobs = models.CharField(choices=JOB_CHOICES, null=True, blank=True, default = "student")

    def __str__(self):
        return f"{id}. {Users.first_name}"
