import factory

from ads.models import User, Category, ADS


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("ean", length=7)

class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ADS

    name = factory.Faker("name")
    category_id = factory.SubFactory(CategoryFactory)
    author_id = factory.SubFactory(UserFactory)
    price = 1000
    
