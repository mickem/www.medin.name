check_cpu with top consumers in NSClient++ (part 1 of 2)
########################################################
:date: 2013-12-04 22:11
:author: Michael Medin
:category: Monitoring
:tags: lua, monitoring, nagios, nsclient++, NSCP, script, windows
:slug: check_cpu-with-top-consumers-in-nsclient-part-1-of-2
:image: /images/check_cpu-with-top-consumers-in-nsclient-part-2-of-2.png
:social_image: /images/check_cpu-with-top-consumers-in-nsclient-part-2-of-2.png

An often requested feature is to include the top-5 consumers of high CPU
load in the result from check_cpu (or checkCpu). I have often discarded
this as a non-core feature since it is not something I think should be
part of `NSClient++ <http://nsclient.org/>`__ instead I think it should
be a script. Since no-one has created such a script I figured it would
make a nice blog post so here I describe in a step by step guide how to
create such a script for NSClient++.

.. PELICAN_END_SUMMARY

More than the sum of its parts
==============================

The first thing we need to explore is the feature of NSClient++ we need
to do this. All these is based of NSClient++ 0.4.2 since a lot of the
building block are not available in previous versions.

-  LUAScript
   The LuaScript module allows us to create and run
   `Lua <http://www.lua.org/>`__ scripts lua is a simple and easily
   embeddable scripting language used much in game development and other
   places where embedded development and performance are key. The great
   thing about Lua script is that the do not require any runtime
   infrastructure so you can use them out-of-the box with NSClient++ and
   as a bonus they are also platform independent which means our script
   can easily be modified to work on Linux as well as Windows.
-  check_cpu
   Since this is the check we are going to hi-jack we need it as we
   obviously do not want to re-invent the wheel. We will use check_cpu
   since it is the future version.
-  check_process
   We can easily use this command to fetch the process which consume
   cpu. Again we use the 0.4.2 version of the command check_process
   (the older checkProc does not provide cpu load).
-  filter_perf
   We could write code in the lua script to sort and filter the
   performance data but this feature is already provided by the
   filter_perf command.

Explore the parts
-----------------

So now we have the parts lets explore them a bit. I wont go into details
here about what these commands can do instead I will detail which
command lines we are interested in.

check_cpu
==========

We wont set any arguments for this command. instead we will pass through
any arguments given to our command to that command. This means that our
command works transparently and any new features added to check_cpu in
the future will be supported. But it can be good to explain some
arguments which can be sent to our script (and thus also to check_cpu).

.. code-block:: text

   check_cpu
   L client OK: CPU Load ok
   L client Performance data: 'total 5m'=0%;80;90 'total 1m'=0%;80;90 'total 5s'=7%;80;90

The most common argument is time which allows us to change the default
times to check (default is 5m, 1m and 5s).

.. code-block:: text

   check_cpu time=10s time=30s time=120s
   L client OK: CPU Load ok
   L client Performance data: 'total 10s'=13%;80;90 'total 30s'=13%;80;90 'total 120s'=7%;80;90

check_process
==============

Next up is check_process which we need to send a whole range of
arguments to to make it do what we want. The final command looks like
this:

.. code-block:: text

   check_process delta=true warn=user>0 filter=user>0
   L client WARNING: csrss.exe=started, dwm.exe=started, ...
   L client Performance data: 'csrss.exe user'=3;0;0 'dwm.exe user'=21;0;0 'nscp.exe user'=7;0;0 'WINWORD.EXE user'=3;0;0 'chrome.exe user'=3;0;0...

-  delta=true
   This tells the command to run a collection cycle of  second and
   collect the changes in this time period. This means the command will
   run for 1 second which is not optimal (and in future versions of
   NSClient++ we will be able to exploit real-time monitoring to get
   around this). This also means all values returned are the deltas over
   the second execution so and in the cpu load (user and kernel) case
   this means percentages.
-  warn=user>0
   This forces NSClient++ to provide the performance data for the user
   (user CPU time) metric.
-  filter=user>0
   Since a lot of the process will be idling (user=0) we filter them
   out since we are most likely not interested in them.

filter_perf
============

Notice in the previous command how the performance data is not sorted
(instead it is provided in order by the pid). We will use filter_perf
for this so notice below how the data is sorted.

.. code-block:: text

   filter_perf command=check_process sort=normal limit=5 arguments delta=true warn=user>0 filter=user>1
   L client WARNING: svchost.exe=started, explorer.exe=started, dwm.exe=started, nscp.exe=started, WINWORD.EXE=started, chrome.exe=started, ConEmuC64.exe=started, conhost.exe=started, trillian.exe=started, skypekit.exe=started, spotify.exe=started, WINWORD.EXE=started
   L client Performance data: 'dwm.exe user'=20;0;0 'nscp.exe user'=10;0;0 'spotify.exe user'=10;0;0 'ConEmuC64.exe user'=6;0;0 'conhost.exe user'=6;0;0

-  command=check_process
   This tells filter_perf which command to execute.
-  sort=normal
   Means we want to sort the data from large values to small values.
   Optionally we could give revers to get the least consuming processes.
-  limit=5
   Only give us the 5 first performance data entries and ignore the
   rest.
-  arguments
   Everything beyond this point is passed as-is to the command which we
   execute.

LUAScript
=========

LuaScript is not a command but a module. Writing Lua script has been
covered before `Statefull scripts <http://blog.medin.name/?p=447>`__ on
this blog and while the language may seem a bit odd at first it is
pretty simple to use and abuse for changing things around a bit. The
most important aspect is that it is included and requires nothing on the
run-time side and since it is running inside NSClient++ is it lightning
fast and can do a lot more then regular “external scripts”.

Some examples of this is interact with other commands, read and modify
the NSClient++ configuration etc etc.

The configuration for loading a lua script is pretty light as well:

.. code-block:: ini

   [/modules]
   LUAScript = enabled
   
   [/settings/lua/scripts]
   extcpu=check_cpu_ex.lua

Putting the pieces together
===========================

The last thing in this blog post is putting the pieces together. We wont
write the actual script here (stay tuned next week for this) instead we
will explain the way we intend to set the pieces together.

#. Create a new command check_cpu_ex
#. Execute check_cpu sending along all our command line arguments
#. Execute check_process using the delta feature to calculate the cpu
   load (user time) for all running processes.
#. Use filter_perf to sort and limit the performance data
#. change the return message of check_cpu to use the resulting
   performance data instead.

The finished result will look like this:

.. code-block:: text

   check_cpu_ex
   L client OK: Top consumers: 'trillian.exe user'=31;0;0 'dwm.exe user'=20;0;0 'spotify.exe user'=6;0;0 'nscp.exe user'=3;0;0 'SetPoint.exe user'=3;0;0
   L client Performance data: 'total 5m'=14%;80;90 'total 1m'=14%;80;90 'total 5s'=13%;80;90

Final words
===========

So now we have the components we need and next week I shall put the
pieces together and create the script. For the impatient the script can
already be found in the latest build of NSClient++.

.. code-block:: text

   check_nrpe --host 127.0.0.1 --command check_cpu_ex
   Top consumers: 'svchost.exe user'=25;0;0 'chrome.exe user'=13;0;0 'trillian.exe user'=11;0;0 'dwm.exe user'=8;0;0 'nscp.exe user'=5;0;0|'total 5m'=14%;80;90 'total 1m'=16%;80;90 'total 5s'=27%;80;90

**Please stay tuned for next week installment**: check_cpu top
consumers in NSClient++ (part 2 of 2)
