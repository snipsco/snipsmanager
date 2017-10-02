---
layout: page
title:  "Skills"
date:   2017-10-02 12:53:25 +0200
---

In this guide, we will help you through the process of creating a simple weather assistant using the Snips Skills toolchain.

#### Creating a Snipsfile

First, let's create a simple **Snipsfile**, and put it in an empty folder on the Raspberry Pi:

```js
var i = 1;
```

{% highlight ruby %}
var i = 1;
{% endhighlight %}

{% highlight yaml %}
assistant_url: "https://github.com/snipsco/example-assistants/raw/master/weather-assistant.zip"
locale: en_US
default_location: Paris,fr
tts:
  service: snips
skills:
  - package_name: snipsfakeweather
    pip: snips-skill-fakeweather
    requires_tts: True
{% endhighlight %}

This Snipsfile points to a weather assistant, as created in the [Snips Console](https://console.snips.ai), using the prepackaged Weather Bundle. It uses the Snips on-device text-to-speech engine, and binds to a single skill, [snipsfakeweather](https://github.com/snipsco/snips-skill-fakeweather), which, given a date and a location, generates a fake spoken weather forecast.

#### Installing dependencies

From the command line, we place ourselves at the location of the Snipsfile, and run:

```sh
$ snipsskills install
```

This will download the language models, create bindings between intents and skills, and optionally install boot scripts (for the assistant to be launched at start) as well as Bluetooth dependencies.

After the installation has completed, we are ready to run the assistant!

#### Running

Simply run the following:

```sh
$ snipsskills run
```

After a few seconds, you will hear a gentle wake up sound, indicating that the assistant is ready to take your voice commands. We can now start speaking:

> Hey Snips

> What is the weather going to be in Chicago this week-end?

If all works well, you should get a reply speaking out a fake weather forecast!