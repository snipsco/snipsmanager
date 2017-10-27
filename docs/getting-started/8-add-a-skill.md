---
layout: doc
title:  "Add a skill"
permalink: /getting-started/add-a-skill/
---

Skills are functions which are executed when the Snips Platform detects an intent from a query.

In the first sample assistant you created, a [Fake Weather Skill](https://github.com/snipsco/snips-skill-fakeweather) is used to speak fake weather forecasts when a weather-related intent is detected. This is specified in the `skills` section of the Snipsfile:

```yaml
skills:
  - url: https://github.com/snipsco/snips-skill-fakeweather
    package_name: snipsfakeweather
    requires_tts: True
```

The skill already knows how to handle intents from the prepackaged Weather Bundle. Therefore, no further configuration is required.

In this step, you will create your own custom skill, and you will explictly tell it how to react to the new intents from the Calculator bundle you just added.

The skill will be very simple: it will just perform the arithmetic operation defined by the intent, and speak out the result.

Edit the Snipsfile, replacing the `skills` section with the following:

```yaml
skills:
  - name: calculator
    requires_tts: True
    intents:
      - intent: GetSum
        action: >
          {% raw %}{%{% endraw %}
          sum = int(intent.firstTerm) + int(intent.secondTerm)
          tts_service.speak(str(sum))
          {% raw %}%}{% endraw %}
      - intent: GetDifference
        action: >
          {% raw %}{%{% endraw %}
          difference = int(intent.firstTerm) - int(intent.secondTerm)
          tts_service.speak(str(difference))
          {% raw %}%}{% endraw %}
      - intent: GetProduct
        action: >
          {% raw %}{%{% endraw %}
          product = int(intent.firstTerm) * int(intent.secondTerm)
          tts_service.speak(str(product))
          {% raw %}%}{% endraw %}
      - intent: GetQuotient
        action: >
          {% raw %}{%{% endraw %}
          quotient = int(intent.firstTerm) / int(intent.secondTerm)
          tts_service.speak(str(quotient))
          {% raw %}%}{% endraw %}
```

That's it. You have added to the assistant a simple skill, named `calculator`. It reacts to four intents: `GetSum`, `GetDifference`, `GetProduct`, `GetQuotient`.

To each intent, an `action` block is provided, containing code written in Python. In each such block, you access the `intent` object and its slot values `intent.firstTerm` and `intent.secondTerm`, and perform the adequate arithmetic operation to find the result.

The skill declares that it uses the Speech-To-Text (TTS) service using the `requires_tts: True` entry. This allows you, in your code, to access an instance named `tts_service`. This instance has a single function, `tts_service.speak()`, that you use to speak out the result.

You can deploy the assistant and check that it works:

```sh
$ sam deploy
```

Try again to speak the query from the previous step:

> Hey Snips, what is 22 multiplied by 133

You will now hear "2926" spoken out.

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/testing-locally/">
  I added the calculator skill
</a>
<a class="button" href="#">
  Report a problem
</a>
