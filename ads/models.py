from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=250)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    MEMBER = "member"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ROLES = [(MEMBER, "member"), (ADMIN, "admin"), (MODERATOR, "moderator")]

    role = models.CharField(max_length=20, choices=ROLES, default=MEMBER)
    age = models.SmallIntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name, self.last_name

    class Meta:
        ordering = ['username']


class ADS(models.Model):
    name = models.CharField(max_length=250, default='')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=500, default='')
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['name']


    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(ADS)

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"
        ordering = ['name']

    def __str__(self):
        return self.name

