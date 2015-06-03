Real time event-log monitoring with NSClient++
##############################################
:date: 2012-03-20 08:41
:author: Michael Medin
:category: Monitoring
:tags: eventlog, monitoring, nagios, NSCP
:slug: real-time-event-log-monitoring-with-nsclient
:image: /images/real-time-event-log-monitoring-with-nsclient-image.png
:social_image: /images/real-time-event-log-monitoring-with-nsclient-image.png


Monitoring the event log can quickly become straining for both the
computer as well as the administrator as the event log grows and grows.
To make this simpler for both the administrator and the computer
NSClient++ 0.4.0 introduced real-time event log monitoring. This means
we no longer scan the event log instead we simply scan events as they
come in. The benefit, in addition to lowering the resources required, is
that we can also get notified instantly when an error occurs instead of
every 5 minutes or however often we check the log. Another addition is a
simple client o generate event log message to help administrators debug
event log filters. This is a quick introduction to event log monitoring
and real-time event log monitoring showing how to set up real-time event
log monitoring both for active and passive use via NSCA and NRPE.

.. PELICAN_END_SUMMARY

Event Log
=========

So to start this off first we need to understand how the event log works
and what we can do with it. The first thing to notice is that the event
log is a bit “odd”. The core event log message is an EVENTLOGRECORD
which is we simplify a bit has the following fields:\ |image|

-  RecordNumber
   Sequence number
-  TimeGenerated
   The time at which this entry was submitted.
-  TimeWritten
   The time at which this entry was received by the service to be
   written to the log.
-  EventID
   See below
-  EventType
   The type of message is one of the following:

   -  Error
   -  Failure Audit
   -  Success Audit
   -  Information
   -  Warning

-  Strings
   TODO:    A list of strings for rendering the message.
-  EventCategory
   TODO:    A token with which the developer can provide filtering and such.
-  UserSid
   Security identifier of the “active user” when the event was logged.

EventID
-------

Now event id seems to me like something which is not really used as
intended or was badly designed. The general idea is that each message
(read text) has a unique identifier provided by the implementing
application. Thus far it is even pretty smart as it means that the event
log does not contain any actual messages only an id and some metadata.
The oddities if you ask me is that they decided to use the event-id for
a lot of other things as well. The field contained in this number (and
since it is a number many of these are just bits) are:

-  Severity. The severity is defined as follows:

   -  00 – Success
   -  01 – Informational
   -  10 – Warning
   -  11 – Error

-  Customer bit. This bit is defined as follows:

   -  0 - System code
   -  1 - Customer code

-  Facility
   Facility code (I think of this as a component within the
   application).
-  Code
   Number identifying the message

|image|\ The first thing to notice is that if you look at modern windows
the event viewer will not show you any of this information unless you
“click advanced” and then only as a number next to the name Qualifiers.

|image|\ The second thing is that some of these fields are a bit odd.
Severity sounds a lot like “type” or level as it is called now. Facility
sounds a lot like source. None of these fields will help provide any
information for the end user and is mainly intended for the developer to
help them organize message files or so it seems to me.

Back to NSClient++
==================

So what can we do in NSClient++?

Well, first off we have two commands:

-  check_eventlog
-  check_eventlog_cache

There is also one command line command available used to generate event
log messages (mainly useful when debugging filters).

So why two commands?

Well, the first command is the “old normal” check command when every
time you run the check the entire event log is scanned which means if
you have a few hundred thousand items it will quickly use up a lot of
resources.

To combat this in 0.4.0 I introduced something called “real-time” event
log monitoring. The idea is that we listen for events and as they happen
we scan them and match them against the filters. The up side of this is
obviously a much reduced CPU footprint. as we instead of every 5 minutes
have to scan hundreds of thousands of entry's we only have to scan the
hand full your server generates. The other benefit is that we can now
get real-time errors if we use passive checking. So you no longer have
to wait “for 5 minutes” instead once the error is triggered you get the
red light in your monitoring tool almost instantly.

But lets start with understanding filters.

Filters
-------

