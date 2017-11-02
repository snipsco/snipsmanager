---
layout: doc
title:  "Viewing logs"
permalink: /getting-started/view-logs/
---

At times, it is useful to inspect what is going on with your device while it is running.

You can inspect the real-time logs on your system as follows:

```sh
$ sam logs
2017-10-27T21:00:20+01:00 sam[system]: Device started
2017-10-27T21:00:25+01:00 sam[mqtt]: New message on topic /hermes/hotword/toggleOn
2017-10-27T21:00:25+01:00 sam[mqtt]: New message on topic /hermes/asr/toggleOn
2017-10-27T21:00:25+01:00 sam[mqtt]: New message on topic /hermes/hotword/toggleOff
```

You may filter on log tag using the `--tag` flag:

```sh
$ sam logs --tag=mqtt
```

To view all the logs, add the `--all` flag. This might be long, so you may want to pipe the output to a file:

```sh
$ sam logs --all > logs.txt
```

### Watching messages

Alternatively, you can watch only the intents which are being detected. For this, use the `watch` command:

```sh
$ sam watch
↯ Hotword detected

Query: Is it going to be sunny in Chicago this week-end
Intent: SearchWeatherForecast
        weatherForecastLocality       locality        chicago
        weatherForecastStartDatetime  snips/datetime  this weekend
```

For more commands, see the [Logging]({{ site.baseurl }}/articles/logging/) article.

<br />
<a class="button is-primary" href="{{ site.baseurl }}/getting-started/the-snipsfile/">
  I know how to inspect logs
</a>
<a class="button" href="#">
  Report a problem
</a>
