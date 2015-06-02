Scripting on the Windows side
#############################
:date: 2013-01-28 21:43
:author: Michael Medin
:category: Monitoring
:tags: monitoring, nrpe, nsclient++, NSCP, scripting, windows
:slug: scripting-on-the-windows-side
:image: /images/scripting-on-the-windows-side-image.png
:social_image: /images/image.png

The biggest reason for Nagios success is the ability to
extend it with custom scripts which makes it one of the most powerful
monitoring systems. Now `Nagios <http://www.nagios.org/>`__ is not the
only place where you can extend your monitoring!
`NSClient++ <http://nsclient.org/>`__ provides many ways to extend it
with scripts and since I have gotten many questions about how to use
scripts with NSClient++ lately I have decided to write this tutorial to
help sort out the concepts.

.. PELICAN_END_SUMMARY

My script is better than yours!
-------------------------------

First off there are two different types of script:

#. Internal scripts
#. External scripts

Internal scripts are running inside NSClient++ and have full access to
the inner workings of NSClient++ they are very powerful but only works
with NSClient++.

External scripts are much like how scripts work on Unix with Nagios.
They are programs which are executed by the operating systems and the
results are handed back to the caller.

For using internal scripts see previous blog posts as this will not be
covered here. This post is about using external scripts.

-  `Enhance your monitoring with stateful
   scripts <http://blog.medin.name/?p=447>`__
-  `Unit test your monitoring: Introducing unit tests in Python for
   NSClient++ <http://blog.medin.name/2011/10/23/creating-nsclient-unit-tests-in-python/>`__

External scripts
----------------

So what is an external script and where can you find one?

Answering the latter is easy there are two main sites where I tend to
look for scripts and they are:

-  https://www.monitoringexchange.org/
-  http://exchange.nagios.org/

As for the first part it is more difficult. An external scripts is a
program so technically it does not have to be a script (you can for
instance use NSClient++ it self as an external “script” if you want).
But usually it is (on Windows) vb-scripts or batch files and the more
modern powershell scripting language. But you can just as easily create
scripts in Perl, `Python <http://www.python.org/>`__,
`Lua <http://www.lua.org/>`__ or whatever language you feel comfortable
with just make sure the scripting environment is installed and working.
Best way to do this is to run the script from a windows command line:

Here you can see the command to test script in red and the resulting
message in blue.

To see the return status I use **echo %ERRORLEVEL%** which displays 0
(marked in green).

Now you might have noticed that when I run the batch script I add **cmd
/c “…”** this is due to a windows oddity with closing the calling
window when a batch script exits you can discard it but if your batch
file exits with a status code it will terminate your calling shell if
you do.

The last question to cover here is where to place your scripts?

I tend to put them under the scripts folder of NSClient++ which makes
things simple. This is not strictly a requirement but for me it makes
things simpler. If you are bundling scripts and distributing them to
many node it might be a good idea to place them in a “local” subfolder
to prevent accidental overwrite if I were to include more scripts in the
future.

.. image:: /images/scripting-on-the-windows-side-image1.png

So now that we (presumably) have our scripts placed somewhere it is time
to use them from NSClient++.

Configuration
-------------

The first thing we need is the CheckExternalScritps module which
provides us with the ability to run scripts. To bring in that module we
use the following command:

.. code-block:: bash

   nscp settings --activate-module CheckExternalScripts --add-defaults

This brings in 5 new section and about 50 or so or so new lines in our
configuration file.

All sections are under **/settings/external scripts** so if your
configuration file is bigger you need only care about sections starting
with **/settings/external scripts**.

Lets run through the sections briefly:

-  /settings/external scripts
   Main section where you configure the actual module
-  /settings/external scripts/alias
   Section for aliases (see below), aliases are in short just another
   name for another command.
-  /settings/external scripts/scripts
   **This is where we place the actual scripts!**
-  /settings/external scripts/wrapped scripts
   Another macro based place to place scripts (see below).
-  /settings/external scripts/wrappings
   Section for defining macros for the wrapped scripts.

Writing a script
----------------

This is a very short section as writing scripts is first of all much the
same as it is for Nagios but also a rather long and complicated topic
(since there are hundreds of language you can write scripts in).

A quick check_ok.bat script looks like this:

.. code-block:: bash

   @echo OK: Everything is going to be fine a
   @exit 0

