Putting some client into NSClient
#################################
:date: 2012-12-16 09:33
:author: Michael Medin
:category: Monitoring
:tags: icinga, nagios, nrpe, nsca, nsclient++
:slug: putting-some-client-into-nsclient
:image: /images/image6.png
:social_image: /images/image6.png

NSClient++ despite its name is most often used in server mode
responding to remote calls via either NRPE or check_nt. The closest
thing to a client we get in normal mode of operation is NSCA where we
submit data back. But NSClient++ can act as a client as well which is
not just something I use for unit testing but something which can
actually be useful in your monitoring environment.

.. PELICAN_END_SUMMARY

A good example of a really useful feature is creating a proxy or use
NSClient++ as proxies to add intelligence (see my post earlier on
writing stateful scripts `Enhance your monitoring with stateful
scripts <http://blog.medin.name/?p=447>`__).

We will quickly go though the command line interface for using it is a
check client following that we will look at using the clients from
within NSClient++ both from checks and scripts and finally we will setup
a simple NRPE proxy for checking machines on a remote inaccessible
network. As a bonus exercise I will show how to create a NRPE-to-NSCA
proxy to create a passive-active bridge to help you transition from an
active setup to a passive one if you are so inclined.

**Introduction to clients**
===========================

Before we start using the which has been touched briefly many times
before in various blog posts so I will try to explain some of the
underlying concepts you will encounter.

**Command line context (client)**
---------------------------------

The first concept to understand is that the command line interface has
“contexts” in our case we want to use the "client context". But many
protocols has short hands to reduce the typing thus the following two
commands are equivalent:

-  *nscp client --module NRPEClient*
-  *nscp nrpe*

I tend use the latter format for brevity but it is important to
understand that is is merely an alias.

**Command line arguments**
--------------------------

The second important thing to understand is that running nsclient++ is
client mode means arguments are picked up by two different components.
First we have the "loader" which accepts arguments such as log, help etc
etc. Then we have the loaded module which accept arguments such as host
and port.

|image|

To make this transparent for the user the loader will pass along any
unknown options and use (eat) all the ones it knows about. This is all
well and good as long as the options are distinctly different. For
instance ***--host*** will never be used by the loader. But as soon as
we have options which are used by both parties such as ***--help***\ it
will becomes a bit awkward because unexpectedly the loader might pickup
options we intended for the module. To work around this you can use the
double dash (--) to denote that all options after this will be intended
for the module (and ignored b the loader).

The best illustration for this is to compare the result of these two
commands:

-  *nscp nrpe --help*
-  *nscp nrpe **--** --help*

The first will give you information about logging and other things which
the loader will understand the latter will give you information about
nrpe connection details which the module understands.

**Operation mode: Query/Exec/Submit?**
--------------------------------------

NSClient++ support several "modes" which are modeled on top of Nagios
the various monitoring paradigms.

|image|

We have (currently) three main modes (with a fourth planned):

#. **Query** modeled on top of NRPE
   In simple terms this is "check\_xxx" which results in a return
   status, a message and performance data.
#. **Submit** modeled on top of NSCA
   In simple terms this is telling the remote node status, a message
   and performance data.
#. **Exec** intended to execute functions
   This is similar to query but the data is more free form.

Which one to use depends on what we want to accomplish but in general if
you use NRPE you probably want query. if you are using NSCA or NRDP you
probably want submit. And if you want to run remote scripts you probably
want exec.

Using the command line

Using the command line
======================

Now that we have sorted out the important bits we end up with the
following to run as a nrpe client:

-  *nscp nrpe -- ...*

And we just stack all options at the end much like we would with
check_nrpe.

If we instead want to submit via NSCA we simply replace nrpe with nsca
and stack on various options related to submissions instead. So what are
the options?

Well, best way is to use the --help command like so:

.. code-block:: text

     Common options:
     -H [ --host ] arg The host of the host running the server
     -P [ --port ] arg The port of the host running the server
     --address arg The address (host:port) of the host running the server
     -T [ --timeout ] arg Number of seconds before connection times out
     (default=10)
     -t [ --target ] arg Target to use (lookup connection info from config)
     -q [ --query ] Force query mode (only useful when this is not already
     obvious)
     -s [ --submit ] Force submit mode (only useful when this is not already
     obvious)
     -e [ --exec ] Force exec mode (only useful when this is not already
     obvious)
     -h [ --help ] Display help information
    
    .. raw:: html
    
       </p>
    
    Command: query:
     -c [ --command ] arg The name of the query that the remote daemon
      should
     run
     -a [ --arguments ] arg list of arguments
     --query-command arg The name of the query that the remote daemon
      should
     run
     --query-arguments arg list of arguments
    
    Command: submit:
     -c [ --command ] arg The name of the command that the remote daemon
      should
     run
     -a [ --alias ] arg Same as command
     -m [ --message ] arg Message
     -r [ --result ] arg Result code either a number or OK, WARN, CRIT,
      UNKNOWN
    
    Common options for nrpe:
     -n [ --no-ssl ] Do not initial an ssl handshake with the server,
     talk in plaintext.
     --certificate arg Length of payload (has to be same as on the
     server)
     --dh arg The pre-generated DH key (if ADH is used this
     will be your 'key' though it is not a secret key)
     --certificate-key arg Client certificate to use
     --certificate-format arg Client certificate format (default is PEM)
     --ca arg A file representing the Certificate authority
     used to validate peer certificates
     --verify arg Which verification mode to use: none: no
     verification, peer: that peer has a certificate,
     peer-cert: that peer has a valid certificate, ...
     --allowed-ciphers arg Which ciphers are allowed for legacy reasons
      this
     defaults to ADH which is not secure preferably
     set this to DEFAULT which is better or a an even
     stronger cipher
     -l [ --payload-length ] arg Length of payload (has to be same as on
      the
     server)
     --buffer-length arg Same as payload-lenght (used for legacy reasons)
     --ssl Initial an ssl handshake with the server.
    >THE END<

