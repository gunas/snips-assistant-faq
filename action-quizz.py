#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
import times_tables as tt
import json


MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


INTENT_START_MISSING_MILES_FAQ = "claim_miles_query_start"
INTENT_MILES_MISSING_FLIGHT = "claim_miles_flown_flight"
INTENT_INTERRUPT = "interrupt"
INTENT_DOES_NOT_KNOW = "does_not_know"

INTENT_FILTER_GET_ANSWER = [
    INTENT_MILES_MISSING_FLIGHT,
    INTENT_INTERRUPT,
    INTENT_DOES_NOT_KNOW
]

def start_missing_miles_faq(hermes, intent_message):
    print("missing_miles_faq start")
    if intent_message.intent.probability > 0.9:
        result_message = "start missing miles faq. did you miss your flight?"
    else:
        result_message = "not sure if you concern about miles, can you ask again"
    hermes.publish_continue_session(intent_message.session_id, result_message, INTENT_FILTER_GET_ANSWER)

def user_gives_answer(hermes, intent_message):
    print("User is giving an answer")


def user_does_not_know(hermes, intent_message):
    print("User does not know the answer")
    


def user_quits(hermes, intent_message):
    print("User wants to quit")
    

def session_started(hermes, session_started_message):
    print("Session Started")




def session_ended(hermes, session_ended_message):
    print("Session Ended")


with Hermes(MQTT_ADDR) as h:

    h.subscribe_intent(INTENT_START_MISSING_MILES_FAQ, start_missing_miles_faq) \
        .subscribe_intent(INTENT_INTERRUPT, user_quits) \
        .subscribe_intent(INTENT_DOES_NOT_KNOW, user_does_not_know) \
        .subscribe_intent(INTENT_MILES_MISSING_FLIGHT, user_gives_answer) \
        .subscribe_session_ended(session_ended) \
        .subscribe_session_started(session_started) \
        .start()
