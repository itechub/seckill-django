import datetime
from django.utils import timezone
from django.test import TransactionTestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError
from seckill.models import Product, Activity, Order


class ProductModelsTest(TransactionTestCase):
    def test_can_save_product(self):
        product = Product.objects.create(name="productA", inventory=6)
        self.assertIn(product, Product.objects.all())

    def test_cannot_save_nagative_inventory(self):
        with self.assertRaises(DataError):
            Product.objects.create(name="productA", inventory=-6)
        product = Product.objects.create(name="productA", inventory=6)
        # Only the valid product info being saved
        self.assertEqual(product.inventory, 6)
        self.assertEqual(Product.objects.count(), 1)

    def test_cannot_save_duplicat_product(self):
        Product.objects.create(name="productA", inventory=6)
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="productA", inventory=6)
        self.assertEqual(Product.objects.count(), 1)


class ActivityModelsTest(TransactionTestCase):
    def test_can_save_activity(self):
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(minutes=10)
        _product = Product.objects.create(name="productA", inventory=6)
        Activity.objects.create(
            name="seckill",
            product=_product,
            start_time=start_time,
            end_time=end_time,
        )
        self.assertEqual(Activity.objects.count(), 1)

    def test_cannot_save_invalid_start_end_time(self):
        start_time = timezone.now()
        end_time = start_time - datetime.timedelta(minutes=10)
        _product = Product.objects.create(name="productA", inventory=6)
        with self.assertRaises(ValidationError):
            Activity.objects.create(
                name="seckill",
                product=_product,
                start_time=start_time,
                end_time=end_time,
            )
        self.assertEqual(Activity.objects.count(), 0)

    def activity_status_helper(self, product, start_time, time_delta, status):
        end_time = start_time + time_delta
        activity = Activity.objects.create(
            name="seckill",
            product=product,
            start_time=start_time,
            end_time=end_time,
        )
        self.assertEqual(activity.get_status(), status)

    def test_activity_status(self):
        start_time = timezone.now()
        timedelta = datetime.timedelta(minutes=10)
        product = Product.objects.create(name="productA", inventory=6)
        self.activity_status_helper(product, start_time, timedelta, "RUNNING")
        self.activity_status_helper(
            product, start_time + timedelta, timedelta, "PREPARING"
        )
        self.activity_status_helper(
            product, start_time - timedelta, timedelta, "OVER"
        )


class OrderModelTest(TransactionTestCase):
    def get_activity(self, inventory=10):
        _product = Product.objects.create(name="seckill", inventory=inventory)
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(minutes=10)
        return Activity.objects.create(
            name="seckill",
            product=_product,
            start_time=start_time,
            end_time=end_time,
        )

    def test_can_save_order(self):
        uuid = 10086
        Order.objects.create(uuid=uuid, activity=self.get_activity())
        self.assertEqual(Order.objects.count(), 1)

    # 同一用户不能重复下单
    def test_cannot_save_duplicate_order(self):
        _activity = self.get_activity()
        uuid = 10086
        Order.objects.create(uuid=uuid, activity=_activity)
        with self.assertRaises(ValidationError):
            Order.objects.create(uuid=uuid, activity=_activity)
        self.assertEqual(Order.objects.count(), 1)

    # 不同用户可以针对统一商品进行下单
    def test_different_user_can_corresponding_order(self):
        _activity = self.get_activity()
        uuidA = 10086
        Order.objects.create(uuid=uuidA, activity=_activity)
        uuidB = 10087
        Order.objects.create(uuid=uuidB, activity=_activity)
        self.assertEqual(Order.objects.count(), 2)

    # 当秒杀库存为 0 时，不能下单
    def test_cannot_save_when_inventory_is_empty(self):
        _activity = self.get_activity(0)
        uuidA = 10086
        with self.assertRaises(ValidationError):
            Order.objects.create(uuid=uuidA, activity=_activity)
        self.assertEqual(Order.objects.count(), 0)