The @ signs prevents the line from being echoed (you can put @echo off
to disable echoing as well). Anything after echo will be displayed on
the console and you use exit to return a status. The statuses are the
same as in Nagios i.e:

-  0 = ok
-  1 = warning
-  2 = critical
-  3 = unknown

So if instead we want to return a critical state we would rewrite the
script like so:

.. code-block:: bash

   @echo OK: Everything is not going to be fine a
   @exit 2

Adding a script
---------------

So lets start by adding a script to the configuration.

The simplest way to add a script is to create a new key value pair under
the scripts section like so:

.. code-block:: ini

   [/settings/external scripts/scripts]
   custom\_ok = "scripts\\\\custom\\\\check\_ok.bat"
   custom\_crit = "scripts\\\\custom\\\\check\_crit.bat" "Hello World"
   custom\_check\_perl = "C:\\strawberry\\\\perl\\\\bin\\\\perl.exe" scripts\\\\custom\\\\check\_perl.pl "Argument 1" "Argument " "$ARG1$"

The first keyword "custom\_ok" is the name of the command we just create
and the latter part is the command to execute. I prefixed my scripts
custom\_again to avoid clashing if an internal commands comes along
with your name it wont be overwritten. The only other ting to notice is
that strings need to have \\ escaped (and various other control
characters").

Adding more complicated scripts such as perl is not much more difficult
all you do is add the exact same thing you would run from the command
line. See for instance above in the custom_check_perl example.

Arguments
---------

Arguments can be a rather confusing subject and the biggest issue is
probably the various “allow arguments” flags you might encounter so lets
cover that first.

The reason for the “allow arguments” options are to provide a security
measure since NRPE lacks authentication (`something I have added in
NSClient++ <http://blog.medin.name/?p=480>`__).

If you do not allow arguments to be injected it means that all commands
have to be predefined (configured inside NSClient++) and thus are
harmless (ish).

Where as this is fine on paper it creates a massive administrative
burden so a lot of people want to allow arguments to make it easy to
configure and change checks centrally. Now what usually confuses people
is that this option exists in two places.

You can allow or disallow arguments for the NRPE server and you can do
so for the CheckExternalScripts module.

-  Enabling them only for NRPE would allow arguments for all internal
   commands but not for scripts.
-  Enabling them only for CheckExternalScripts would not make much sense
   really
-  Enabling them for both would allow external scripts (and internal
   commands) to have arguments.

So if your script has command line arguments you have three options:

#. Allow arguments from BOTH and configure the arguments from Nagios.
#. Allow arguments from CheckExternalScripts and define an alias (see
   below)
#. Don’t allow arguments and create the definition (with arguments)
   inside NSClient++ configuration.

The other issue is how to configure them.

.. code-block:: ini

   [/settings/external scripts/scripts]
   custom\_1 = "scripts\\\\custom\\\\check.bat"
   custom\_2 = "scripts\\\\custom\\\\check.bat" --help
   custom\_3 = "scripts\\\\custom\\\\check.bat" $ARG1$
   custom\_4 = "scripts\\\\custom\\\\check.bat" --date $ARG1$ --foo $ARG2$ --bar $ARG3$

In this examples we have a few different ways to define arguments. We
start off running the script with out them and then we have a hard coded
argument.

Next up comes the more interesting $ARG1$ syntax which will take the
argument from the incoming command (think check_nrpe … –a THIS). Lastly
you can see that you can mix and match between $ARG?$ and hard coded
options. The number of arguments are not limited so you can easily
create $ARG1234567890$ but my guess is you would run out of space since
NRPE only allows 1024 chars. If you argument has spaces in it it is
probably a good idea to enclose it inside quotes like so “$ARG1$”.

Running a script (A full example)
---------------------------------

As always I advocate starting your tests inside NSClient++ and not from
the Nagios console. This saves you a lot of time and makes life easier.
But before we get ahead or ourselves lets start with the configuration I
will use here:

.. code-block:: ini

   [/modules]
   CheckExternalScripts = enabled
   NRPEServer = enabled
   
   [/settings/NRPE/server]
   allow arguments = true
   
   [/settings/external scripts]
   allow arguments = true
   
   [/settings/external scripts/scripts]
   test1 = scripts\\\\check\_test.bat
   test2 = scripts\\\\check\_test.bat Hello $ARG1$ "$ARG2$"

Here we have enabled NRPE server and CheckExternalScripts we also allow
arguments and define two scripts test1 and test2.

