#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

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

import traceback

from .const import CAT_SUCCESS
from .container import sdk

__all__ = ["log_event", "log_exception", "log_error", "log_tag_for_api",
           "log_biz_result", "set_trace_id", "get_trace_id", "set_attributes",
           "set_baggages", "log_tag_for_next_call"]


def log_event(mtype, mname, status=CAT_SUCCESS, data=""):
    sdk().log_event(mtype, mname, status, data)


def log_exception(exc, err_stack=None):
    if err_stack is None:
        err_stack = traceback.format_exc()
    sdk().log_error(exc.__class__.__name__, err_stack)


def log_error(err_message, err_stack=None):
    if err_stack is None:
        err_stack = traceback.format_exc()
    sdk().log_error(err_message, err_stack)


def log_tag_for_api(name, custom_params):
    sdk().log_tag_for_api(name, custom_params)


def log_biz_result(code, msg, status):
    sdk().log_biz_result(code, msg, status)


def set_trace_id(trace_id):
    sdk().set_trace_id(trace_id)


def get_trace_id():
    return sdk().get_trace_id()


def set_attributes(attributes):
    sdk().set_attributes(attributes)


def set_baggages(baggages):
    sdk().set_baggages(baggages)


def log_tag_for_next_call(name, custom_params):
    sdk().log_tag_for_next_call(name, custom_params)
