# -*-: coding utf-8 -*-
""" Auto-generated intent class. """

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

# pylint: disable=line-too-long

from snipsmanagercore.intent_parser import IntentParser

class {{to_camelcase_capitalized(intent.name)}}Intent:

    intentName = "{{ intent.name }}"

    {% if intent.slots is defined and intent.slots|length > 0 -%}
    def __init__(self, sessionId, siteId, customData{% for slot in intent.slots -%}, {{slot.name}}=None{% endfor %}):
        self.sessionId = sessionId
        self.siteId = siteId
        self.customData = customData
        {% for slot in intent.slots -%}
        self.{{slot.name}} = {{slot.name}}
        {% endfor %}
    {% endif -%}

    @staticmethod
    def parse(payload):
        intentName = IntentParser.get_intent_name(payload)
        if intentName != {{to_camelcase_capitalized(intent.name)}}Intent.intentName:
            return None
        return {{to_camelcase_capitalized(intent.name)}}Intent(
            IntentParser.get_session_id(payload),
            IntentParser.get_site_id(payload),
            IntentParser.get_custom_data(payload),
            {% for slot in intent.slots -%}
            IntentParser.get_slot_value(payload, "{{ slot.name }}"){{"," if not loop.last}}
            {% endfor -%}
        )
