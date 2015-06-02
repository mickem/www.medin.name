Real-time log file monitoring (both event log and text files)
#############################################################
:date: 2012-11-26 23:50
:author: mickem
:category: Monitoring
:tags: eventlog, icinga, nagios, nsclient++, realtime
:slug: real-time-log-file-monitoring-both-event-log-and-text-files
:image: /images/real-time-log-file-monitoring-both-event-log-and-text-files-image.png
:social_image: /images/real-time-log-file-monitoring-both-event-log-and-text-files-image.png

Time for yet another tutorial this time detailing how to monitoring log
files both event log and regular text files. The event log parts will
build a bit on the earlier posts on monitoring the event log but since
the “event log cache” feature has been replaced by the generic
SimpleCache in 0.4.1 as well as 0.4.1 introducing a new SimpleFileWriter
module as well  I felt it was time to re-visit this topic.

.. PELICAN_END_SUMMARY

Introduction
------------

One of the new modules introduced in
`NSClient++ <http://nsclient.org/>`__ 0.4.1 was the CheckLogFile which
is similar to CheckEventLog except it works on log files which are in
text format. The idea behind this module was to proved the same powerful
real-time monitoring features that I introduced with CheckEventLog but
also to show how the new “warning and critical” check syntax will become
in 0.4.2.  So in a way this is a gateway to the syntax of future
versions of NSClient++.

In addition to CheckLogFile another module called SimpleCache was also
introduced which replaced the temporary “event log cache” feature I
introduced in 0.4.0. Simple cache is generic so it can be used for other
things in addition to CheckEventLog. We shall also briefly touch o the
SimpleFileWriter which can be used to write notifications to file.

But enough introduction lets get start by introducing real time
monitoring.

Real time monitoring
--------------------

The idea behind real-time monitoring is that instead of poll for changes
we have modules notifying the system when changes occur. Classically
this is in the Nagios space called “passive monitoring”. I don’t like
that word so I tends avoid it and instead use real-time monitoring. Both
CheckEventLog and CheckLogFile supports event driven architecture this
means the kernel in the operating system, will notify subscribes of
changes thus there is very little overhead.

The setup is similar in both cases so we will walk through them in
parallel.

The overall design of our first incarnation will look like this:

|image|

