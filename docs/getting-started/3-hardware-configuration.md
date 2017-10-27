---
layout: doc
title:  "Hardware configuration"
permalink: /getting-started/hardware-configuration/
---

Depending on the hardware you use (microphone, speaker, leds etc), you may need to go through some preliminary configuration. Sam provides some helpers to automate this process with common hardware. In most cases, you don't need to do anything.

### Microphone

You can start checking that your microphone is working:

```sh
$ sam test microphone
Testing microphone
Say something in the microphone, then press Enter...
...
```

If you can clearly hear what you just said, you can move on without further microphone configuration. If not, start the interactive microphone setup guide:

```sh
$ sam setup microphone
Starting microphone setup...
What microphone do you use?
[1] Generic USB
[2] ReSpeaker 7-Mic Array
...
```

For further details, you can check our [Microphone Setup Guide]({{ site.baseurl }}/articles/microphone-setup/).

### Other peripherals

Similarly to the microphone, you can check that your speaker is working:

```sh
$ sam test speaker
```

You can also test your leds:

```sh
$ sam test leds
```

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/deploy-an-assistant/">
  My microphone is recording
</a>
<a class="button" href="#">
  Report a problem
</a>
