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
from hashlib import sha512

import requests

import utils

app = Celery('tasks', broker=utils.redis_broker_url())


@app.task(ignore_result=True, bind=True)
def do(self, method, url, headers, body, callback, insecure,
       salt=None, context=None):
    func = getattr(requests, method.lower())
    resp = func(url, headers=headers, data=body, verify=not insecure)
    data = {'task': self.request.id,
            'status': '%s %s' % (resp.status_code, resp.reason),
            'headers': dict(resp.headers),
            'body': resp.content}

    if salt:
        data['task_signature'] = sha512(self.request.id + str(salt)).hexdigest()

    if context:
        data['context'] = context

    requests.post(callback, json=data, verify=not insecure)
    return None
