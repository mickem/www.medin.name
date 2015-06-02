Using WMI with NSClient++ 0.4.0 Part 1: Command line tools
##########################################################
:date: 2012-03-09 00:52
:author: Michael Medin
:category: Monitoring
:tags: monitoring, NSCP, windows, WMI
:slug: using-wmi-with-nsclient-0-4-0-part-1-command-line-tools
:image: /images/wlEmoticon-smile.png
:social_image: /images/wlEmoticon-smile.png

This is a series detailing how you can leverage WMI to monitor you
Computers from a monitoring tool such as Nagios or Icinga. Since I
decided to clean up the command line syntax of the WMI plugin for
NSClient++ for the up-coming 0.4.0 version a few days ago I will start
by showing how you can use what has become an almost full featured WMI
client.

.. PELICAN_END_SUMMARY

NSClient++ 0.4.0
================

First off this is upcoming 0.4.0 it is available in the latest nightly
build but I should probably not recommend installing that into your
production environment |Ler|. The “last” RC for 0.4.0 has just been
released so feel free to
`download <http://nsclient.org/nscp/downloads>`__ that and let me know
anything which breaks before you get started on this. Anyways, The first
thing if you don’t know anything about NSClient++ command line syntax is
that it uses a concept similar to git and what not. Meaning the first
“option” is a command and everything else works like options (with
double dashes).

So you can do:

[sourcecode language="bash" padlinenumbers="true"]
 nscp help
 ...
 nscp client --exec ...

[/sourcecode]

The core defines a series of “context” such as settings, client,
service, test, etc etc but modules can also provide similar
functionality. To use this we use the “client” mode. Which is similar to
starting NSClient++ before running the command the shutting it down
again afterwards.

In our case we want to use the module called CheckWMI so we need to add
***--modules CheckWMI*** end up with the following command:

[sourcecode language="bash"]
 nscp client --module CheckWMI
 CheckWMI Command line syntax:
 Allowed options:
 -h [ --help ] Show help screen
 -s [ --select ] arg Execute a query
 --list-classes arg list all classes of a given type
 --list-instances arg list all instances of a given type
 --list-ns list all name spaces
 -l [ --limit ] arg Limit number of rows
 -n [ --namespace ] arg (=root\\cimv2) Namespace
 -c [ --computer ] arg A remote computer to connect to
 -u [ --user ] arg The user for the remote computer
 -p [ --password ] arg The password for the remote computer
 [/sourcecode]

Now this is a bit of hand full to type so there are a set of short hand
aliases you can use to reduce the amount of typing. In our case we want
to use the wmi alias which is equivalent to the above command:

[sourcecode language="bash"]
 nscp wmi
 CheckWMI Command line syntax:
 Allowed options:
 -h [ --help ] Show help screen
 -s [ --select ] arg Execute a query
 --list-classes arg list all classes of a given type
 --list-instances arg list all instances of a given type
 --list-ns list all name spaces
 -l [ --limit ] arg Limit number of rows
 -n [ --namespace ] arg (=root\\cimv2) Namespace
 -c [ --computer ] arg A remote computer to connect to
 -u [ --user ] arg The user for the remote computer
 -p [ --password ] arg The password for the remote computer
 [/sourcecode]

Namespaces
==========

So now that we know how to access the WMI command line what can we
actually do with it?

Well a lot actually so lets start off by exploring namespaces.
Namespaces in WMI is a bit like a path or folder on your file system or
a package in your java code. In other words a hierarchical structure
used to make it simpler to find things.

The default namespace (if you do not specify one) is root\\cimv2 which
is where most of the normal system classes reside but there are a lot of
things in other namespaces and most server components such as SQL Server
and Exchange will provide their own namespaces. So listing namespaces is
a pretty important first step.

So how can we figure out which namespaces are available?

Conveniently the CheckWMI plugin provides not only one command for this
but two. The first ***--list-ns*** will list all child namespaces in a
given parent namespace. The second ***--list-all-ns*** will list all
children (and grandchildren) recursively from a given namespace. An
important thing to notice is that **the default namespace is always
root\\cimv2** which means that if you want to list ALL namespaces you
**need to specify the** **root namespace instead** by adding the
“\ ***--namespace root***\ ” option.

