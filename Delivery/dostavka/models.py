from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey('Cafe', on_delete=models.CASCADE)
    phone = models.CharField(max_length=18)

    STATUS_CHOICES = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('On order', 'On order'),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='Offline')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Courier.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.courier.save()


class Cafe(models.Model):
    address = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.IntegerField(null=True, blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")


class Order(models.Model):
    client_address = models.CharField(max_length=255),
    client_phone = models.CharField(max_length=25),
    courier = models.ForeignKey(Courier, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=400, null=True, blank=True)

    STATUS_CHOICES = (
        ('Accept', 'Accept'),
        ('Confirmed', 'Confirmed'),
        ('Ready for delivery', 'Ready for delivery'),
        ('On way', 'On way'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    )

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Accept')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.OrderItem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order} -- {self.product} -- {self.quantity}'

    def get_cost(self):
        return self.product.price * self.quantity
