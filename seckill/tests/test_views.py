import json
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from seckill.models import Product, Activity, Order
from seckill.serializers import (
    ActivitySerializer,
    ActivityInstanceSerializer,
    OrderSerializer,
)
from seckill.constants import SECKILL_CONSTANT


class ActivityTest(TestCase):
    def data_slug(
        self,
        activity_name="demo",
        product_name="seckill",
        inventory=10,
        status="RUNNING",
    ):
        _product = Product.objects.create(
            name=product_name, inventory=inventory
        )
        if status == "PREPARING":
            start_time = timezone.now() + timezone.timedelta(minutes=20)
        elif status == "RUNNING":
            start_time = timezone.now()
        else:
            start_time = timezone.now() - timezone.timedelta(minutes=20)
        end_time = start_time + timezone.timedelta(minutes=10)
        return Activity.objects.create(
            name=activity_name,
            product=_product,
            start_time=start_time,
            end_time=end_time,
        )

    # 测试获取活动页面接口
    def test_get_activity_list(self):
        self.data_slug("first activity", "product A")
        self.data_slug("second activity", "product B")
        activities = Activity.objects.all()
        response = self.client.get(reverse("get_activity_list"))
        serializer = ActivitySerializer(activities, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 获取单一合法活动
    def test_get_valid_single_activity(self):
        activity = self.data_slug("first activity", "product A")
        response = self.client.get(
            reverse("get_activity_instance", kwargs={"pk": activity.pk})
        )
        # activity = Activity.objects.get(pk=activity.id)
        serializer = ActivityInstanceSerializer(activity)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 非法 404
    def test_get_invalid_single_activity(self):
        response = self.client.get(
            reverse("get_activity_instance", kwargs={"pk": 20})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 用户正常下单: 活动进行中(running)，并且库存容量大于零(valid)
    # 订单是否合法判断: 是否带上用户 uuid
    # 活动是否合法判断: 是否容量大于 0
    # 活动状态: PREPARING, RUNNING, OVER
    def test_place_valid_order_to_running_valid_activity(self):
        activity = self.data_slug("first activity", "product A", 10, "RUNNING")
        uuid = 20
        response = self.client.post(
            reverse("get_activity_instance", kwargs={"pk": activity.id}),
            data={"uuid": uuid},
            content_type="application/json",
        )
        order = Order.objects.get(uuid=uuid, activity=activity)
        serializer = OrderSerializer(order)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_place_invalid_order_to_running_valid_activity(self):
        activity = self.data_slug("first activity", "product A", 10, "RUNNING")
        response = self.client.post(
            reverse("get_activity_instance", kwargs={"pk": activity.id}),
            content_type="application/json",
        )
        msg = {"msg": SECKILL_CONSTANT["REQUIRED_UUID"]}
        self.assertEqual(response.data, msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_place_valid_order_to_running_invalid_activity(self):
        activity = self.data_slug("first activity", "product A", 0, "RUNNING")
        uuid = 20
        response = self.client.post(
            reverse("get_activity_instance", kwargs={"pk": activity.id}),
            data={"uuid": uuid},
            content_type="application/json",
        )
        msg = {"msg": SECKILL_CONSTANT["EMPTY_INVENTPRY"]}
        self.assertEqual(response.data, msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_place_valid_order_to_preparing_valid_activity(self):
        activity = self.data_slug(
            "first activity", "product A", 10, "PREPARING"
        )
        uuid = 20
        response = self.client.post(
            reverse("get_activity_instance", kwargs={"pk": activity.id}),
            data={"uuid": uuid},
            content_type="application/json",
        )
        msg = {"msg": SECKILL_CONSTANT["ACTIVITY_PREPARING"]}
        self.assertEqual(response.data, msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_place_valid_order_to_over_valid_activity(self):
        activity = self.data_slug("first activity", "product A", 10, "OVER")
        uuid = 20
        response = self.client.post(
            reverse("get_activity_instance", kwargs={"pk": activity.id}),
            data={"uuid": uuid},
            content_type="application/json",
        )
        msg = {"msg": SECKILL_CONSTANT["ACTIVITY_OVER"]}
        self.assertEqual(response.data, msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_place_duplicate_valid_order_to_running_valid_activity(self):
        activity = self.data_slug("first activity", "product A", 10, "RUNNING")
        uuid = 20
        self.client.post(
            reverse("get_activity_instance", kwargs={"pk": activity.id}),
            data={"uuid": uuid},
            content_type="application/json",
        )
        response = self.client.post(
            reverse("get_activity_instance", kwargs={"pk": activity.id}),
            data={"uuid": uuid},
            content_type="application/json",
        )
        msg = {"msg": SECKILL_CONSTANT["DUPLICATE_ORDER"]}
        self.assertEqual(response.data, msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        orders = orders = Order.objects.filter(uuid=uuid).count()
        self.assertEqual(orders, 1)


class OrderTest(ActivityTest):
    def test_get_user_order_list(self):
        activity = self.data_slug("first activity", "product A", 10, "RUNNING")
        uuid = 20
        Order.objects.create(activity=activity, uuid=uuid)
        orders = Order.objects.filter(uuid=uuid)
        response = self.client.get(reverse("get_order_list"), {"uuid": uuid})
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user_order_list(self):
        self.data_slug("first activity", "product A", 10, "RUNNING")
        response = self.client.get(reverse("get_order_list"))
        msg = {"msg": SECKILL_CONSTANT["REQUIRED_UUID"]}
        self.assertEqual(response.data, msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
