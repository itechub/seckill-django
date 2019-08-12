#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 root <root@MrRobot.local>
#

from django.conf import settings
from rest_framework import serializers

from .models import Product, Activity, Order


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ("id", "name", "inventory", "created")


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = Activity
        fields = ("id", "name", "product", "start_time", "end_time", "created")


class ActivityInstanceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    product = ProductSerializer()

    class Meta:
        model = Activity
        fields = ("id", "name", "product", "start_time", "end_time", "created")


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    activity = ActivitySerializer()
    created = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ("id", "uuid", "activity", "payment", "created")


class UidSerializer(serializers.Serializer):
    uuid = serializers.IntegerField(min_value=1)
