# -*-: coding utf-8 -*-
""" Class for holding all the intent classes present in the assistant. """

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

{% for intent in intents -%}
from intents.{{camel_case_to_underscore(to_camelcase_capitalized(intent.name))}}_intent import {{to_camelcase_capitalized(intent.name)}}Intent
{% endfor %}

class IntentRegistry:
    """ Class for holding all the intent classes present in the assistant. """

    # pylint: disable=too-few-public-methods
    def __init__(self):
        """ Initialisation. """
        self.intent_classes = [
            {% for intent in intents -%}
            {{to_camelcase_capitalized(intent.name)}}Intent{{"," if not loop.last}}
            {% endfor -%}
        ]

