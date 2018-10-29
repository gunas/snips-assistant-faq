#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"
INTENT_START_MISSING_MILES_FAQ = "claim_miles_query_start"
INTENT_MILES_MISSING_FLIGHT = "claim_miles_flown_flight"
INTENT_INTERRUPT = "interrupt"
INTENT_DOES_NOT_KNOW = "does_not_know"

INTENT_FILTER_GET_ANSWER = [
    INTENT_MILES_MISSING_FLIGHT,
    INTENT_INTERRUPT,
    INTENT_DOES_NOT_KNOW
]

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)



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


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent(INTENT_START_MISSING_MILES_FAQ, start_missing_miles_faq) \
         .subscribe_intent(INTENT_INTERRUPT, user_quits) \
         .subscribe_intent(INTENT_DOES_NOT_KNOW, user_does_not_know) \
         .subscribe_intent(INTENT_MILES_MISSING_FLIGHT, user_gives_answer) \
         .subscribe_session_ended(session_ended) \
         .subscribe_session_started(session_started) \
         .start()




