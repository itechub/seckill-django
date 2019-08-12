from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=600, null=True)
    price = models.FloatField(default=0)
    inventory = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=250)
    product = models.ForeignKey(
        Product, verbose_name="product_id", on_delete=models.DO_NOTHING
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def get_status(self):
        now = timezone.now()
        if self.start_time >= now:
            return "PREPARING"
        elif self.end_time <= now:
            return "OVER"
        else:
            return "RUNNING"

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(
                ("start_time should be earlier than end_time")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Activity, self).save(*args, **kwargs)


class Order(models.Model):
    uuid = models.SmallIntegerField()
    activity = models.ForeignKey(
        Activity, verbose_name="activity_id", on_delete=models.DO_NOTHING
    )
    payment = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("uuid", "activity")

    def clean(self):
        if self.activity.product.inventory <= 0:
            raise ValidationError(("product inventory is empty"))

    def __str__(self):
        return str(self.uuid) + str(self.activity.id)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Order, self).save(*args, **kwargs)
