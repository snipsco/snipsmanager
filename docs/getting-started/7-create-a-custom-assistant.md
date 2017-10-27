---
layout: doc
title:  "Create a custom assistant"
permalink: /getting-started/create-a-custom-assistant/
---

In the sample Snipsfile, the assistant you use is a public assistant created by Snips, handling weather-related queries:

```yaml
assistant_url: https://s3.amazonaws.com/labs-assistants/assistant_labs.zip
```

In this step, you will replace this with your own assistant.

To do so, head over to the [Snips Console](https://console.snips.ai). If you haven't done so already, create an account

### Create an assistant

Create an assistant, selecting "Raspberry" as the platform:

<img src="{{ site.baseurl }}/images/console-create-assistant.png" srcset="{{ site.baseurl }}/images/console-create-assistant@2x.png 2x"/>

### Add intents

Select the "Calculator" intents bundle. This is a prepackaged set of intents for simple arithmetic operations, such as additions and multiplications.

<img src="{{ site.baseurl }}/images/console-add-bundle.png" srcset="{{ site.baseurl }}/images/console-add-bundle@2x.png 2x"/>

You can try out the assistant in the console by typing queries in the web console on the right.

### Add the assistant to your Snipsfile

Note down the ID of your assistant. It can be found in the URL:

<img src="{{ site.baseurl }}/images/console-assistant-id.png" srcset="{{ site.baseurl }}/images/console-assistant-id@2x.png 2x"/>

Edit your Snipsfile, replacing the `assistant_url` line with the following:

```yaml
assistant_id: YOUR_ASSISTANT_ID
```

replacing `YOUR_ASSISTANT_ID` with the ID of your assistant.

<div class="notification is-info">
    Note how the key has changed from <code>assistant_url</code> to <code>assistant_id</code>: you are now pointing to a private assistant, accessible only to you. As a third option, you can point to a local file on your device, downloaded from the Snips Console, using the <code>assistant_file</code> key. For more information, see the <a href="{{ site.baseurl }}/articles/snipsfile">Snipsfile article</a>.
</div>

### Update your device

Push the changes to your device:

```sh
$ sam deploy
```

Once ready, try the following queries:

> Hey Snips, what is 22 multiplied by 133

You will notice that nothing happens. This is because the assistant is not configured to react to the new intents from the IoT bundle. In the next step, you will learn how to create a skill and to bind it to the intents of your assistant.

You can check that the assistant is nevertheless running. Try to repeat the above query, but this time watching the logs:

```sh
$ sam watch
↯ Hotword What is 22 multiplied by 133

Query: Turn on the lights
Intent: GetSum
        firstTerm  snips/number 22
        secondTerm snips/number 133
```

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/add-a-skill/">
  I deployed a custom assistant
</a>
<a class="button" href="#">
  Report a problem
</a>
