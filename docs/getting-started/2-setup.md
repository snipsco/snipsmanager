---
layout: doc
title:  "Set up"
permalink: /getting-started/setup/
---

In this step, you will install all the necessary dependencies on the Raspberry Pi to run the Snips Platform as well as the Sam Server.

Initialise the device:

```sh
$ sam init
Installing the Snips toolkit on device raspi-snips
Installing the Snips Platform
Installing the Sam Server
Setting up Bluetooth
Rebooting device
[OK] Installation finished
```

Once the device has rebooted, you can again check its status. Notice that the Snips Platform and Sam Server are now installed, and that the device status is "Live":

```sh
$ sam status
Connected to device raspi-snips
OS version ........... Raspbian Jessie Lite Apr-17
Snips version ........ 0.9.1
Sam Server version ... 0.3.5
Status................ Live (no assistant)
```

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/hardware-configuration/">
  I have installed Snips on my device
</a>
<a class="button" href="#">
  Report a problem
</a>
