---
layout: doc
title:  "Deploy an assistant"
permalink: /getting-started/deploy-an-assistant/
---

In this step, you will deploy an assistant to your device.

Create a new Snips assistant, which will setup a simple project using the current device settings, and load a sample assistant for testing:

```sh
$ sam create
Creating new Snips assistant... done
Loading sample assistant... done
[OK] Snips assistant created
```

When you create a new Snips assistant, a [Snipsfile]({{ site.baseurl }}/articles/snipsfile) is created in the root directory of your project. This is a plain text file, adhering to YAML syntax, containing all the information about your project.

Deploy your assistant to your device:

```sh
$ sam deploy
Deploying Snips assistant to device raspi-snips
[OK] Successfully deployed assistant to raspi-snips
```

Your assistant is now deployed on your device, and you can start speaking to it. Start with the wakeword:

> Hey Snips

followed by your query:

> Is it going to be sunny in Chicago this week-end?

You should hear a sample response being spoken to you. If not, make sure that the [speaker is properly configured]({{ site.baseurl }}/getting-started/hardware-configuration/).

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/view-logs/">
  I deployed by assistant
</a>
<a class="button" href="#">
  Report a problem
</a>
