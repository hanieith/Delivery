from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey('Cafe', on_delete=models.CASCADE)


class Cafe(models.Model):
    address = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.CharField(max_length=400)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Courier.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.courier.save()
