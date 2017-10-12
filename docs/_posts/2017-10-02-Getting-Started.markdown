---
layout: page
title:  "Getting Started"
date:   2017-10-02 12:53:25 +0200
permalink: /getting-started/
---

In this guide, we will help you through the process of creating a simple assistant using the Snips Assistant Manager.

## What is a Snips assistant composed of?

A typical voice assistant is a device, such as a Raspberry Pi, equipped with a microphone. The device is waiting for a hotword, e.g. *Hey Snips*, *OK Google* or *Alexa*, that puts it in listening mode. Then it starts transcribing the user's voice into text, using Automatic Speech Recognition (ASR). After a short silence, it sends the transcribed phrase to a Natural Language Understanding (NLU) component, which extract the meaning of the phrase encoded in a JSON object, a so-called *intent*, that the system can understand and act upon. For instance, if the user says *Turn on the lights*, the system will output an intent which could be named `Lights` with parameter `state=on`. This is the first part illustrated in the following diagram, and consistutes the Snips Platform:

<img src="{{ site.baseurl }}/images/Platform.png" srcset="{{ site.baseurl }}/images/Platform@2x.png 2x"/>

The second part, the Skills part, corresponds to what happens after an intent has been detected by the Snips Platform. For instance, for a connected alarm clock, on may want to add a weather skill and a radio skill which react to `WeatherForecast` and `TurnOnRadio` intents, respectively.

The hotword, ASR, and NLU modules are configured in the [Snips Console](https://console.snips.ai). This is a web interface that allows you to specify the language of the system, to define the types of queries that the system should understand, and to provide custom training examples that correspond exactly to the intended use.

## What is Sam?

The Snips Assistant Manager, or Sam, is a set of command-line utilities for managing assistants built with Snips. With it, you can completely specify the behaviour of your assistant without a single line of code.

All the information about an assistant is contained in a file, the Snipsfile. In it, you can specify:

- The location of your assistant models
- The skills you want to include, and accompanying parameters, such as an API key or a username
- Optionally, how skills should react to intents
- Various general configuration parameters, such as microphone type or Text-to-Speech service



## Installation

## Creating a Snipsfile

First, let's create a simple **Snipsfile**, and put it in an empty folder on the Raspberry Pi:

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

## Installing dependencies

From the command line, we place ourselves at the location of the Snipsfile, and run:

```sh
$ snipsskills install
```

This will download the language models, create bindings between intents and skills, and optionally install boot scripts (for the assistant to be launched at start) as well as Bluetooth dependencies.

After the installation has completed, we are ready to run the assistant!

## Running

Simply run the following:

```sh
$ snipsskills run
```

After a few seconds, you will hear a gentle wake up sound, indicating that the assistant is ready to take your voice commands. We can now start speaking:

> Hey Snips

> What is the weather going to be in Chicago this week-end?

If all works well, you should get a reply speaking out a fake weather forecast!