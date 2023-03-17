from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, RegexValidator

from ads.validators import check_birth_date


class Category(models.Model):
    name = models.CharField(max_length=250, default='')
    slug = models.SlugField(max_length=10, validators=[MinLengthValidator(5), MaxLengthValidator(10)], unique=True)

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
    age = models.SmallIntegerField(null=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True, blank=True,
                              validators=[RegexValidator(regex="@rambler.ru",
                                                        inverse_match=True,
                                                        message="Регистрация с домена rambler.ru запрещена!"
                                                        )])
    birth_date = models.DateField(null=True, blank=True, validators=[check_birth_date])

    def __str__(self):
        return self.first_name, self.last_name

    class Meta:
        ordering = ['username']


class ADS(models.Model):
    name = models.CharField(max_length=250, default='', blank=False, validators=[MinLengthValidator(10)])
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=500, default='', blank=True)
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