The first thing we need to test is that the scripts work so lets start
NSClient++ in test mode (make sure you have stopped the service):

.. code-block:: text

   d:\\source\\build\\x64\\dist> nscp test
   ...
   debug core NSClient++ - 0,4,2,1 2012-08-08 Started!
   message client Enter command to inject or exit to terminate...

Next up we run the first script:

.. code-block:: text

   test1
   debug core Injecting: test1...
   debug ext-script Arguments:
   debug core Result test1: CRITICAL
   message client CRITICAL:CRITICAL: Everything is not going to be ok! ( )

Not that exciting we can see the script worked and returned a critical
state. To make things a bit more interesting lets run the second one
which takes arguments instead:

.. code-block:: text

   test2 world foo
   debug core Injecting: test2...
   debug ext-script Arguments: Hello world foo
   debug core Result test2: CRITICAL
   message client CRITICAL:CRITICAL: Everything is not going to be ok!
   (Hello world foo)

So arguments seems to work, now since we have enabled NRPE lets try
locally from NRPE as well to that open up a new console window and run
the following commands. If it does not work please go back to the first
console and check the log which usually tells you want is wrong!

.. code-block:: bash

   d:\\source\\nscp\\build\\x64>nscp nrpe -H 127.0.0.1 -- -c test1
   CRITICAL: Everything is not going to be ok! ( )
   d:\\source\\nscp\\build\\x64>nscp nrpe -H 127.0.0.1 -- -c test2 -a 1 2 3
   CRITICAL: Everything is not going to be ok! (Hello 1 2)

Simplifying with wrapped scripts
--------------------------------

Now as you saw above the Perl command line started to become a bit
cumbersome so what if you have 30 Perl scripts? Not so fun, especially
not once you change from Strawberry to activestate or something similar
so the command changes for all of them.

To resolve this I added something called wrapped-scripts. The reside in
the own section called: **/settings/external scripts/wrapped
scripts**. Essentially a wrapped script will use a macro during
instantiation splitting the script configuration from the runtime
configuration.

The way it works is you define a template (macro) for a given extension
and once you add (to the wrapped scripts section, not the normal scripts
section) a script with that extension the template will be used.

The default wrappings are for batch, vba and powershell scripts. But you
can easily define you own as I have done below for pl scripts.

.. code-block:: ini

   ; A list of wrappped scripts (ie. using the template mechanism)
   [/settings/external scripts/wrapped scripts]
   custom\_ok = check\_ok.bat
   custom\_crit = check\_crit.bat "Hello World"
   custom\_check\_perl = check\_perl.pl "Argument 1" "Argument " "$ARG1$"
   
   ; A list of templates for wrapped scripts
   [/settings/external scripts/wrappings]
   ; Perl scripts
   pl = "C:\\\\strawberry\\\\perl\\\\bin\\\\perl.exe" scripts\\\\%SCRIPT% %ARGS%
   ; BATCH FILE WRAPPING -
   bat = scripts\\\\%SCRIPT% %ARGS%

The way it works is that when our .pl script is found it looks up the pl
template and replaces %SCRIPT% with the name of the script and %ARGS%
with the list of arguments and then use the resulting command line
instead. As you can see I usually also specify the folder of the script
in the template which makes it very simple to add scripts.

Simplifying with aliases
------------------------

Now first off I want to say that aliases should never have been included
in the CheckExternalScripts module and in 0.4.2 they will be removed.
Now don’t get excited they will instead be included in the core where
they belong!

Aliases are extremely useful and the best way to kick start your
monitoring.

But they are not really script related in fact I would say they are more
useful for internal commands then they are for scripts.

So what are aliases then? Well they are a way to remove options you
never want to change. Think of aliases as the feature with the same name
in the Unix shell (at least in bash). You create a predefined command
with you can run without having to specify all the options.

A good example: A standard CheckCPU check might look like this:
“checkCPU warn=80 crit=90 time=5m time=1m time=30s” but that’s a lot of
typing to do on the Nagios server since it is always the same you can
create an alias like so and just call “alias_cpu”.

.. code-block:: ini

   [/settings/external scripts/alias]
   alias\_cpu = checkCPU warn=80 crit=90 time=5m time=1m time=30s

Conclusion
----------

Well, that’s pretty much it.

Running external script is pretty simple and don’t forget to use wrapped
script if you keep having to type a lot in your script command line.
And remember alias is not just for scripts just as useful for internal
commands as well.

