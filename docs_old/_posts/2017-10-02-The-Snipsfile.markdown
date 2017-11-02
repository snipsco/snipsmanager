---
layout: page
title:  "The Snipsfile"
date:   2017-10-02 12:53:25 +0200
permalink: /snipsfile/
---

## What is a Snipsfile?

The Snipsfile is a plain text file that declaratively describes your assistant. It contains a reference to the Snips assistant as created in the [Snips Console](https://console.snips.ai), and optionally as list of skills and various settings such as logging info and language.

A Snipsfile can be very simple:

```yaml
assistant_id: proj_01ap9812WUer9
```

A slightly more complex Snipsfile can look like this:

```yaml
assistant_id: proj_01ap9812WUer9
logging: True
microphone:
    identifier: respeaker
    params:
        vendor_id: "2886"
        product_id: "0007"
skills:
    - package_name: snipshue
      params:
          hostname: 192.168.100.20
          username: AzXYX391uurWWAzmMkff192Pwo
          light_ids: [1, 2, 3, 4]
    - package_name: snipssmartercoffee
```

## Supported fields

The Snipsfile adheres to [YAML syntax](https://en.wikipedia.org/wiki/YAML). Let us go through the various fields which are currently handled:

### 'assistant_id'

```yaml
assistant_id: proj_01ap9812WUer9
```

This field indicates the identifier of your assistant. To obtain it, head over the the [Snips Console](https://console.snips.ai), select your assistant, right click on the "Download Assistant" button and select "Copy Link Address". The address is of the form _https://console.snips.ai/api/assistants/proj_XYZ/download_, and the part starting with `proj_` corresponds to the identifier.

### 'assistant_file'

```yaml
assistant_file: path/to/assistant.zip
```

Instead of fetching an assistant from the Snips Console, using the `assistant_id` field as described above, you can specify a local file instead using the `assistant_file` field. The file in question is obtained in the Snips Console via the "Download Assistant" button. You may then manually copy this file to your device. The path may either be full (e.g. `/etc/snips/assistant.zip`), or relative to the location of the Snipsfile (e.g. `my_tv_assistant.zip`).

### 'assistant_url'
```yaml
assistant_url: https://example.com/my_assistant.zip
```

This field specifies a URL that points to an assistant stored in a server. This method allows everyone to create an assistant using the Console and upload it to a different server (Amazon S3, Dropbox, etc) to share it among other users. The file must be publicly available as direct download.

### 'logging'

```yaml
logging: True
```

If logging is enabled, your will be able to inspect detailed logs of the skills server, either when running `snipsskills run` on your own, or as output of the systemd scripts used to start the skills server at boot. In the latter case, logs are accessed via the command:

```sh
$ sudo journalctl -u snipsskills.service
```

### 'microphone'

This section provides information about your microphone setup. It will handle setting up the adequate `.asoundrc` configuration, and write udev rules if required. If using a generic plug-and-play microphone, this section is not needed. Here is an example section for a ReSpeaker microphone:

```yaml
microphone:
    identifier: respeaker
    params:
        vendor_id: "2886"
        product_id: "0007"
```

The `vendor_id` and `product_id` fields are specific to ReSpeaker, and are found using the `lsusb` command.

In addition to the above ReSpeaker configuration, we support the Jabra microphone configuration:

```yaml
microphone:
    identifier: jabra
```

In case you have a specific configuration and you do not want `snipsskills` to modify it, just add the following variable to the Snipsfile.

```yaml
modify_asoundrc: False
```

More custom configurations will be added in the future. You can find help on setting up various microphones on the [Microphone Setup Guide]({{ site.baseurl }}{% post_url 2017-10-02-Microphone-Setup %}).

### 'tts'

This section specifies the text-to-speech service you want to use.

```yaml
tts:
    service: snips
```

Currently, two values are supported:

- `snips`: This is the in-house Snips TTS engine, based on Pico. It is on-device, so it does not require network connectivity.
- `google`: This is Googles Cloud Speech TTS engine. It works in the cloud, and requires a network connection.

### 'mqtt_broker'

By default, the Snips SDK launches an MQTT broker locally, listening on port 9898. You may optionally tell the SDK to use another MQTT broker, in which case you would want to also change the skills service to point to that broker. This is done as follows:

```yaml
mqtt_broker:
    hostname: 192.168.1.22
    port: 1883
```

Here, `hostname` can either be an IP address or a hostname.

### 'skills'

You may want your assistant to react in specific ways upon receiving an intent from the Snips SDK. This is done by binding skills to intents as follows:

```yaml
skills:
    - id: snipshue
        params:
            hostname: 192.168.1.226
            username: iUELXTFaQXPiXRixOXaz36IeJeX3mjkZ
            light_ids: [1, 2, 3, 4]
    - id: snipssmartercoffee
        params:
            hostname: 192.168.163.105
    - package_name: snipsfakeweather
      pip: snips-skill-fakeweather
      requires_tts: True
```

Let's dive deeper into how skills are handled in the Snipsfile.

## Skills

Skills are functions which are executed after an intent is detected. For instance, if trained to do so, your assistant may react to the utterance *"Turn on the lights"* and detect, say, a `LightsOn` intent. In the Snipsfile, you can tell your assistant to react to this intent by binding it to a skill which actually turns on the lights (e.g. with the Philips Hue API). In its simplest form, this is done as follows:

```yaml
skills:
    - id: snipshue
        params:
            hostname: 192.168.1.226
            username: iUELXTFaQXPiXRixOXaz36IeJeX3mjkZ
            light_ids: [1, 2, 3, 4]
    - id: snipssmartercoffee
        params:
            hostname: 192.168.151.96
```

This tells the Skills Manager to fetch two skills, `snipshue` and `snipssmartercoffee`, and set them up with various parameters, such as the IP address of the Philips Hue Bridge and Smarter Coffee machine.

### Skill location

You may specify the location of the skill using either `id` or `url`:

```yaml
skills:
    - id: snipshue
    - url: https://github.com/snipsco/snips-skill-smarter-coffee
```

In the first case, the skill is referenced by identified, corresponding to one listed in the [Official Skills Registry](https://github.com/snipsco/snips-skills-registry). If you want to have your skill listed there, you are welcome to (submit a Pull Request)[https://github.com/snipsco/snips-skills-registry/pulls]. In the latter case, an explicit url of the Python package is provided.

### Providing skills parameters

Each skill may require some custom set up. For instance, the Philips Hue skill requires the hostname of the Philips Hue Bridge, the username, as well as a list of light IDs. This is specified in the `params` section:

```yaml
skills:
    - id: snipshue
        params:
            hostname: 192.168.1.226
            username: iUELXTFaQXPiXRixOXaz36IeJeX3mjkZ
            light_ids: [1, 2, 3, 4]
```

### Explicit bindings with intents

In the above examples, the skills are set up to react to specific intents, via a custom [Snipsspec file](https://github.com/snipsco/snips-skill-hue/blob/master/Snipsspec) proper to each skill. This means that, upon receiving an intent from the Snips SDK, a certain skill may be triggered automatically. For instance, the `snipshue` skill automatically reacts to the `ActivateLightColor` intent provided in the Snips IoT bundle available in the console.

#### Triggering simple skill functions

However, your assistant might not include this bundle, and have alternative intents for changing the light color. In this case, we can explicitly specify which intents a skill should react to, and how. In the above example, let's say we want to turn on the lights when receiving a custom intent named `LightsOn`. This is done by adding an `intents` section in the `snipshue` skill, providing the name of the intent, and the action to execute. For instance:

```yaml
skills:
    - id: snipshue
        intents:
        - intent: LightsOn
            action: "turn_on"
```

Here, upon receiving a `LightsOn` intent, it will call the [`turn_on()`](https://github.com/snipsco/snips-skill-hue/blob/master/snipshue/snipshue.py) function of the skill.

#### Complex bindings

Now suppose we want to add more conditionals on a certain intent. For instance, I may have a `SetLightColor` intent which set the Hue to a certain color, or just turns on the lights if no color slot is included in the intent. This is done using a YAML code block, starting the `action` field with a `>` sign, and providing Python code inside a block delimited by `{% raw %}{%{% endraw %}`  and `{% raw %}%}{% endraw %}`:

```yaml
skills:
    - id: snipshue
        intents:
        - intent: SetLightColor
            action: >
                {% raw %}{%{% endraw %}
                if intent.objectColor != None:
                  skill.set_color_name(intent.objectColor)
                else:
                  skill.turn_on()
                {% raw %}%}{% endraw %}
```

Here, the names `intent` and `skills` are reserved. The `intent` variable corresponds to the intent received from the SDK. We may use it to test various conditions, and react accordingly. The `skill` variable corresponds to the actual skill instance, and we may explicitly call functions from its API.

#### Default behaviours in `Snipsspec`

As mentioned above, skills can automatically react to certain intents, so that we don't have to provide everything explicitly in the Snipsfile. For more information on how to provide default behaviours to your skills, see the [Snipsspec Wiki](https://github.com/snipsco/snipsskills/wiki/Creating-Skills#the-snipsspec-file).

## Examples

We've compiled a list of sample Snipsfiles on the [Examples Wiki](https://github.com/snipsco/snipsskills/wiki/Examples).