Filters was introduced in 0.3.8 of NSClient++ and consists of something
similar to SQL statements (or WQL statements for that matter) where you
can filter information you want. As of 0.4.0 we have the following
keywords on which we can filter:

-  Numbers:

   -  id
      The event id
   -  category
      The event category
   -  qualifier
      Qualifier part of event id
   -  facility
      Facility part of event id
   -  customer
      Customer bit part of event id
   -  rawid
      The entire event id including any qualifier/facility/customer/\*
      parts
      This is obviously faster than separating them into multiple
      statements.

-  Strings

   -  source
      Event source
   -  file / log
      Log file
   -  message
      The renderd message
   -  strings
      The string data (used to render the message)
      This is much much faster and yields the same result as message.
   -  computer

-  Dates

   -  written
   -  generated

-  Keywords

   -  type (level)
   -  severity

So essentially we can filter on anything except sid which for some
strange reason I missed |Ler|. Writing filters is pretty straight
forward as well and if you know some basic SQL you should not have too
much trouble. This article is not about writing event log queries so I
will only give you an example here (let me know if you want me to write
an article about writing filters):

.. code-block:: text

   generated gt -2d AND severity NOT IN ('success', 'informational')

Real time event log
-------------------

Real time event log monitoring is almost simpler to set up then using
server-side checks. The drawback though is that it requires up-front and
client-side configuration which is obviously not for everyone.

.. code-block:: ini

   [/modules]
   CheckEventLog=1
   
   [/settings/eventlog/real-time]
   enabled=true
   filter=id = 1000 and category = 0

The above configuration will do two things, first enable CheckEventLog
module and then enable real-time checking. We also configure a random
filter I was using when testing something. So configuring this is pretty
straight forward and simple. Apart from this there are a hand full of
options you can tweak as well. The only problem here is what happens
when you hit a message?

Well, since we have not configured a destination nothing will happen so
thus far this is a bit useless. Unfortunately this blog post is not
about configuring NSCA so the next section will only skim through it a
bit. But first lets look at the other options we can tweak:

-  enabled
   Spawns a background thread which detects issues and reports them
   back instantly.
-  destination
   The destination for intercepted messages
-  maximum age
   How long before reporting "ok" (if this is set to off no ok will be
   reported only errors)
-  filter
   The initial age to scan when starting NSClient++
-  syntax
   The initial age to scan when starting NSClient++
-  log
   Coma separated list of logs to check
-  debug
   Log missed records (useful to detect issues with filters) not useful
   in production as it is a bit of a resource hog.
-  enable active
   This will store all matches so you can use real-time filters from
   active monitoring (use CheckEventlogCache).
-  ok message
   This is the message sent periodically when no error is discovered.
-  alias
   The alias to use for this event (in NSCA this is the service name).

NSCA
----

If we are planning to use this with NSCA (and we are) there are a few
things to extra to configure. First we have a concept called
service_name which we need to define. A service name is the way Nagios
(or Icinga) associates the result with a check. So if you have multiple
checks you need to be able to configure multiple service names for
different filters. The way this is handled is using aliases. Aliases can
be configured in two ways:

#. Locally by settings the key for the filter query under […/filters].
#. Globally in the […/real-time] section
   All filters without alias will use this alias.

So if you in Nagios have two different service_checks (eventlog_1 and
eventlog_2) you need to set this using the […/filters] section like so:

.. code-block:: ini

   [/settings/eventlog/real-time/filters]
   eventlog\_1=id = 1000 and category = 1
   eventlog\_1=id = 1000 and category = 0

The other thing we need to configure is the NSCA client itself which for
simple scenarios is pretty straight forward to configure as well:

.. code-block:: ini

   [/modules]
   ; ...
   NSCAClient = 1
   
   [/settings/NSCA/client/targets/default]
   address=nsca://127.0.0.1:5667
   encryption=aes256
   password=YL04nBb14stIgCjZxcudGtMqz4E6NN3W

Finally we need to tell CheckEventlog to send messages to NSCA which is
done by specifying the destination:

.. code-block:: ini

   [/settings/eventlog/real-time]
   ; ...
   destination=NSCA

Causing problems
----------------

