Self-resetting event log alerts
###############################
:author: Michael Medin
:tags: eventlog, icinga, nagios, nsclient++, windows
:image: /images/thumbnails/300x-/1098106984_d250a227fb_b.jpg
:social_image: /images/thumbnails/300x-/1098106984_d250a227fb_b.jpg

Take your monitoring to the next level by
creating self-resetting event log checks. Sometimes it is not only
faults which can be harvested from the windows event log many
applications will also report a message when the state returns to
normal. This tutorial show you how to configure NSClient++ 0.4.1 to
setup auto resetting event log checks. In addition to using passive
checks via NSCA I will also demonstrate how to use the Cache module to
benefit from real time event log checks via NRPE.

.. PELICAN_END_SUMMARY

Traditionally event log checking (Using NSClient++) has been "if more
than X errors in Y minutes" something is bad. This is a rather crude and
edge weapon. The next step has generally been to filter out some noise
which leaves you with pretty much the same result albeit more
configuration. It is still important to do this but it is not very nice
to have this as your primary monitoring. With the advent of real-time
event log checking introduced in NSClient++ 0.4.0 we showed that we
could do much better without losing to many hours configuring things.
And here I will show how to harness the full power of real-time event
log checking do get some much-needed intelligence back into the event
log monitoring.

The application
===============

We will work with a fictive application here which reports three
messages of varying degree (one being “ok”).

#. Id=100: I am broken!
#. Id=200: I am feeling so-so
#. Id=300: I am awesome!

So what we want to see in Nagios is CRITCAL for the first message above
and WARNING for the second one and finally an OK for the last message.
This means that the Nagios status would directly reflect the status of
the real application which is nice.

In earlier version of NSClient++ (before 0.4.1) we could do this using
some custom scripts and the built-in check_eventlog command. But with
0.4.1 we can do this purely with configuration which makes things much
simpler. To set this up we will need a series of real-time event log
filters which corresponds to the various messages above and abuse the
alias property to fool NSClient++ and Nagios into thinking they are all
the same event.

But before we get into that lets first look at real-time event log
filtering. I previously did a
`post <http://blog.medin.name/2012/03/20/real-time-event-log-monitoring-with-nsclient/>`__
where I introduced event log monitoring including real-time event log
monitoring so feel free to head over there and read up on `real-time
event log
monitoring <http://blog.medin.name/2012/03/20/real-time-event-log-monitoring-with-nsclient/>`__
before continuing reading this post to get your bearings.

But lets have a quick recap here. Real-time event log monitoring is a
mode where NSClient++ subscribes to messages from the event log and when
new messages are added to the log it will receive a notification and run
filtering logic on all new message and report any events matching your
configuration. The message are then normally sent to Nagios via NSCA or
similar means.

The filters we create consist of a filer string (using the same SQL
syntax used used in the normal event log checks) in addition to this we
have a series of attributes we can configure to control what happens
when a filter is matched.

An example of a real-time event log filter can be found here:

.. code-block::ini

   [/settings/eventlog/real-time]
   enabled = true
   [/settings/eventlog/real-time/filters/my_filter]
   # Report all messages with level = error (ie. errors)
   filter=level = 'error'
   # Send this to the NSCAClient for further dispatching to Nagios.
   target=NSCA
   # Report this message as a CRITICAL alert.
   severity=CRITICAL

This means when an error is reported in to the event log NSClient++ will
submit a CRITICAL message to Nagios via NSCA (assuming we have configure
the NSCA module).

The message sent will have an command/alias (service name in Nagios)
my_filter.

Configuration
=============

In our case it is slightly more complicated, we will start by adding
three filters one capturing each application message as we stated
initially by filtering on id = 100, 200 and 300.

.. code-block:: ini

   [/settings/eventlog/real-time]
   enabled = true
   
   [/settings/eventlog/real-time/filters/ourapp\_ok]
   filter=source = 'ourapp' AND id = 100
   severity=OK
   destination=NSCA
   
   [/settings/eventlog/real-time/filters/ourapp\_warning]
   filter=source = 'ourapp' AND id = 200
   severity=WARNING
   destination=NSCA
   
   [/settings/eventlog/real-time/filters/ourapp\_critical]
   filter=source = 'ourapp' AND id = 300
   severity=CRITICAL
   destination=NSCA

If we were to use this we would most likely get errors reported by NSCA
Server saying it drops messages because of unknown service name.

