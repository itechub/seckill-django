#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
from django.conf.urls import url
from seckill import views

urlpatterns = [
    url(
        "^activities/$", views.ActivityList.as_view(), name="get_activity_list"
    ),
    url(
        "^activities/(?P<pk>[0-9]+)/$",
        views.ActivityInstance.as_view(),
        name="get_activity_instance",
    ),
    url(r"^orders/$", views.OrderList.as_view(), name="get_order_list"),
]