As you can see there is a lot of options but a lot of it is for various
things you probably wont need initially so if we remove ssl/certificate
related options (Which you can find more about in the `Securing NRPE
With certificate based
authentication <http://blog.medin.name/?p=480>`__) as well as all modes
apart from query we end up with the following list:

.. code-block:: text

     Common options:
     -H [ --host ] arg The host of the host running the server
     -P [ --port ] arg The port of the host running the server
     --address arg The address (host:port) of the host running the server
     -T [ --timeout ] arg Number of seconds before connection times out
     (default=10)
     -t [ --target ] arg Target to use (lookup connection info from config)
     -h [ --help ] Display help information
    
    .. raw:: html
    
       </p>
    
    Command: query:
     -c [ --command ] arg The name of the query that the remote daemon
      should
     run
     -a [ --arguments ] arg list of arguments
    
    Common options for nrpe:
     -n [ --no-ssl ] Do not initial an ssl handshake with the server,
     talk in plaintext.
    >THE END<

And this is very similar to the check_nrpe options which in turns means
it is very similar to how you use check_nrpe. So one might argue that
the benefit to NSClient++ as a client is limited. And indeed it is but
in contrast to NRPE which is essentially a dead project NSClient++ is
evolving. For instance in 0.4.1 we introduced full SSL support and in
0.4.2 we are planning to add protocol tweaks to support passwords as
well as variable length payloads.

As you saw there is a lot of options and going into them in detail is
beyond the scope of this article so I will leave it with the following
two examples:

-  nrpe
   nscp nrpe -- --host 127.0.0.1 –port 5556 –command check\_command
   –arguments foo bar
-  nsca
   nscp nsca …

One thing I want to touch briefly before continuing is targets. A target
is much like a host definition inside
`NSClient++ <http://nsclient.org/>`__ so instead of adding all the hosts
ports and security details you can simply specify the target and
configure the other options in the configuration file.

-  *nscp settings --path /settings/NRPE/client/targets --key **foo**
   --set **127.0.0.1***

Then we can use it like so:

-  *nscp nrpe -- --target **foo** --command check_ok*

**Check client**
================

So hopefully now you have a solid understanding of how the clients work
lets move on and explore how you can use them from within NSClient++ as
check commands.

Lets first load the NRPEClient and see which commands we have:

nscp settings --activate-module NRPEClient

Then we do

.. code-block:: text

     nscp test
     …
     commands
     l ce\\simple\_client.hpp:57 \| nrpe\_exec: Execute (via query) remote
    NRPE host
     l ce\\simple\_client.hpp:57 \| nrpe\_forward: Forward query to remote
    NRPE host
     l ce\\simple\_client.hpp:57 \| nrpe\_help: Help on using NRPE Client
     l ce\\simple\_client.hpp:57 \| nrpe\_query: Check remote NRPE host
     l ce\\simple\_client.hpp:57 \| nrpe\_submit: Submit (via query) remote
    NRPE host
    >THE END<

As discussed earlier for NRPE most of these commands are not useful
since NRPE is a single paradigm protocol. So lets focus on nrpe_query.

-  *nrpe_query --help*

Now this screen looks surprisingly like the command line help screen and
that is because this is in many ways exactly the same command.

So accessing a remote NRPE server we would use the following commands:

-  *nrpe_client -H 123.45.67.89 -c check_ok*
-  **nrpe_client --host 123.45.67.89 --command check_ok**
-  **nrpe_client host=123.45.67.89 command=check_ok**

They are all the same but the last version is better suited to run from
check_nrpe and other remote queries since they do not allow the --
syntax for options. So using clients from within NSClient++ is almost
the exact same as using them from command line. But before we move on to
the script lets revisit targets a bit. Previously the target was defined
like this:

.. code-block:: text

     [/settings/NRPE/client/targets]
     foo=127.0.0.1
    >THE END<

This is marginally useful since all we can configure is host and port.
What if we want to disable SSL as well? Then we use the longer object
format instead which looks like this (notice the section name now
includes the alias which means all the options in this section relates
to the alias).

