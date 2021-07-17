#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request, jsonify

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"


# Added color and quantity as parameters in this endpoint and changed it to a post request
@app.route("/purchase_a_sword/<color>/<quantity>", methods=["POST"])
def purchase_a_sword(color, quantity):
    purchase_sword_event = {'event_type': 'purchase_sword', 'color': color, 'quantity': quantity}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"
