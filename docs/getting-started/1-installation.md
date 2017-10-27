---
layout: doc
title:  "Installation"
permalink: /getting-started/installation/
---

In this step you will install the Sam Command Line Interface (CLI). You will use the CLI to create, manage and deploy your assistants, to configure your hardware, to view the logs of your assistants as it runs on the Raspberry, as well as to run your application locally for quick prototyping.

<div class="language-sh highlighter-rouge"><div class="highlight hljs shell"><code><span class="nv"><span class="hljs-meta">$</span><span class="bash"> </span></span><span class="bash">sam devices</span>
Scanning Raspberry Pi devices on the network...
Found 2 device<span class="o">(</span>s<span class="o">)</span>:
- raspberrypi <span class="o">(</span>192.168.9.2<span class="o">)</span>
- raspi-basement <span class="o">(</span>192.168.9.3<span class="o">)</span>
</code></div></div>


<div class="dropdown is-hoverable">
  <div class="dropdown-trigger">
    <button class="button is-primary" aria-haspopup="true" aria-controls="dropdown-menu4">
      <span class="icon is-small">
        <i class="fa fa-download"></i>
      </span>
      <span>Choose platform...</span>
      <span class="icon is-small">
        <i class="fa fa-angle-down" aria-hidden="true"></i>
      </span>
    </button>
  </div>
  <div class="dropdown-menu" id="dropdown-menu3" role="menu">
    <div class="dropdown-content">
      <a href="#" class="dropdown-item">
        Raspbian Image
      </a>
      <a href="#" class="dropdown-item">
        Debian
      </a>
      <a href="#" class="dropdown-item">
        macOS
      </a>
    </div>
  </div>
</div>
<br />

Once installed, you can use the `sam` command from your command shell.

Find a nearby device running the Snips platform:

```sh
$ sam devices
Scanning Raspberry Pi devices on the network...
Found 2 device(s):
- raspberrypi (192.168.9.2)
- raspi-basement (192.168.9.3)
```

<div class="notification is-info">
  If Sam does not find any device, make sure the Raspberry Pi and your computer are on the same network.
</div>

Connect to your device:

```sh
$ sam connect raspberrypi
Connecting to device raspberrypi...
[OK] Connected to device raspberrypi
```

You are now connected to your Snips device. At any time, you may check the connection status:

```sh
$ sam status
Connected to device raspberrypi
OS version ........... Raspbian Jessie Lite Apr-17
Snips version ........ Not installed
Sam Server version ... Not installed
Status ............... Not live
```

The device is shown as "Not live" as it currently does not have the Snips Platform installed. In the next step, you will install the Snips Platform on the device.

Optionally, you can rename your device to something more suited:

```sh
$ sam set alias raspi-snips
```

You can now access your device with your new alias:

```sh
$ sam connect raspi-snips
```

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/setup/">
  I have connected to my Pi
</a>
<a class="button" href="#">
  Report a problem
</a>
