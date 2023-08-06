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

# -*- coding: utf-8 -*-

import cffi

ffi = cffi.FFI()

definitions = """
typedef struct _CatMessage CatMessage;
typedef struct _CatMessage CatEvent;
typedef struct _CatMessage CatMetric;
typedef struct _CatMessage CatHeartBeat;

typedef struct _CatTranscation CatTransaction;

struct _CatTranscation {
    void (*addData)(CatTransaction *transaction, const char *data);

    void (*addKV)(CatTransaction *transaction, const char *dataKey, const char *dataValue);

    void (*setStatus)(CatTransaction *transaction, const char *status);

    void (*setTimestamp)(CatTransaction *transaction, unsigned long long timestamp);

    void (*complete)(CatTransaction *transaction);

    void (*addChild)(CatTransaction *transaction, CatMessage *message);

    void (*setDurationInMillis)(CatTransaction* transaction, unsigned long long duration);

    void (*setDurationStart)(CatTransaction* transaction, unsigned long long durationStart);
};

struct _CatMessage {
    void (*addData)(CatMessage *message, const char *data);

    void (*addKV)(CatMessage *message, const char *dataKey, const char *dataValue);

    void (*setStatus)(CatMessage *message, const char *status);

    void (*setTimestamp)(CatMessage *message, unsigned long long timestamp);

    void (*complete)(CatMessage *message);
};

typedef struct _CatClientConfig {
    int encoderType;
    int enableHeartbeat;
    int enableSampling;
    int enableMultiprocessing;
    int enableDebugLog;
    int enableAutoInitialize;
} CatClientConfig;

// Origin implementation of map in C.
typedef struct __pthread_internal_list
{
  struct __pthread_internal_list *__prev;
  struct __pthread_internal_list *__next;
} __pthread_list_t;

struct __pthread_mutex_s
{
  int __lock;
  unsigned int __count;
  int __owner;
  unsigned int __nusers;
  int __kind;
  short __spins;
  short __elision;
  __pthread_list_t __list;
# define __PTHREAD_MUTEX_HAVE_PREV      1
};

typedef union {
  struct __pthread_mutex_s __data;
  char __size[40];
  long int __align;
} pthread_mutex_t;

typedef struct dictEntry {
    void *key;
    void *val;
    struct dictEntry *next;
} dictEntry;

typedef struct dictType {
    unsigned int (*hashFunction)(const void *key);
    void *(*keyDup)(void *privdata, const void *key);
    void *(*valDup)(void *privdata, const void *obj);
    int (*keyCompare)(void *privdata, const void *key1, const void *key2);
    void (*keyDestructor)(void *privdata, void *key);
    void (*valDestructor)(void *privdata, void *obj);
} dictType;

typedef struct dict {
    dictEntry **table;
    dictType *type;
    unsigned int size;
    unsigned int sizemask;
    unsigned int used;
    void *privdata;
} dict;

typedef struct _CCHashSlot {
    dict *m_dict;
    pthread_mutex_t m_lock;
} CCHashSlot;

typedef struct _CCHashMap {
    int m_hashSlotCount;
    void *m_privateData;
    dictType m_type;
    volatile long m_count;
    CCHashSlot m_hashSlot[];
} CCHashMap;
"""

ffi.cdef(definitions)

# map ops.
ffi.cdef("CCHashMap *createCCHashMapForPython();")
ffi.cdef("void *findCCHashMap(CCHashMap *pCCHM, void *key);")
ffi.cdef("void *findCCHashMapWithoutLock(CCHashMap *pCCHM, void *key);")
ffi.cdef("int putCCHashMap(CCHashMap *pCCHM, void *key, void *pVal);")
ffi.cdef("int putCCHashMapWithoutLock(CCHashMap *pCCHM, void *key, void *pVal);")
ffi.cdef("int replaceCCHashMap(CCHashMap *pCCHM, void *key, void *pVal);")
ffi.cdef("int replaceCCHashMapWithoutLock(CCHashMap *pCCHM, void *key, void *pVal);")

# common apis.
ffi.cdef("int catClientInitWithConfig(const char *domain, CatClientConfig* config);")
ffi.cdef("int catClientDestory();")
ffi.cdef("int isCatEnabled();")

# transaction apis.
ffi.cdef("CatTransaction *newTransaction(const char *type, const char *name);")

# event apis.
ffi.cdef("void logEvent(const char *type, const char *name, const char *status, const char *nameValuePairs);")
ffi.cdef("void logError(const char *msg, const char *errStr);")

# heartbeat apis.
ffi.cdef("CatHeartBeat *newHeartBeat(const char *type, const char *name);")

# metric apis.
ffi.cdef("void logMetricForCount(const char *name, int quantity);")
ffi.cdef("void logMetricForDuration(const char *name, unsigned long long durationMs);")
ffi.cdef("void logMetricForCountMap(const char *name, int quantity, CCHashMap* customParams, char* occurredTime);")
ffi.cdef("void logMetricForAvg(const char *name, const char *val, CCHashMap* customParams, char* occurredTime);")
ffi.cdef("void logMetricForSum(const char *name, const char *val, CCHashMap* customParams, char* occurredTime);")

# tag apis.
ffi.cdef("void logTagForApi(const char *name, CCHashMap* customParams);")
ffi.cdef("void logTagForNextCall(const char *name, CCHashMap* customParams);")

# biz result.
ffi.cdef("void logBizResult(const char *code, const char * msg, const char *status);")

# trace attributes getter / setter.
ffi.cdef("void setThreadLocalMessageTraceId(char *traceId);")
ffi.cdef("char *getThreadLocalMessageTraceId();")
ffi.cdef("void setThreadLocalMessageAttributes(CCHashMap *attributes);")
ffi.cdef("CCHashMap *geThreadLocaltMessageAttributes();")
ffi.cdef("void setThreadLocalMessageBaggages(CCHashMap *baggages);")
ffi.cdef("CCHashMap *getThreadLocalMessageBaggages();")

# destroy cat client.
ffi.cdef("void catClientDestroy();")


if __name__ == '__main__':
    ffi.compile(verbose=True)
