---
title: Overview
---

The Snips Skills Manager is a tool for easily setting up and managing a Snips assistant. A single configuration file, the Snipsfile, is required to create an assistant. In it, you specify:

- The location of your assistant, as created in the Snips Console
- The skills you want to install, and accompanying parameters, such as an API key
- Bindings between intents and skills
- Various configuration parameters, such as language and logging preferences.

Check out [Awesome Snips](https://www.github.com/snipsco/awesome-snips), a curated list of Snips skills, assistants and other resources to get you started. In particular, make sure to read the [Getting Started guide](./getting-started.html).

#### Why Snips Skills?

Creating, managing and deploying an assistant is complex. From fetching the latest language models from the [Snips Console](https://console.snips.ai), to setting up a custom microphone configuration, to binding with a multitude of skills, requires a lot of cumbersome work. We created Snips Skills to automate this process as much as possible, so that in fact all this work can be done declaratively in a single file, the Snipsfile.

With the Snipsfile, an assistant can be entirely specified and run with a simple command, and does not require a single line of code. As an added benefit, it is very easy to share an assistant: rather than copying a repository of code, only Snipsfiles need to be shared.

#### Snips platform architecture

The [Snips Voice Platform](https://www.snips.ai) takes as input either text or an audio signal, as produced by a microphone. In the latter case, it uses Automatic Speech Recognition (ASR) to transcribe the audio signal into spoken text. Next, using Natural Language Understanding, it transform the text into an intent, which is a payload that includes the intention in the phrase, and slots  represents the meaning of the phrase