[sourcecode language="bash"]
 nscp wmi --list-all-ns --namespace root
 root\\subscription
 root\\subscription\\ms_41d
 root\\subscription\\ms_409
 ...
 root\\CIMV2
 root\\CIMV2\\Security
 root\\CIMV2\\Security\\MicrosoftTpm
 root\\CIMV2\\Security\\MicrosoftVolumeEncryption
 root\\CIMV2\\ms_41d
 ...
 root\\Microsoft\\SqlServer
 root\\Microsoft\\SqlServer\\ServerEvents
 root\\Microsoft\\SqlServer\\ServerEvents\\SQLEXPRESS
 root\\Microsoft\\SqlServer\\ComputerManagement
 root\\Microsoft\\SqlServer\\ComputerManagement\\ms_409
 ...
 [/sourcecode]

As we can see here SqlServer has its own namespace so whenever we want
to query from there we need to use the namespace option.

An interesting side note which I discovered after a few hours of
googling for an API to list namespaces was that namespaces are in fact
instances of a class called __Namespace. Hence there is no API to list
them which now that I know it it is kind of obvious but this means that
***--list-ns*** is really wrapper for ***--list-instance
__Namespace*** but lets not get ahead of ourselves.

Now that we have hopefully understood namespaces lets move on to the
next logical component: classes.

Listing Classes
===============

Classes is what WMI calls which I would call tables or objects.
Basically you can think of a class as a type of objects which has
instances (rows) as well as methods and metadata and what not. In
NSClient++ we only deal with instances and attributes currently but that
will probably change in the next version (0.4.2).

Using the command line of NSClient++ there is just a single option
(***--list-classes***) for listing object so it is pretty straight
forward. The option takes an optional base class argument. This is a
probably on the **advanced** side of things but since Classes are
hierarchical (think inheritance) you can filter on just a certain kind
of base class. But most likely you wont be needing this if you are
reading this. So all you are left with are two other options one being
***--namespace*** which is where you specify the namespace the other is
***--limit*** where you can limit the result set.

Here we have all the classes we can query under the
*root\\Microsoft\\SqlServer \\ComputerManagement namespace*.

[sourcecode language="bash"]
 nscp wmi --list-classes --namespace
root\\Microsoft\\SqlServer\\ComputerManagement
 \| __CLASS \|
 \|-------------------------------------\|
 \| __NotifyStatus \|
 \| __ExtendedStatus \|
 ...
 \| ClientNetworkProtocol \|
 \| ServerNetworkProtocol \|
 \| SqlServerAlias \|
 \| ServerNetworkProtocolProperty \|
 \| ServerSettings \|
 \| SqlServiceAdvancedProperty \|
 \| SecurityCertificate \|
 \| ClientSettingsGeneralFlag \|
 \| ClientNetLibInfo \|
 \| ServerNetworkProtocolIPAddress \|
 \| SqlService \|
 \| RegServices \|
 \| ClientNetworkProtocolProperty \|
 \| ServerSettingsGeneralFlag \|
 [/sourcecode]

So now we know our way around and can find a set of classes in a
hierarchical namespace structure which means we have to start exploring
what the classes can provide us with.

Making Queries
==============

There are basically two ways to query information. The first is
***--list-instances*** which lists all instance of a class and the
second is ***--select*** where you ask a “WQL” query. I tend to almost
always use the latter as it gives you more flexibility and power. First
off lets explain what WQL is if you are familiar with SQL (or for that
matter the filter syntax of NSClient++) you are spot on. WQL (WMI Query
Language) is a query language modeled on SQL but it is a bit different
as WMI is an object oriented data store and SQL usually deals with a
relational data store. Regardless for normal use your basic SQL skills
will normally get you far enough.

The main benefit to using WQL over listing instances is that the query
language allows you to limit the information you get back.

