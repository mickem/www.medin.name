NSClient++ for NRPE users
#########################
:author: Michael Medin
:tags: icinga, nagios, nrpe, nsclient++, NSCP
:image: /images/nrpe-vs-nsclient.png
:social_image: /images/nrpe-vs-nsclient.png

A lot of people coming to `NSClient++ <http://nsclient.org/>`__ has a
background in NRPE since it is a common transport mechanism for check
results on Linux.

And while NSClient++ is fully NRPE compatible it allows for more control
and has more features which can make it seem difficult to get started
with. This is a guide for getting started with NSClient++ from a NRPE
perspective.

.. PELICAN_END_SUMMARY

Overview
========

The biggest difference between NRPE and NSClient++
is that NSClient++ provides built-in commands through its modules. This
means that for many common checks you do not need to configure any
external scripts. The other major change is the configuration and
command line syntax is somewhat different.

The illustration tries to depict this visually. Where the regular NRPE
server (lower right) responds to a query and sends a reply NSClient++
(upper right) has a series of servers which accepts requests
(NRPEServer) which are forwarded to a number of modules
(CheckExternalScripts) which in turn execute the command. In a way one
could consider NSClient++ as a broker who facilitate exchange.

Configuration
=============

The configuration in NSClient++ is based on the Windows INI file format.
The structure of an ini file is somewhat similar to the NRPE
configuration format (and many other Linux configuration files) but it
also features section (which NRPE lacks). A simple configuration entry
might look like this:

.. code-block:: ini

     [section]
     key 1=value 1
     key 2 = value 2

When it comes to key names most are inherited from the Original NRPE
implementation so you should feel right at home. One difference is that
keys in NSClient++ use white space ( ) instead of under score (_). When
it comes to sections they are hierarchical and form a tree structure
where each module has its own node under /settings. To use NRPE and
external scripts you need to configure three sections:

#. Which modules to load (**/modules**)
#. Server properties (**/settings/default** and
   **/settings/NRPE/server**)
#. Execution properties (**/settings/external scripts**)

Modules
-------

The first thing we need to do is load the modules. In our example here
we load **NRPEServer** and **CheckExternalScripts** as well as
**CheckSystem** to showcase the features of a built-in module.
CheckSystem provides (amongst others) the check_cpu and check_mem
commands.

.. code-block:: ini

     [/modules]
     NRPEServer=enabled
     CheckExternalScripts=enabled
     CheckSystem=enabled

Default settings
----------------

Configuring defaults for our server is a good way to save yourself a few
lines of typing especially if you plan to use multiple protocols. The
default values are used whenever specific values are not pressent.

.. code-block:: ini

     [/settings/default]
     allowed hosts = 10.11.12.13

Thus the following would yield the same result:

.. code-block:: ini

     [/settings/NRPE/server]
     allowed hosts = 10.11.12.13

The value for **allowed hosts** is the Nagios IP address which we have
entered here as 10.11.12.13. The purpose is the same as the
allowed_hosts option in nrpe.conf where we configure which IP addresses
is allowed to connect.

Reloading settings
------------------

|restart-op5-nscp|\ Now we can restart the service and try connecting
from our `Nagios <http://www.nagios.org/>`__ server.

Simplest way to restart the service is to open a command prompt and
type:

.. code-block:: bat

   net stop nscp
   net start nscp

Another option is to restart the service from the **Service manager**.

Connecting
==========

The simplest way to diagnose connection details and network related
issues is to run **check_nrpe** without a command. This is identical
to the regular NRPE behavior and looks like this in the NSClient++ case:

.. code-block:: bat

     ./check\_nrpe -H <nsclient++ server ip>
     I (0.4.2.1 2013-06-05) seem to be doing fine...

If this works out we want to try running an internal command to validate
that everything is working ok. A simple one to use is alias_cpu which
will check the CPU metrics for us.

.. code-block:: bat

     ./check\_nrpe -H <nsclient++ server ip> -c alias\_cpu
     OK CPU Load ok.\|'5m'=0%;80;90 '1m'=0%;80;90 '30s'=1%;80;90

