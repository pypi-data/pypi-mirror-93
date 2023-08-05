#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com>

# Copyright (c) 2011-2018, Meituan Dianping. All Rights Reserved.
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time

from .container import sdk


__all__ = ['MetricHelper', 'metric']


class MetricHelper(object):

    def __init__(self, name):
        self._name = name

    def add_name(self, name):
        self._name = name
        return self

    def count(self, count=1):
        sdk().log_metric_for_count(self._name, count)

    @classmethod
    def get_current_timestamp_ms(cls):
        return int(time.time() * 1000)

    def duration(self, duration_ms):
        sdk().log_metric_for_duration(self._name, duration_ms)

    def log_for_count_map(self, quantity, customParams, occurredTime=None):
        if occurredTime is None:
            occurredTime = self.get_current_timestamp_ms()
        sdk().log_metric_for_count_map(self._name, quantity, customParams, occurredTime)

    def log_for_avg(self, val, customParams, occurredTime=None):
        if occurredTime is None:
            occurredTime = self.get_current_timestamp_ms()
        sdk().log_metric_for_avg(self._name, val, customParams, occurredTime)

    def log_for_sum(self, val, customParams, occurredTime=None):
        if occurredTime is None:
            occurredTime = self.get_current_timestamp_ms()
        sdk().log_metric_for_sum(self._name, val, customParams, occurredTime)

    # def log_for_occ_time(self, customParams, occurredTime):
    #     sdk().log_metric_for_occ_time(self._name, customParams, occurredTime)


def metric(name):
    return MetricHelper(name)
