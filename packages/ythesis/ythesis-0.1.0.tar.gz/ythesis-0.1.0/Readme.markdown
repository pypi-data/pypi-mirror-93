Exclock
=======

![image](https://img.shields.io/pypi/v/exclock)
![image](https://img.shields.io/pypi/pyversions/exclock)
![image](https://gitlab.com/yassu/exclock/badges/master/pipeline.svg)
![image](https://gitlab.com/yassu/exclock/badges/master/coverage.svg)
![image](https://img.shields.io/pypi/l/exclock)

exclock is a cui extended timer.

Required
--------

-   mplayer
-   xmessage or terminal-notifier(If you use mac, I recommend
    terminal-notifier)

How to install
--------------

    $ pip install exclock

Usage
-----

    $ exclock [options] {clock-filename}

Features
--------

-   Sound an alarm at a specified time.
-   Sound the alarm after the specified time has elapsed.
-   You can flexibly set the alarm.

Options
-------

-   `--version`: show program's version number and exit
-   `-h, --help`: show this help message and exit
-   `-l, --list`: show clock names in your PC and exit
-   `-t, --time`: Time which spends until or to specified
-   `-r, --ring-filename`: Sound-filename which used for ringing with
    -t, --time option. Note that you can use EXCLOCK\_RING\_FILENAME
    system variable if you often indicate ring-filename option.
-   `--trace, --traceback`: show traceback

How to sound an alarm at a specified time
-----------------------------------------

Enter

    $ exclock -t {time}

format command.

Where time is given in the {hour}:{min} or {hour}:{min}:{sec} format.

Ex.

    $ exclock -t "1:00"
    $ exclock -t "1:00:20"

How to sound the alarm after the specified time has elapsed
-----------------------------------------------------------

Enter

    $ exclock -t {time}

format command.

Where time is given in the {sec}, {sec}s, {min}m or {min}m{sec}s.

Ex.

    $ exclock -t 3
    $ exclock -t 3s
    $ exclock -t 2m
    $ exclock -t 2m3s

How to flexibly set the alarm
-----------------------------

Enter

    $ exclock {clock-filename}

format command. Although {clock-filename} can be omitted as descrived
below.

clock-file should be a file in json5 format.

Official page for json5 format is [Here](https://json5.org/).

clock file format
-----------------

    {
      "title": "title(optional)",
      "sounds": {
        "time1": {
          "message": "message1",
          "sound_filename": "sound_filename1",
        },
        "time2":{
        "message": "message2",
        "sound_filename": "sound_filename2",
        },
        ...
      },
      "show_message": show_message(optional),
      "loop": loop_number(optional)
    }

-   title(Optional): string which be used for notification. Then the
    property is computed from clock-filename if this option is not
    indicated.
-   sounds: dictionary from time to dictionary which includes message
    and sound\_filename.
    -   time format is "{sec}", "{sec}s", "{min}m" or "{min}m{sec}s"
        format.
    -   message is a string which be used for notification and terminal
        output. Then message is replaced by "{count}" to number of how
        many times execute.
    -   sound\_filename is a string which be used for play the sound.
-   show_message(Option): bool of show_message using xmessage or terminal-notifier
-   loop(Option): number of iterations for above clock timer. If this is
    nil, this means repeatation a number of times. Default value is 1.

There are sample files in [sample dir in
gitlab](https://gitlab.com/yassu/exclock/-/tree/master/exclock/assets/clock).

How to omit clock filename
--------------------------

Clock filename can be omitted for some case.

Rules are

-   If extension of clock filename is .json5, extension can be
    omitted(ex: pomodoro.json5 =&gt; pomodoro).
-   If dir is in the specified directory(\~/.config/exclock/clock/ or
    environment variable EXCLOCK\_CLOCK\_DIR), dir is omitted (ex:
    \~/.config/exclock/clock/abc.json5 =&gt; abc).
-   Buitin clock file can be accessed. There are in [sample dir in
    gitlab]() (ex: 3m or pomodoro).

How to omit sound filename
--------------------------

Sound filename can be omitted for some case.

Rules are

-   If dir is in the specified directory(\~/.config/exclock/sound/ or
    environment variable EXCLOCK\_SOUND\_DIR), dir is omitted (ex:
    \~/.config/exclock/sound/abc.mp3 =&gt; abc.mp3).
-   Buitin sound file can be accessed. There are in [sample sound dir in
    gitlab](https://gitlab.com/yassu/exclock/-/tree/master/exclock/assets/sound)
    (ex: silent.mp3 or ring.mp3).

LICENSE
-------

[Apache 2.0](https://gitlab.com/yassu/exclock/blob/master/LICENSE)