That is because the default “service name” is the last part of the
filter path (in our case “ourapp\_…” which is presumably not what we
have configure in Nagios. To get around this we need another property as
well which configures the alias/command (service name) of the event sent
to Nagios.

In our case we want the SAME service name for all messages so we need to
set this to the same value.

Thus we end up with the following:

.. code-block:: ini

   [/settings/eventlog/real-time]
   enabled = true
   
   [/settings/eventlog/real-time/filters/ourapp\_ok]
   filter=source = 'ourapp' AND id = 100
   severity=OK
   destination=NSCA
   command=check\_ourapp\_eventlog
   
   [/settings/eventlog/real-time/filters/ourapp\_warning]
   filter=source = 'ourapp' AND id = 200
   severity=WARNING
   destination=NSCA
   command=check\_ourapp\_eventlog
   
   [/settings/eventlog/real-time/filters/ourapp\_critical]
   filter=source = 'ourapp' AND id = 300
   severity=CRITICAL
   destination=NSCA
   command=check\_ourapp\_eventlog

Now what happens is that NSClient++ will always report these matches
against the service name check_ourapp_eventlog which means we get all
messages correlated against the same service.

**Testing it**
==============

I tend to want to test my setup in a controlled environment. I guess I
could go on and claim that is because it is so boring to wait for months
and months for the application to break before I get to see the wonders
of my work. But alas the sad truth is that I tend to make a lot of silly
mistakes so the only way for me to make sure things are correct is to
test it.

With NSClient++ 0.4.0 we introduced the command line event log poster
which is what I will use here to test this. **Notice before you try this
it will add ACTUAL errors in your event log so do this only on your test
rig not the actual production server!**

The syntax to inject messages can be displayed by running "nscp
eventlog" without any options:

.. code-block:: text

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

In our case we want to set id to 100, 200 and 300 as well as source to
ourapp so we end up with (I add level error for good sake as well but
this is not really necessary):

.. code-block:: text

   d:\\source\\nscp\\build\\x64>nscp eventlog --level error --id 100 --source ourapp
   Message reported successfully

The best way to test this is to open up two command windows one running
NSClient++ in “test mode” and the other posting the messages.

|image|

You might have noticed I get two errors here. The first one: “Could not
extract DLL for eventsource: ourapp:…” is due to this being a fake
application I actually don’t have an application called ourapp on my
system so the log message will not render at all. The other message is
“No one listens for events from: NSCA (NSCA)” which is due to the fact
that we have not configured NSCA (yet) so the messages we send are not
sent correctly.

Templates
=========

Another nice feature we should get in the habit of using is templates.

Templates allow you to "inherit" (to use programming talk) properties
from a more general definition. If you have worked with Nagios you are
probably aware of the concept (and their use).

Since we NSCA in all of these as well  as override the command we can
save ourselves a few lines of configuration by using templates but
mainly it is easier to make changes (which we will do later on) if you
do.

SO we create a template called orapp_template which sets destination,
command as well as the magic "is template" option. This option prevents
this template for becoming registered as a filter.

.. code-block:: ini

   [/settings/eventlog/real-time]
   enabled = true
   
   [/settings/eventlog/real-time/filters/ourapp\_template]
   destination=NSCA
   command=check\_ourapp\_eventlog
   is template=true
   
   [/settings/eventlog/real-time/filters/ourapp\_ok]
   template=ourapp\_template
   filter=source = 'ourapp' AND id = 100
   severity=OK
   
   [/settings/eventlog/real-time/filters/ourapp\_warning]
   template=ourapp\_template
   filter=source = 'ourapp' AND id = 200
   severity=WARNING
   
   [/settings/eventlog/real-time/filters/ourapp\_critical]
   template=ourapp\_template
   filter=source = 'ourapp' AND id = 300
   severity=CRITICAL

Not too much saved maybe but this is a very short example so you will
hopefully save some more once you start doing this yourself.

Configuring NSCA
================

What we have been missing thus far I NSCA we send the message but no one
wants them to resolve this we need to configure a NSCA client as well. I
will not go into details here since this is about event log monitoring
and not NSCA configuration but the following is a simple chunk for
setting up a very basic NSCA client (this chunk is straight from the
event log previous event log monitoring post

.. code-block:: ini

   [/modules]
   ; ...
   NSCAClient = 1
   
   [/settings/NSCA/client/targets/default]
   address=nsca://127.0.0.1:5667
   encryption=aes256
   password=YL04nBb14stIgCjZxcudGtMqz4E6NN3W

**Active Monitoring (NRPE)**
============================

The last thing we are going to cover is the all-new SimpleCache module
which is the first tiny step along the lines of CEP (Complex Event
Processing) based monitoring.

To quickly explain what the SimpleCache module do is that it listens to
messages (much like the NSCAClient module) but instead of sending them
it stores them internally. This stored data can them be retrieved using
the check_cache command.

Configuring the SimpleCache module is extremely simple all we can really
tweak is the channel to listen on and the index to use when caching
results.

.. code-block:: ini

   [/modules]
   ; SimpleCache module - Caches results for later checking.
   SimpleCache = enabled
   
   ; Section for simple cache module (SimpleCache.dll).
   [/settings/cache]
   
   ; CHANNEL - The channel to listen to.
   channel = CACHE
   
   ; PRIMARY CACHE INDEX - Set this to the value you want to use as unique key for the cache (host, command, result,...).
   primary index = ${alias-or-command}

The default channel is CACHE and the default index is alias-or-command
which is exactly what we want so we need not enter anything at all
really apart from loading the module. This is really not about
SimpleCache but a quick note about the index might be in order. The
default ${alias-or-command} will expand to the alias or command which
means that each service check will get their own entry in the cache.
This is normally what you want but some times it might not be unique
enough for instance if you were to have two caches you might need to
prefix the index setting “primary index=cache1-${alias-or-command}” or
if you check multiple hosts you might want to add ${host} in there as
well.

Now if we run check_cache index=check_ourapp_eventlog we get ok after
the ok message is submitted and the next time we get a warning since we
have submitted the warning state message.

.. code-block:: text

   check\_cache index=check\_ourapp\_eventlog
   d rvice\\NSClient++.cpp:958 Result check\_cache: OK
   l ce\\simple\_client.hpp:80 OK:Our application works
   
   check\_cache index=check\_ourapp\_eventlog
   d rvice\\NSClient++.cpp:958 Result check\_cache: WARNING
   l ce\\simple\_client.hpp:80 WARNING:Our application is not good

Rounding off
============

This post is the main reason I have not been blogging for some time. As
always I promised to talk about features I had not finished at OSMC so I
have been spending all my “computer time” trying to get the features I
need for OSMC. Now the only remaining feature is the Logfile checker
which means I will hopefully have more time to blog now (unless people
report a lot of bugs that is |Ler|).

Next up is (besides some non NSClient++ stuff) some details on how to
actually secure your monitoring by adding client based certificates to
NRPE as well as NSCA and check_mk…

.. |image| image:: /images/self-resetting-event-log-alerts-image.png
.. |Ler| image:: /images/wlEmoticon-smile.png