.. code-block:: bash

   nscp wmi --list-instances SqlService --namespace root\\Microsoft\\SqlServer\\ComputerManagement
   \| AcceptPause \| AcceptStop \| BinaryPath \| Dependencies \| Description \| DisplayName \| ErrorControl \| ExitCode \| HostName \| Name \| ProcessId \| SQLServiceType \| ServiceName \| StartMode\| StartName \| State \|
   \|-------------\|------------\|--------------------------------------------------------------------------------------------\|--------------\|----------------------------------------------------------------------------------------------\|-------------------------\|--------------\|----------\|-------------\|---------\|-----------\|----------------\|------------------\|-----------\|-----------------------------\|-------\|
   \| TRUE \| TRUE \| "c:\\Program Files (x86)\\Microsoft SQL Server\\MSSQL.1\\MSSQL\\Binn\\sqlservr.exe" -sSQLEXPRESS \| UNKNOWN \| Provides storage, processing and controlled access of data and rapid transaction processing. \| SQL Server (SQLEXPRESS) \| 1 \| 0 \| MIME-LAPTOP \| Unknown \| 2780 \| 1 \| MSSQL$SQLEXPRESS \| 2\| NT AUTHORITY\\NetworkService \| 4 \|
   \| TRUE \| TRUE \| "c:\\Program Files (x86)\\Microsoft SQL
   Server\\90\\Shared\\sqlbrowser.exe" \| UNKNOWN \| Provides SQL Server
   connection information toclient computers. \| SQL Server Browser \| 1 \|
   0 \| MIME-LAPTOP \| Unknown \| 3636 \| 7 \| SQLBrowser \| 2\| NT
   AUTHORITY\\NetworkService \| 4 \|

Versus:

.. code-block:: bash

   nscp wmi --select "select DisplayName, State, ProcessId from
   SqlService" --namespace root\\Microsoft\\SqlServer\\ComputerManagement
   \| DisplayName \| ProcessId \| State \|
   \|-------------------------\|-----------\|-------\|
   \| SQL Server (SQLEXPRESS) \| 2780 \| 4 \|
   \| SQL Server Browser \| 3636 \| 4 \|

The last one is a lot more readable and contain hopefully the
information you actually want. And if you really want all the
information you can still ***select \* from ..*** to get exactly same
result as ***--list-instances***. So to be fair I don’t really see a
point to using the ***--list-instance*** option |Ler|

Remote machines
===============

Another nifty thing you can do is make remote queries.

There are a set of option ***--computer***, ***--user*** and
***--password*** which can be used to do this remotely on another
machine on your network.

Remember the ***--list-all-ns*** command we used in before? Here is the
same command targeting a virtual machine remotely.

.. code-block:: bash

   nscp wmi --list-all-ns --computer mmedin-vm --user YYY --password XXX --namespace root
   \\\\mmedin-vm\\root\\ServiceModel
   \\\\mmedin-vm\\root\\SECURITY
   \\\\mmedin-vm\\root\\MSAPPS12
   ...
   \\\\mmedin-vm\\root\\CIMV2
   \\\\mmedin-vm\\root\\CIMV2\\ms_409
   \\\\mmedin-vm\\root\\CIMV2\\Applications
   \\\\mmedin-vm\\root\\CIMV2\\Applications\\MicrosoftIE
   ...
   \\\\mmedin-vm\\root\\subscription
   \\\\mmedin-vm\\root\\subscription\\ms_409
   \\\\mmedin-vm\\root\\nap

Naturally all commands you can do locally will also work remotely so you
can also query for information as well as list namespaces, classes and
instances.

Scripts
=======

Since this is an internal command there are APIs available so you can
use these commands from scripts as well. To demonstrate this I will show
a simple python script which lists all objects in all namespaces. To do
this we use the ***--list-all-ns*** command to list all namespaces and
then loop through the list and for each namespace we call
***--list-classes*** with that namespace. To make things simple to work
with from a scripting perspective there is an option we can use to
simplify the output ***--simple*** will return the data as a comma
separated list which is simpler to parse in our python script.

The script in its entirety looks like this:

.. code-block:: python

     from NSCP import Core
     core = Core.get()
    
    def \_\_main\_\_():
     # List all namespaces recursivly
     (ret, ns\_msgs) = core.simple\_exec('any', 'wmi', ['--list-all-ns',
      '--namespace', 'root'])
     for ns in ns\_msgs[0].splitlines():
     # List all classes in each namespace
     (ret, cls\_msgs) = core.simple\_exec('any', 'wmi', ['--list-classes',
      '--simple', '--namespace', ns])
     for cls in cls\_msgs[0].splitlines():
     print '%s : %s'%(ns, cls)
    >THE END<

Next post in this series

This ends this installment of “Using WMI with NSClient++”. In the next
section I will show how to use the various check commands you can use
from a monitoring tool such as Nagios or Icinga to make sure your
servers are working.

.. |Ler| image:: /images/wlEmoticon-smile.png
