---
layout: page
title:  "Microphone Setup"
date:   2017-10-02 12:53:25 +0200
permalink: /microphones/
---

We have streamlined the process of setting up a microphone using Snips Assistant Manager, so it should just be a matter of specifying the microphone model in the Snipsfile, and Sam will update drivers and setup acoundrc configurations. If you want recommendation for which microphones to use, check out our [Microphone Array Benchmark](medium.com/snips-ai/benchmarking-microphone-arrays-respeaker-conexant-microsemi-acuedge-matrix-creator-minidsp-950de8876fda).

On this page, we compile the setup instructions for the most popular microphones for Raspberry Pi.

## ReSpeaker

Simply add the following to your Snipsfile:

```yaml
microphone:
    identifier: respeaker
    params:
        vendor_id: "2886"
        product_id: "0007"
```

You need to change the `vendor_id` and `product_id` to match those of your setup. You can obtain these by running the  `lsusb` command.

```sh
$ lsusb
Bus 001 Device 004: ID 2886:0007 ReSpeaker
...
```

## Jabra

Add the following to your Snipsfile:

```yaml
microphone:
    identifier: jabra
```

## Other microphones

Most other microphones do not require a custom setup. You don't need to add anything to your Snipsfile. However, if you have trouble setting one up, please let us know and we will try to include it in our toolkit.