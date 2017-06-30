# Copyright 2017 Mastercard
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from celery import Celery

import requests

import utils

app = Celery('tasks', broker=utils.redis_broker_url())


@app.task
def do(method, url, headers, body, callback):
    func = getattr(requests, method.lower())
    resp = func(url, headers=headers, data=body)
    requests.post(callback,
                  data={'status': '%s %s' % (resp.status_code, resp.reason),
                        'headers': resp.headers,
                        'body': resp.content})
    return None
