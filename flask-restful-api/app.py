# -*- coding: utf-8 -*-
import os

from flask import Flask, jsonify, request

from __init__ import app, db
from models import Resource

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/resource', methods=['GET', 'POST'])
def all_resources():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        Resource.append({
            'resource_name': post_data.get('resource_name'),
            'status': post_data.get('status'),
            'description': post_data.get('description'),
            'resource_type': post_data.get('resource_type')
        })
        response_object['message'] = 'Resource added!'
    else:
        response_object['resources'] = Resource
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()