In case of errors
=================

If this did not work we probably want to do some debugging. This is
vastly different since on Linux with regular NRPE your first bet would
be the start tailing the syslog or messages file. But with NSClient++
your closest resemblance is the is the nsclient.log file.

But a much better option is the NSClient++ test mode. To activate test
mode all you need to do is shut down the regular client and start
NSClient++ in test mode:

.. code-block:: bat

   cd \\program files\\nsclient++
   net stop nscp
   nscp test
   ...
   ... wait
   ...
   ... error
   ...
   exit
   net start nscp

What this does is give you real-time debugging information as well as
errors and such.

Executing scripts
=================

Hopefully by now we have managed to connect and utilize the built-in
commands. Before we move on to external scripts lets discuss arguments a
bit since it is a source of confusion for many users. Arguments work
much the same as vanilla NRPE in that you can allow arguments and “nasty
characters”. The difficulty is that there are **TWO** places to allow
arguments:

#. NRPEServer
   For all inbound commands
#. CheckExternalScripts
   Only for external scripts

The reasoning behind this is that it **could be** considered less
dangerous to deny arguments only for externals scripts which are
executed by the shell (and a lot less to configure if you allow them for
internal commands). For details about arguments see the HOWTO about
using `external
scripts <http://docs.nsclient.org/howto/external_scripts.html#arguments>`__.

|external-scripts-args-2|

Scripts
=======

The final thing we need to do is load and configure scripts. This is a
bit different from the NRPE syntax but works much the same. You give
each script an alias which becomes the command. Arguments are forwarded
using $ARG1$ argument variables:

.. code-block:: ini

     [/settings/external scripts/scripts]
     test=scripts\\check\_ok.bat

You can add as many script as you like as long as the alias (command) is
unique.

Scripts on Windows
------------------

One snag which is really more related to how windows work than
NSClient++ is that most scripting languages requires the full command
line syntax.

This means that if I want to use a VBS (VisualBasic Script) I would have
to enter:

.. code-block:: ini

     [/settings/external scripts/scripts]
     test=cscript.exe //T:30 //NoLogo scripts\\check\_test.vbs
    

This means it is a lot more to configure when your using script on
Windows fortunately to combat this the concept of “wrapped scripts” was
added to NSClient++. Wrapped script work much like a macro where you can
define how vbs scripts are executed and have NSClient++ add-in all the
nitty gritty details.

The same command above using wrapped scripts look like this:

.. code-block:: ini

     [/settings/external scripts/wrapped scripts]
     test=check\_test.vbs
    

Which is much simpler, for more details on wrapped scripts see the HOWO
section about `wrapped
scripts <http://docs.nsclient.org/howto/external_scripts.html#wrapped-scripts>`__.

Summary
=======

So using NSClient++ if you have an NRPE background is not that
different. Most of the changes are simply syntactical. And once you get
started you will be able to explore many of the more advanced features
which NSCLient++ provides over the regular NSRPE program such as:

-  `Securing NRPE with certificate based
   authentication <http://blog.medin.name/?p=480>`__
-  `Real-time log file monitoring (both event log and text
   files) <http://blog.medin.name/?p=457>`__
-  `Enhance your monitoring with stateful
   scripts <http://blog.medin.name/?p=447>`__
-  Feel free to browse this blog for more articles as well as the
   `NSClient++ <http://nsclient.org/>`__ webpage.

**The full configuration is shown below:**

.. code-block:: ini

   [/modules]
   NRPEServer=enabled
   CheckExternalScripts=enabled
   CheckSystem=enabled
   
   
   [/settings/default]
   allowed hosts = 10.11.12.13
   
   [/settings/external scripts/scripts]
   test\_script=scripts\\check\_ok.bat
    
    

.. |nrpe-vs-nsclient| image:: /images/nrpe-vs-nsclient.png
.. |restart-op5-nscp| image:: /images/restart-op5-nscp.png
.. |external-scripts-args-2| image:: /images/external-scripts-args-2.png