.. code-block:: text

     [/settings/NRPE/client/targets/foo]
     address=127.0.0.1
     ssl=false
    >THE END<

**Scripts**
===========

Scripts are very similar to the previous use cases (which has been the
idea all along) the main difference is that we can now use both modes of
execution.

#. Queries
   This is exactly the same as using the *nrpe\_client* command above.
#. Executions
   This is the exact same as using nrpe from the command line above.

So we have already been through this but I will give a quick example
here using `Python <http://www.lua.org/>`__.

.. code-block:: python

     core = Core.get()
    
    .. raw:: html
    
       </p>
    
    args = [
     '--command', 'check\_ping'
     '--arguments', 'Hello World',
     '--address', '127.0.0.1:5666',
     ]
    
    # Using execution
     (result\_code, result\_message) = core.simple\_exec('any',
      'nrpe\_query', args)
    
    # Using query:
     (res, msg, perf) = core.simple\_query('nrpe\_query', args)
    >THE END<

So now you might be wondering what the difference between execution and
query is?

And as I mentioned initially the main difference between them is the way
the data is sent. In a query for instance performance data is parsed,
when you execute something the result is only raw text. The idea behind
the execution mode is to execute commands not retrieve data. So in this
case when we execute something we do not get performance data as a
separate field.

NRPE proxy
==========

So lets put all this together and execute some remote-remote checks but
first lets set the scene so it will be simpler to keep track of things.
We have our Monitoring Server server running check_nrpe against our
Proxy server (running NSClient++) which in turn will use the NRPEClient
to run the check against the Monitored Host.

|image|

First we need to configure the proxy

.. code-block:: text

     [/modules]
     NRPEServer=enabled
     NRPEProxy=enabled
     [/settings/NRPE/server]
     allowed hosts=10.0.0.1
     allow arguments=true
    
    .. raw:: html
    
       </p>
    
    >THE END<

Next we configure our remote NRPE on our Monitored Host to accept
requests from our Proxy.

[sourcecode language="actionscript3"]
 # Regular nrpe.cfg from our Linux server
 allowed_hosts=10.0.1.1
 [/sourcecode]

Finally we execute our check from the monitoring server (here we use the
syntax without -- since check_nrpe wont allow us to have -- or - in the
arguments).

-  *check_nrpe -H 10.0.1.1 -c nrpe_query \\
   host=10.0.1.23 command=check\_ok*

**Bonus section: NSCA-NRPE Proxy**
==================================

I thought I would return to a subject I have brought up several times on
various presentations since I think it is neat if not all that useful
feature. But it is a good way to explain things you can do.

|image|

This is similar to the above NRPE Proxy solution but instead of
scheduling checks from the Monitoring server we schedule them from the
Proxy and submit them back passively via NSCA.

The setup on the Monitored Host is the same so all we need to do is
change the Proxy configuration as below:

.. code-block:: text

     [/modules]
     NRPEClient = enabled
     NSCAClient = enabled
     Scheduler = enabled
    
    .. raw:: html
    
       </p>
    
    [/settings/NSCA/client/targets/remote\_host]
     address = 10.0.0.1
     encryption = xor
     password = secret-password
    
    [/settings/scheduler/schedules/remote\_host\_check\_ok]
     ; SCHEDULE ALIAS - The alias (service name) to report to server
     alias = check\_ok
     ; SCHEDULE CHANNEL - Channel to send results on
     channel = NSCA
     ; SCHEDULE COMMAND - Command to execute
     command = nrpe\_query --host 10.0.1.23 --command check\_ok
     ; SCHEDULE INTERAVAL - Time in seconds between each check
     interval = 5s
     ; TARGET - The target to send the message to (will be resolved by the
      consumer)
     target = remote\_host
    >THE END<

The main difference is that we need to change NRPEServer for NSCAClient
and of course configure our NSCA connection details including encryption
and password. We also need to configure all our checks under the
schedules section. In my case here I simply have a single one called
remote_host_check_ok which runs check_ok on our remote host.

Conclusion
==========

So that’s pretty much all you can do with clients. Hopefully you will
find some cool and interesting things you can use in your monitoring
infrastructure.

**UPDATE:**

As James Jimmy Burns (`@JimBurns83 <https://twitter.com/JimBurns83>`__)
noticed nrpe_client does not support -- in arguments so I have updated
both NSClient++ and the tutorial to instead use host=192.168.0.1 over
--host 192.168.0 etc. (Notice that this syntax requires 0.4.1.73 of
NSClient++)

.. |image| image:: /images/image_thumb6.png
   :target: /images/image6.png
.. |image2| image:: /images/image_thumb7.png
   :target: /images/image7.png
.. |image3| image:: /images/image_thumb8.png
   :target: /images/image8.png
.. |image4| image:: /images/image_thumb9.png
   :target: /images/image9.png
.. |image5| image:: /images/image_thumb10.png
   :target: /images/image10.png
