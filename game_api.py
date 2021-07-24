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



# Function to purchase a horse
@app.route("/purchase_a_horse/<speed>/<size>/<quantity>", methods=["POST"])
def purchase_a_horse(speed, size, quantity):
    """
    Inputs:
    - speed
    - size (small, medium, or large)
    - quantity
    """
    
    # collect user inputs
    purchase_horse_event = {
        "event_type": "purchase_horse", 
        "speed": speed, 
        "size": size, 
        "quantity": quantity}
    
    # error handling
    if purchase_horse_event['size'].lower() not in ['small', 'medium', 'large']:
        raise Exception("Please enter either 'small', 'medium' or 'large' for horse size")
        
    elif float(purchase_horse_event['speed']) < 0:
        raise Exception("Please enter a non-negative value for speed")
        
    elif float(purchase_horse_event['quantity']) < 0:
        raise Exception("Please enter a non-negative value for quantity")
        
    else:
        # clean inputs to collect only lower case values for consistency
        purchase_horse_event['size'] = purchase_horse_event['size'].lower()
        
        # log event to kafka
        log_to_kafka("events", purchase_horse_event)
        return "Horse Purchased!\n"



# Function to join guild
@app.route("/guild/<action>", methods=["POST"])
def guild(action):
    """
    Inputs:
    - action (join, leave)
    """
    
    guild_event = {
        "event_type": "guild", 
        "action": action}
    
    # clean inputs to collect only lower case values for consistency
    guild_event['action'] = guild_event['action'].lower()
    
    # error handling
    if guild_event['action'] not in ['join', 'leave']:
        raise Exception("Available actions are 'join' or 'leave'")
    
    else:
        log_to_kafka("events", guild_event)
    
        if guild_event['action'] == "join":
            return "You joined the guild!\n"
        else:
            return "You left the guild!\n"