Now, how can we test this (apart from sitting around waiting for
something to happen?

Well, NSClient++ provides a rather nifty (and dangerous) command which
allow you to inject messages into the event log.

.. code-block:: bat

     nscp eventlog
     CheckEventLog Command line syntax:
     Allowed options:
     -h [ --help ] Show help screen
     -s [ --source ] arg (=Application Error)
     source to use
     -t [ --type ] arg Event type
     -l [ --level ] arg Event level (type)
     -f [ --facility ] arg Facility/Qualifier
     -q [ --qualifier ] arg Facility/Qualifier
     --severity arg Event severity
     -c [ --category ] arg Event category
     --customer arg Customer bit 0,1
     -a [ --arguments ] arg Message arguments (strings)
     --eventlog-arguments arg Message arguments (strings)
     --event-arguments arg Message arguments (strings)
     -i [ --id ] arg Event ID

In our case since we filter on event id 1000 we can use the following
command to insert an application error.

.. code-block:: bat

   nscp eventlog --exec insert-eventlog --source "Application Error" --id 1000 --level error --category 0

Which will trigger the following message to be sent to NSCA: ***“Felet
uppstod i programmet med namn: %1, version %2, tidsstämpel 0x%3…”*** all
the %1, %2 represent insert points which is where your event log message
strings would normally end up. To add this we can add a series of
--eventlog-argument options to insert some strings into these markers
like so:

.. code-block:: bat

   nscp eventlog --exec insert-eventlog --source "Application Error" --id 1000 --level error --category 0 --eventlog-argument a --eventlog-argument b ...

Active monitoring and real time
===============================

So maybe you are thinking, darn I just configure everything to use
active monitoring via NRPE, cant I get any real-time goodness? Well
fortunately the answer is: Yes you can!

**UPDATE** The details in this section is deprecated as in 0.4.1 the
check_eventlog_cache command was replaced by the more generic
check_cache command in the SimpleCache module. It works the same though
so the concepts are still valid. For details about the SimpleCache
module please refer to the following blog posts:

-  `Real-time log file monitoring (both event log and text
   files) <http://blog.medin.name/2012/11/26/real-time-log-file-monitoring-both-event-log-and-text-files/>`__
-  `Self-resetting event log
   alerts <http://blog.medin.name/2012/09/09/self-resetting-event-log-alerts/>`__

If you recall we had two commands: check_eventlog and
check_eventlog_cache and the latter does just that. This is done by
configuring active monitoring to store all matches for you and then you
can check the results cache using the check_eventlog_cache command.

To enable this we need to add one more option to the configuration file.

.. code-block:: ini

   [/settings/pytest\_eventlog/real-time]
   ;...
   enable active=true

And then we need to run the following command:

.. code-block:: bat

   check\_eventlog\_cache warn=gt:0 crit=gt:0

Which will give you a critical message when you have more then 0 items
in the cache. Be advised though that when you check the cache the cache
is emptied meaning you will only get this warning "the first time” if
you only have a single problem. So be sure you configure your Nagios
server accordingly. Currently this is a bit simple and not very powerful
so while you can use it it might not be what you are looking for and if
that is the case please let me know so I can improve it in the future.

Summary
=======

So I think with the introduction of filters in 0.3.8 and real-time
filters in 0.4.0 as well as the ability to inject errors into the event
log makes CheckEventlog a both powerful and simple tool for checking for
errors in your event log. That’s pretty much it for now, please let me
know what you want me to write about next!

**UPDATE:** Added information about check_eventlog_cache being
replaced by the more generic check_cache.

.. |image| image:: /images/real-time-event-log-monitoring-with-nsclient-image.png
   :target: /images/real-time-event-log-monitoring-with-nsclient-image.png
.. |image2| image:: /images/real-time-event-log-monitoring-with-nsclient-image1.png
   :target: /images/real-time-event-log-monitoring-with-nsclient-image1.png
.. |image3| image:: /images/real-time-event-log-monitoring-with-nsclient-image2.png
   :target: /images/real-time-event-log-monitoring-with-nsclient-image2.png
.. |Ler| image:: /images/wlEmoticon-smile1.png