ON the left we have two modules which receives events from the
underlying operating system. They send the events (in the form of
notifications) to multiple channels (the (NSCA, CACHE, FILE). The
channels each has a subscriber (in the form of another plugin) which
turn the notification into an action.

#. NSCAClient
   Sends notification to remote
   Nagios/\ `Icinga <https://www.icinga.org/>`__ via NSCA.
#. SimpleCache
   Caches events for later use by for instance NRPE commands
#. SimpleFileWriter
   Writes notification to a regular text file

So lets loo into how we configure the CheckEventLog module first.

Configuring real-time event log checks
--------------------------------------

For CheckEventlog we need essentially three things:

#. Load the module

.. code-block: ini

   [/modules]
   CheckEventLog = enabled


#. Enable real time monitoring

.. code-block: ini

   [/settings/eventlog/real-time]
   enabled = true

#. Create a simple filter

.. code-block: ini

   [/settings/eventlog/real-time/filters/eventlog]
   filter=level = 'error'
   target=NSCA,CACHE,FILE

I wont go into the details as this has all been covered in earlier blog
posts:

-  `Self-resetting eventlog alerts <http://blog.medin.name/?p=396>`__
-  `Real-time eventlog monitoring with
   NSClient++ <http://blog.medin.name/?p=287>`__

Suffice to say is the important things to notice are target sets the
channels we submit the message to this is a coma separated list with
specify all three modules since we want to fire everything. Next up is
configuring real-time log file monitoring.

Configuring real-time log file monitoring
-----------------------------------------

Real-time log file monitoring is pretty easy to configure as well and
very similar. Again we need three things.

#. Load the module

.. code-block: ini

   [/modules] CheckLogFile = enabled

#. Enable real time monitoring

.. code-block: ini

   [/settings/logfile/real-time]
   enabled = true

#. Create a simple filter

.. code-block: ini

   [/settings/logfile/real-time/checks/logfile]
   file = ./test.txt
   destination = NSCA,CACHE,FILE
   filter = column1 like 'hello'
   critical = column2 like 'world'
   column separator=;

Again I wont go into details as the information can be found in the post
where I presented my slides from OSMC 2012:

-  `Slides from OSMC 2012
   pressentation <http://blog.medin.name/?p=433>`__

An important thing to notice is the names are NOT consistent. This will
be fixed in 0.4.2 where there will be a consistent naming of things
(with backwards compatibility).

So notice the ***destination*** is now used instead of ***target*** they
both have the same function and behavior.

Another thing to notice is since I am on Windows this time I set
***column separator*** to ; as it is difficult to create “tab
characters” using the echo command in the command shell.

Configuring the rest
--------------------

Now that we have the important things in place (the real-time
monitoring) I will quickly introduce the rest we need to do:

#. Load all the other modules:

.. code-block: ini

   [/modules]
   SimpleFileWriter = enabled
   SimpleCache = enabled
   NSCAClient = enabled

#. Configure a default target for the NSCA destination

.. code-block: ini

   [/settings/NSCA/client/targets/default]
   address=nsca://127.0.0.1:5667
   encryption=aes256
   password=YL04nBb14stIgCjZxcudGtMqz4E6NN3W

This has already been covered many times before so I wont even mention
what this is/does.

-  `Self-resetting eventlog alerts <http://blog.medin.name/?p=396>`__
-  `Real-time eventlog monitoring with
   NSClient++ <http://blog.medin.name/?p=287>`__
-  `Slides from OSMC 2012
   pressentation <http://blog.medin.name/?p=433>`__

The entire configuration looks like this:

.. code-block: ini

   [/modules]
   CheckLogFile = enabled
   CheckEventLog = enabled
   SimpleFileWriter = enabled
   SimpleCache = enabled
   NSCAClient = enabled
   
   [/settings/eventlog/real-time]
   enabled = true
   
   [/settings/eventlog/real-time/filters/eventlog]
   filter=level = 'error'
   target=NSCA,CACHE,FILE
   
   [/settings/logfile/real-time]
   enabled = true
   
   [/settings/logfile/real-time/checks/logfile]
   file = ./test.txt
   destination = NSCA,CACHE,FILE
   filter = column1 like 'hello'
   critical = column2 like 'world'
   column separator=;
   
   [/settings/NSCA/client/targets/default]
   address=nsca://127.0.0.1:5667
   encryption=aes256
   password=YL04nBb14stIgCjZxcudGtMqz4E6NN3W

And this is pretty much it.

If we start NSClient++ now and either generate event into the event log
or the text file we subscribe to (test.txt) we will see everything fire
meaning we get a notification sent to NSCA, we get a record in the cache
and we get a new entry in our log file.

Before we test this though we need to make sure we have the file created
since we cant listen to events from a non existing file.

So lets create the file and start NSClient++ in test mode.

.. code-block: text

   echo. > test.txt
   nscp test --log info

Next up we fire up another console and add some data to our file:

.. code-block: text

   echo hello;world >> test.txt

In my case I get errors in the console since I have not configured a
proper NSCA server if your NSCA server is responding you will not see
anything but on the other hand you will hopefully receive some nifty
messages.

.. code-block: text

   e lient\\NSCAClient.cpp:435 Error: Failed to connect to: 127.0.0.1:5667

Next we want to verify that the SimpleFileWriter works so lets open up
the a file called ***output.txt*** where you should see something along
the following lines:

.. code-block: text

   logfile OK ./test.txt: 1 (hello;world , , )

Finally we want to confirm the cache module which we can do using the
***check_cache*** command like so:

.. code-block: text

   check_cache index=logfile
   l ce\\simple_client.hpp:80 OK:./test.txt: 1 (hello;world , , )

Which means it seems that everything is working. If we wait for a bit we
will most likely get a few message from the event log as well or we can
use NSClient++ to inject some messages (see my blog for details:
`Real-time eventlog monitoring with
NSClient++ <http://blog.medin.name/?p=287>`__ ).

The conclusion
--------------

So there we have it: a crash course in using the new real time
facilities in NSClient++ 0.4.1.

Much of this is brand new and “experimental” so please use with care but
please use it so any bugs can be found (and don’t forget to report any
bugs you found).

The most important point is that I implemented all these as a proof of
concept on how I think monitoring can be made simpler and easier. But I
would very much like to get some feedback on it as well as please let me
know how this could be made more useful and how I could tweak and extend
this to help solve ***YOUR PROBLEMS!***

.. |image| image:: /images/real-time-log-file-monitoring-both-event-log-and-text-files-image.png
