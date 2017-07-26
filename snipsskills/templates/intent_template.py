#!/usr/bin/env python3
# encoding: utf-8

# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
#
# WARNING: THIS IS AN AUTO-GENERATED FILE
# DO NOT ATTEMPT TO EDIT IT, AS CHANGES WILL BE OVERWRITTEN.
#
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************

from utils.intent_parser import IntentParser as ip


class {{to_camelcase_capitalized(intent.name)}}Intent:

    intentName = "{{ intent.name }}"

    {% if intent.slots is defined and intent.slots|length > 0 -%}
    def __init__(self{% for slot in intent.slots -%}, {{slot.name}}=None{% endfor %}):
        {% for slot in intent.slots -%}
        self.{{slot.name}} = {{slot.name}}
        {% endfor %}
    {% endif -%}

    @staticmethod
    def parse(payload):
        intentName = ip.get_intent_name(payload)
        if intentName != {{to_camelcase_capitalized(intent.name)}}Intent.intentName:
            return None
        return {{to_camelcase_capitalized(intent.name)}}Intent(
            {% for slot in intent.slots -%}
            ip.get_slot_value(payload, "{{ slot.name}}"){{"," if not loop.last}}
            {% endfor -%}
        )
