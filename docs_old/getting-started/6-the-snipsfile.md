---
layout: doc
title:  "The Snipsfile"
permalink: /getting-started/the-snipsfile/
---

The [Snipsfile]({{ site.baseurl }}/articles/snipsfile/) is where you define the features and settings of your Snips assistant. It is a plain text file, adhering to YAML syntax.

When you created your sample project, a Snipsfile was generated, and it looks similar to this:

```yaml
assistant_url: https://s3.amazonaws.com/labs-assistants/assistant_labs.zip
microphone:
  identifier: respeaker
  params:
    vendor_id: "2886"
    product_id: "0007"
skills:
  - url: https://github.com/snipsco/snips-skill-fakeweather
    package_name: snipsfakeweather
    requires_tts: True
```


The first line contains a reference to the assistant, as created in the [Snips Console](https://console.snips.ai):

```yaml
assistant_url: https://s3.amazonaws.com/labs-assistants/assistant_labs.zip
```

Here, you are pointing to a sample public assistant created by Snips. In the next section, you will load your own assistant.

The next section contains information about your microphone:

```yaml
microphone:
  identifier: respeaker
  params:
    vendor_id: "2886"
    product_id: "0007"
```

Depending on your setup, this section may be different, or not present at all in case of plug and play microphones.

Finally, the last section declares which skills to bind to, as well as some configuration parameters pertaining to each skill:

```yaml
skills:
  - url: https://github.com/snipsco/snips-skill-fakeweather
    package_name: snipsfakeweather
    requires_tts: True
```

For this example, we are using the [Fake Weather Skill](https://github.com/snipsco/snips-skill-fakeweather), which simply generates a random weather forecast.

For more configuration option, make sure to read the [Snipsfile article]({{ site.baseurl }}/articles/snipsfile).

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/create-a-custom-assistant/">
  I undertand the workings of the Snipsfile
</a>
<a class="button" href="#">
  Report a problem
</a>
