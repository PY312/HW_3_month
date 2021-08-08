from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    descriptions = models.TextField()
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class ConfeirmCode(models.Model):
    code = models.CharField(max_length=12)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    valid_until=models.DateTimeField(null=True)

    def __str__(self):
        return self.code