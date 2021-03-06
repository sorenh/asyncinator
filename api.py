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
import json

from flask import Flask, request, Response

import tasks

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return Response(open('README.md', 'r'), mimetype='text/plain')

    for arg in ['method', 'url', 'callback']:
        if arg not in request.form:
            return 'You must provide method, url, and callback', 400

    if request.form['method'].lower() not in ['get', 'post', 'patch', 'put']:
        return 'Invalid method', 400

    res = tasks.do.delay(request.form['method'],
                         request.form['url'],
                         json.loads(request.form.get('headers', '[]')),
                         request.form.get('body', None),
                         request.form['callback'],
                         'insecure' in request.form,
                         request.form.get('salt'),
                         request.form.get('context'))
    return res.id, 201
